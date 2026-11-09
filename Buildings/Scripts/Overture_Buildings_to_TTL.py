#!/usr/bin/env python3
"""
Convert Overture Maps building GeoJSON / GeoJSONSeq to RDF/Turtle for the
University of Toronto City Digital Twin.

Implemented mapping:
- Overture building -> bdg:Building
- id -> genprop:hasIdentifier
- names.primary -> genprop:hasName
- geometry -> loc:associatedLocation -> loc:Location -> geo:asWKT
- subtype -> shared bdg:BuildingUse + code:Code
- height -> bdg:hasBuildingHeight -> cityunits:Length -> i72:Measure
- num_floors -> bdg:numAboveGroundFloors
- sources[] -> prov:Entity linked by prov:wasDerivedFrom
- building -> cdt:locatedInAdministrativeArea -> tor:toronto

Not mapped yet by design:
- Overture class
- sources[].update_time
- addresses (requires matching the separate Overture Addresses theme)

Production-scale behaviour:
- Supports ordinary GeoJSON FeatureCollections and Overture GeoJSONSeq.
- Streams GeoJSONSeq one feature at a time instead of loading the full file.
- Writes RDF in chunks, so the complete RDF graph does not stay in memory.
- Optionally clips buildings to a Toronto boundary GeoJSON. A FeatureCollection
  is allowed (for example the 140-neighbourhood GeoJSON); its geometries are
  unioned into one city boundary.
- Uses each building footprint's representative point for boundary membership.
  This avoids keeping buildings that merely touch the municipal boundary.

Examples:
    # Small/test GeoJSON
    python Overture_Buildings_to_TTL.py toronto_buildings.geojson

    # Full Overture GeoJSONSeq, streamed and clipped to Toronto
    python Overture_Buildings_to_TTL.py toronto_buildings_full.geojsonseq \
        --boundary neighbourhoods-historical-140-4326.geojson \
        -o toronto_overture_buildings_full.ttl

    # Quick production-format test on the first 10,000 input features
    python Overture_Buildings_to_TTL.py toronto_buildings_full.geojsonseq \
        --limit 10000 -o toronto_overture_buildings_test.ttl

Dependencies:
    pip install rdflib shapely
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterator, Optional, Set

from rdflib import Graph, Literal, Namespace, RDF, XSD
from rdflib.namespace import PROV
from shapely.geometry import shape
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union
from shapely.prepared import prep


# =============================================================================
# NAMESPACES
# =============================================================================

TOR = Namespace("http://ontology.eil.utoronto.ca/Toronto/Toronto#")
GENPROP = Namespace(
    "https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/"
)
CDT = Namespace("http://ontology.eil.utoronto.ca/CDT#")
LOC = Namespace(
    "https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/"
)
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
CODE = Namespace(
    "https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Code/"
)
CITYUNITS = Namespace(
    "https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/CityUnits/"
)
BDG = Namespace(
    "https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Building/"
)
I72 = Namespace("http://ontology.eil.utoronto.ca/ISO21972/iso21972#")

# The Administrative Areas graph uses the lowercase Toronto individual.
TORONTO_CITY = TOR.toronto

FIRST_CANADIAN_PLACE_ID = "cc964f89-dd07-4eec-a0d1-8fc383c3b264"

PREFIX_HEADER = """@prefix bdg: <https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Building/> .
@prefix cdt: <http://ontology.eil.utoronto.ca/CDT#> .
@prefix cityunits: <https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/CityUnits/> .
@prefix code: <https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Code/> .
@prefix genprop: <https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix i72: <http://ontology.eil.utoronto.ca/ISO21972/iso21972#> .
@prefix loc: <https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix tor: <http://ontology.eil.utoronto.ca/Toronto/Toronto#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

"""


# =============================================================================
# BASIC HELPERS
# =============================================================================

def bind_prefixes(graph: Graph) -> None:
    graph.bind("tor", TOR)
    graph.bind("genprop", GENPROP)
    graph.bind("cdt", CDT)
    graph.bind("loc", LOC)
    graph.bind("geo", GEO)
    graph.bind("code", CODE)
    graph.bind("cityunits", CITYUNITS)
    graph.bind("bdg", BDG)
    graph.bind("i72", I72)
    graph.bind("prov", PROV)
    graph.bind("xsd", XSD)


def safe_token(value: str) -> str:
    """Create a conservative URI-local token while preserving useful IDs."""
    value = str(value).strip()
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value)
    return value.strip("_") or "unknown"


def valid_number(value: Any) -> Optional[float]:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def valid_nonnegative_integer(value: Any) -> Optional[int]:
    number = valid_number(value)
    if number is None or number < 0 or not number.is_integer():
        return None
    return int(number)


def primary_name(properties: Dict[str, Any]) -> Optional[str]:
    names = properties.get("names")
    if not isinstance(names, dict):
        return None
    primary = names.get("primary")
    if primary is None:
        return None
    text = str(primary).strip()
    return text or None


def clean_geometry(geometry_json: Any) -> Optional[BaseGeometry]:
    if not isinstance(geometry_json, dict):
        return None
    geometry_type = geometry_json.get("type")
    if geometry_type not in {"Polygon", "MultiPolygon"}:
        return None
    try:
        geom = shape(geometry_json)
    except Exception:
        return None
    if geom.is_empty:
        return None
    if not geom.is_valid:
        try:
            geom = geom.buffer(0)
        except Exception:
            return None
    if geom.is_empty:
        return None
    return geom


# =============================================================================
# INPUT STREAMING
# =============================================================================

def input_kind(path: Path) -> str:
    name = path.name.lower()
    if name.endswith((".geojsonseq", ".geojsonl", ".ndjson", ".jsonl")):
        return "geojsonseq"
    return "geojson"


def iter_geojsonseq(path: Path) -> Iterator[Dict[str, Any]]:
    """Yield one Feature per line from Overture GeoJSONSeq."""
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            text = line.strip()
            if not text:
                continue
            # RFC 8142 JSON text sequences may begin records with ASCII RS.
            if text.startswith("\x1e"):
                text = text[1:]
            try:
                feature = json.loads(text)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on GeoJSONSeq line {line_number}: {exc}"
                ) from exc
            if not isinstance(feature, dict):
                continue
            if feature.get("type") != "Feature":
                continue
            yield feature


def iter_geojson(path: Path) -> Iterator[Dict[str, Any]]:
    """Yield features from an ordinary GeoJSON FeatureCollection."""
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if data.get("type") != "FeatureCollection":
        raise ValueError("GeoJSON input must be a FeatureCollection.")
    features = data.get("features")
    if not isinstance(features, list):
        raise ValueError("GeoJSON FeatureCollection is missing a features list.")
    for feature in features:
        if isinstance(feature, dict) and feature.get("type") == "Feature":
            yield feature


def iter_features(path: Path) -> Iterator[Dict[str, Any]]:
    if input_kind(path) == "geojsonseq":
        yield from iter_geojsonseq(path)
    else:
        yield from iter_geojson(path)


# =============================================================================
# OPTIONAL TORONTO BOUNDARY CLIPPING
# =============================================================================

def load_boundary(path: Path) -> BaseGeometry:
    """
    Load a GeoJSON boundary. If it is a FeatureCollection (for example the
    historical 140 neighbourhoods), union all polygon geometries.
    """
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    geometries = []

    if data.get("type") == "FeatureCollection":
        features = data.get("features") or []
        for feature in features:
            if not isinstance(feature, dict):
                continue
            geom_json = feature.get("geometry")
            if not isinstance(geom_json, dict):
                continue
            try:
                geom = shape(geom_json)
            except Exception:
                continue
            if not geom.is_empty:
                geometries.append(geom)
    elif data.get("type") == "Feature":
        geom_json = data.get("geometry")
        if isinstance(geom_json, dict):
            geometries.append(shape(geom_json))
    elif data.get("type") in {"Polygon", "MultiPolygon"}:
        geometries.append(shape(data))
    else:
        raise ValueError(
            "Boundary must be a Polygon/MultiPolygon GeoJSON geometry, Feature, "
            "or FeatureCollection."
        )

    if not geometries:
        raise ValueError(f"No usable polygon geometry found in boundary file: {path}")

    boundary = unary_union(geometries)
    if not boundary.is_valid:
        boundary = boundary.buffer(0)
    if boundary.is_empty:
        raise ValueError("Boundary union is empty.")
    return boundary


def inside_boundary(geom: BaseGeometry, prepared_boundary) -> bool:
    """Assign a building to Toronto by a point guaranteed inside its footprint."""
    try:
        return prepared_boundary.covers(geom.representative_point())
    except Exception:
        return False


# =============================================================================
# RDF MAPPING
# =============================================================================

def add_geometry(
    graph: Graph,
    building_uri,
    location_uri,
    geom: Optional[BaseGeometry],
) -> bool:
    if geom is None:
        return False
    graph.add((building_uri, LOC.associatedLocation, location_uri))
    graph.add((location_uri, RDF.type, LOC.Location))
    graph.add((location_uri, GEO.asWKT, Literal(geom.wkt, datatype=GEO.wktLiteral)))
    return True


def add_building_use(
    graph: Graph,
    building_uri,
    subtype: Any,
    defined_subtypes: Set[str],
) -> bool:
    """Map one Overture subtype to one shared BuildingUse and Code."""
    if subtype is None:
        return False

    subtype_text = str(subtype).strip()
    if not subtype_text:
        return False

    token = safe_token(subtype_text)
    use_uri = TOR[f"buildingUse_{token}"]
    code_uri = TOR[f"overtureBuildingUseCode_{token}"]

    graph.add((building_uri, BDG.use, use_uri))

    # Define each shared use/code only once in the complete output file.
    if token not in defined_subtypes:
        graph.add((use_uri, RDF.type, BDG.BuildingUse))
        graph.add((use_uri, CODE.hasCode, code_uri))
        graph.add((code_uri, RDF.type, CODE.Code))
        graph.add(
            (
                code_uri,
                GENPROP.hasIdentifier,
                Literal(subtype_text, datatype=XSD.string),
            )
        )
        graph.add(
            (
                code_uri,
                GENPROP.hasName,
                Literal(subtype_text, datatype=XSD.string),
            )
        )
        defined_subtypes.add(token)

    return True


def add_height(graph: Graph, building_uri, building_token: str, value: Any) -> bool:
    height = valid_number(value)
    if height is None or height <= 0:
        return False

    height_uri = TOR[f"building_{building_token}Height"]
    measure_uri = TOR[f"building_{building_token}HeightMeasure"]

    graph.add((building_uri, BDG.hasBuildingHeight, height_uri))
    graph.add((height_uri, RDF.type, CITYUNITS.Length))
    graph.add((height_uri, I72.hasValue, measure_uri))
    graph.add((measure_uri, RDF.type, I72.Measure))
    graph.add(
        (
            measure_uri,
            I72.hasNumericalValue,
            Literal(height, datatype=XSD.double),
        )
    )
    graph.add((measure_uri, I72.hasUnit, I72.metre))
    return True


def add_sources(
    graph: Graph,
    building_uri,
    building_token: str,
    sources: Any,
) -> int:
    """Map Overture source entries to PROV-O entities."""
    if not isinstance(sources, list):
        return 0

    mapped = 0
    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            continue

        source_uri = CDT[f"source_{building_token}_{index}"]
        graph.add((building_uri, PROV.wasDerivedFrom, source_uri))
        graph.add((source_uri, RDF.type, PROV.Entity))

        record_id = source.get("record_id")
        if record_id is not None and str(record_id).strip():
            graph.add(
                (
                    source_uri,
                    GENPROP.hasIdentifier,
                    Literal(str(record_id).strip(), datatype=XSD.string),
                )
            )

        dataset = source.get("dataset")
        if dataset is not None and str(dataset).strip():
            graph.add(
                (
                    source_uri,
                    GENPROP.hasName,
                    Literal(str(dataset).strip(), datatype=XSD.string),
                )
            )

        # update_time intentionally remains unmapped: it is source-record
        # update metadata, not equivalent to PROV generation time.
        mapped += 1

    return mapped


def update_first_canadian_place_check(
    feature_id: str,
    properties: Dict[str, Any],
    stats: Dict[str, Any],
) -> None:
    if feature_id != FIRST_CANADIAN_PLACE_ID:
        return
    stats["fcp_seen"] = True
    stats["fcp_name_ok"] = primary_name(properties) == "First Canadian Place"
    stats["fcp_subtype_ok"] = str(properties.get("subtype", "")).strip() == "commercial"
    stats["fcp_floors_ok"] = valid_nonnegative_integer(properties.get("num_floors")) == 72
    height = valid_number(properties.get("height"))
    stats["fcp_height_ok"] = height is not None and abs(height - 292.0) < 1e-9


def convert_feature(
    graph: Graph,
    feature: Dict[str, Any],
    geom: Optional[BaseGeometry],
    stats: Dict[str, Any],
    defined_subtypes: Set[str],
) -> bool:
    feature_id = feature.get("id")
    if feature_id is None or not str(feature_id).strip():
        stats["skipped_missing_id"] += 1
        return False

    feature_id_text = str(feature_id).strip()
    building_token = safe_token(feature_id_text)
    building_uri = TOR[f"building_{building_token}"]
    location_uri = TOR[f"building_{building_token}Location"]

    properties = feature.get("properties") or {}
    if not isinstance(properties, dict):
        properties = {}

    graph.add((building_uri, RDF.type, BDG.Building))
    graph.add((building_uri, RDF.type, PROV.Entity))
    graph.add(
        (
            building_uri,
            GENPROP.hasIdentifier,
            Literal(feature_id_text, datatype=XSD.string),
        )
    )
    graph.add((building_uri, CDT.locatedInAdministrativeArea, TORONTO_CITY))

    name = primary_name(properties)
    if name:
        graph.add((building_uri, GENPROP.hasName, Literal(name, datatype=XSD.string)))
        stats["with_name"] += 1

    if add_geometry(graph, building_uri, location_uri, geom):
        stats["with_geometry"] += 1

    if add_building_use(
        graph,
        building_uri,
        properties.get("subtype"),
        defined_subtypes,
    ):
        stats["with_subtype"] += 1

    if add_height(graph, building_uri, building_token, properties.get("height")):
        stats["with_height"] += 1

    floors = valid_nonnegative_integer(properties.get("num_floors"))
    if floors is not None:
        graph.add(
            (
                building_uri,
                BDG.numAboveGroundFloors,
                Literal(floors, datatype=XSD.nonNegativeInteger),
            )
        )
        stats["with_num_floors"] += 1

    stats["source_entities"] += add_sources(
        graph,
        building_uri,
        building_token,
        properties.get("sources"),
    )

    # Overture class intentionally remains unmapped.
    update_first_canadian_place_check(feature_id_text, properties, stats)
    stats["mapped_buildings"] += 1
    return True


# =============================================================================
# STREAMING OUTPUT + VALIDATION
# =============================================================================

def empty_stats() -> Dict[str, Any]:
    return {
        "input_features": 0,
        "mapped_buildings": 0,
        "outside_boundary": 0,
        "skipped_missing_id": 0,
        "skipped_no_geometry_for_boundary": 0,
        "with_name": 0,
        "with_geometry": 0,
        "with_subtype": 0,
        "with_height": 0,
        "with_num_floors": 0,
        "source_entities": 0,
        "written_triples": 0,
        "fcp_seen": False,
        "fcp_name_ok": False,
        "fcp_subtype_ok": False,
        "fcp_floors_ok": False,
        "fcp_height_ok": False,
    }


def first_canadian_place_status(stats: Dict[str, Any]) -> str:
    if not stats["fcp_seen"]:
        return "NOT PRESENT / CHECK"
    checks = (
        stats["fcp_name_ok"],
        stats["fcp_subtype_ok"],
        stats["fcp_floors_ok"],
        stats["fcp_height_ok"],
    )
    return "PASS" if all(checks) else "FAIL / CHECK"


def read_state_file(input_path: Path) -> Dict[str, Any]:
    state_path = Path(str(input_path) + ".state")
    if not state_path.exists():
        return {}
    try:
        with state_path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def build_report(
    stats: Dict[str, Any],
    input_path: Path,
    boundary_path: Optional[Path],
    state: Dict[str, Any],
) -> str:
    lines = [
        "Overture Toronto Building Mapping Validation",
        "============================================",
        "",
        f"Input file:                        {input_path.name}",
        f"Input format:                      {input_kind(input_path)}",
    ]

    if state:
        lines += [
            f"Overture release:                  {state.get('last_release', 'unknown')}",
            f"Download bbox:                     {state.get('bbox', 'unknown')}",
        ]

    lines += [
        f"Boundary clipping:                 {boundary_path if boundary_path else 'not used'}",
        "",
        f"Input features processed:          {stats['input_features']}",
        f"Mapped Toronto buildings:          {stats['mapped_buildings']}",
        f"Excluded outside boundary:         {stats['outside_boundary']}",
        f"Skipped missing ID:                {stats['skipped_missing_id']}",
        f"Skipped no geometry for clipping:  {stats['skipped_no_geometry_for_boundary']}",
        f"Buildings with primary name:       {stats['with_name']}",
        f"Buildings with geometry:           {stats['with_geometry']}",
        f"Buildings with subtype/use:        {stats['with_subtype']}",
        f"Buildings with height:             {stats['with_height']}",
        f"Buildings with num_floors:         {stats['with_num_floors']}",
        f"Mapped provenance source entities: {stats['source_entities']}",
        f"Total RDF triples written:         {stats['written_triples']}",
        "",
        "First Canadian Place example:      " + first_canadian_place_status(stats),
    ]

    warnings = []
    if stats["mapped_buildings"] == 0:
        warnings.append("No buildings were mapped.")
    if stats["mapped_buildings"] != stats["with_geometry"]:
        warnings.append(
            "Some mapped buildings do not have geometry / loc:associatedLocation."
        )
    if boundary_path is None and input_kind(input_path) == "geojsonseq":
        warnings.append(
            "No Toronto boundary was supplied. A broad Overture bbox may include "
            "buildings outside the City of Toronto."
        )

    if warnings:
        lines += ["", "WARNINGS", "--------"] + [f"- {w}" for w in warnings]

    return "\n".join(lines)


def flush_graph(graph: Graph, output_handle, stats: Dict[str, Any]) -> None:
    if len(graph) == 0:
        return
    stats["written_triples"] += len(graph)
    # N-Triples is a strict subset of Turtle. Writing it under a single Turtle
    # prefix header allows streaming without holding the complete RDF graph.
    serialized = graph.serialize(format="nt")
    output_handle.write(serialized)
    if not serialized.endswith("\n"):
        output_handle.write("\n")
    output_handle.write("\n")


def convert_streaming(
    input_path: Path,
    output_path: Path,
    report_path: Path,
    boundary_path: Optional[Path],
    chunk_size: int,
    limit: Optional[int],
    progress_every: int,
) -> Dict[str, Any]:
    if chunk_size <= 0:
        raise ValueError("--chunk-size must be greater than 0.")

    prepared_boundary = None
    if boundary_path is not None:
        print(f"Loading Toronto boundary: {boundary_path}")
        boundary = load_boundary(boundary_path)
        prepared_boundary = prep(boundary)
        print("Boundary loaded.")

    stats = empty_stats()
    defined_subtypes: Set[str] = set()
    state = read_state_file(input_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    graph = Graph()
    bind_prefixes(graph)
    mapped_in_chunk = 0

    with output_path.open("w", encoding="utf-8", newline="\n") as output_handle:
        output_handle.write(PREFIX_HEADER)

        for feature in iter_features(input_path):
            if limit is not None and stats["input_features"] >= limit:
                break

            stats["input_features"] += 1
            geom = clean_geometry(feature.get("geometry"))

            if prepared_boundary is not None:
                if geom is None:
                    stats["skipped_no_geometry_for_boundary"] += 1
                    continue
                if not inside_boundary(geom, prepared_boundary):
                    stats["outside_boundary"] += 1
                    continue

            if convert_feature(graph, feature, geom, stats, defined_subtypes):
                mapped_in_chunk += 1

            if mapped_in_chunk >= chunk_size:
                flush_graph(graph, output_handle, stats)
                graph = Graph()
                bind_prefixes(graph)
                mapped_in_chunk = 0

            if progress_every > 0 and stats["input_features"] % progress_every == 0:
                print(
                    f"Processed {stats['input_features']:,} input features; "
                    f"mapped {stats['mapped_buildings']:,}."
                )

        flush_graph(graph, output_handle, stats)

    report = build_report(stats, input_path, boundary_path, state)
    report_path.write_text(report + "\n", encoding="utf-8")

    print("\n" + report)
    print()
    print(f"TTL written to:        {output_path}")
    print(f"Validation written to: {report_path}")
    return stats


# =============================================================================
# CLI
# =============================================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Stream Overture building GeoJSON/GeoJSONSeq into City Digital Twin Turtle."
        )
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Input Overture building .geojson or .geojsonseq file",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("toronto_overture_buildings.ttl"),
        help="Output Turtle file",
    )
    parser.add_argument(
        "--validation",
        type=Path,
        default=Path("toronto_overture_buildings_validation.txt"),
        help="Validation report output file",
    )
    parser.add_argument(
        "--boundary",
        type=Path,
        default=None,
        help=(
            "Optional Toronto boundary GeoJSON. A FeatureCollection such as the "
            "historical 140-neighbourhood file is accepted and unioned."
        ),
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=5000,
        help="Number of mapped buildings per in-memory RDF chunk (default: 5000)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional maximum number of input features to process (useful for testing)",
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=25000,
        help="Print progress every N input features; 0 disables progress output",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Input file not found: {args.input}")
    if args.boundary is not None and not args.boundary.exists():
        raise FileNotFoundError(f"Boundary file not found: {args.boundary}")
    if args.limit is not None and args.limit <= 0:
        raise ValueError("--limit must be greater than 0 when supplied.")

    convert_streaming(
        input_path=args.input,
        output_path=args.output,
        report_path=args.validation,
        boundary_path=args.boundary,
        chunk_size=args.chunk_size,
        limit=args.limit,
        progress_every=args.progress_every,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        sys.exit(1)
