#!/usr/bin/env python3
"""
Rebuild Toronto2.ttl from the legacy graph + original administrative-area sources.

This version is designed to run directly in PyCharm with the folder structure
shown in the project screenshot:

AdministrativeAreas/
├── data/
│   ├── 25-ward-model-december-2018-wgs84-latitude-longitude/
│   ├── community-council-boundaries-data-4326/
│   ├── lct_000a16a_e/
│   ├── neighbourhoods-historical-140-4326/
│   ├── police-boundaries-data-4326/
│   └── neighbourhoods-historical-140-4326.geojson
├── Toronto2.ttl
└── Rebuild_Toronto2_PyCharm.py

WHAT THIS SCRIPT DOES
---------------------
1. Loads the existing Toronto2.ttl as the base graph so content outside the
   administrative-area reconstruction is preserved (for example population
   centres, ontology declarations, and other Toronto geography content).

2. Rebuilds these layers from the public source files:
   - 25 wards
   - historical 140 neighbourhoods
   - 2016 Toronto census tracts

3. Recreates the historical ward-neighbourhood links from Toronto2.ttl because
   the source ward/neighbourhood files do not directly contain that crosswalk.

4. Recreates census-tract -> neighbourhood membership spatially from the source
   geometries.

5. Applies known corrections:
   - current ISO SpatialLoc namespace
   - genprop:hasName for ward/neighbourhood/census labels
   - Toronto -> neighbourhood links
   - ISO 5087-2 city:administrativeAreaOf for wards, neighbourhoods, and census tracts
   - ward WKT regenerated from the source dataset
   - census geometries reprojected to EPSG:4326
   - safe census-tract URIs built from the real CTUID

6. Preserves the legacy PoliceDivision, CommunityCouncil, and PopulationCentre
   content for now. The current police source is not used to replace the legacy
   police layer because the current Toronto Police boundary model differs from
   the 17-division historical model represented in Toronto2.ttl.

7. Migrates any remaining legacy SpatialLoc URIs in the graph to the current
   ISO SpatialLoc namespace.

OUTPUTS
-------
Toronto2_rebuilt.ttl
Toronto2_rebuilt_validation.txt

INSTALL ONCE
------------
In the PyCharm terminal:

    pip install geopandas rdflib shapely pyproj

Then right-click this file and choose Run.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

try:
    import geopandas as gpd
    from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
    from rdflib.namespace import OWL
    from shapely import wkt as shapely_wkt
    from shapely.geometry.base import BaseGeometry
except ImportError as exc:
    print("\nMissing Python package:", exc)
    print("\nInstall the required packages in the PyCharm terminal:")
    print("pip install geopandas rdflib shapely pyproj\n")
    raise


# =============================================================================
# PROJECT PATHS
# =============================================================================

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"

LEGACY_TTL = PROJECT_DIR / "Toronto2.ttl"

WARD_DIR = DATA_DIR / "25-ward-model-december-2018-wgs84-latitude-longitude"
NEIGHBOURHOOD_DIR = DATA_DIR / "neighbourhoods-historical-140-4326"
NEIGHBOURHOOD_GEOJSON = DATA_DIR / "neighbourhoods-historical-140-4326.geojson"
CENSUS_DIR = DATA_DIR / "lct_000a16a_e"

# These are currently used for validation/reporting only.
COMMUNITY_COUNCIL_DIR = DATA_DIR / "community-council-boundaries-data-4326"
POLICE_DIR = DATA_DIR / "police-boundaries-data-4326"

OUTPUT_TTL = PROJECT_DIR / "Toronto2_rebuilt.ttl"
OUTPUT_VALIDATION = PROJECT_DIR / "Toronto2_rebuilt_validation.txt"


# =============================================================================
# NAMESPACES
# =============================================================================

COT = Namespace("http://ontology.eil.utoronto.ca/Toronto/Toronto#")
CACENSUS = Namespace("http://ontology.eil.utoronto.ca/tove/cacensus#")

OLD_LOC = Namespace("http://ontology.eil.utoronto.ca/5087/1/SpatialLoc/")
LOC = Namespace(
    "https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/"
)
GENPROP = Namespace(
    "https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/"
)
CITY = Namespace(
    "https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/City/"
)
GEO = Namespace("http://www.opengis.net/ont/geosparql#")


# =============================================================================
# SETTINGS
# =============================================================================

OUTPUT_CRS = "EPSG:4326"
ANALYSIS_CRS = "EPSG:26917"   # NAD83 / UTM Zone 17N
TORONTO_CMAUID = "535"

# This value reproduced the 572 Toronto census tracts in earlier validation.
CT_MIN_CITY_OVERLAP = 0.05


# =============================================================================
# FILE HELPERS
# =============================================================================

def find_shapefile(folder: Path, preferred_text: str = "") -> Path:
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found:\n{folder}")

    shp_files = sorted(folder.rglob("*.shp"))
    if not shp_files:
        raise FileNotFoundError(f"No .shp file found inside:\n{folder}")

    if preferred_text:
        preferred = [
            p for p in shp_files
            if preferred_text.lower() in p.stem.lower()
        ]
        if preferred:
            return preferred[0]

    return shp_files[0]


def find_neighbourhood_file() -> Path:
    if NEIGHBOURHOOD_GEOJSON.exists():
        return NEIGHBOURHOOD_GEOJSON
    return find_shapefile(NEIGHBOURHOOD_DIR, "historical 140")


def optional_source_count(folder: Path) -> Optional[int]:
    """Return row count for an optional shapefile source, or None."""
    if not folder.exists():
        return None

    shp_files = sorted(folder.rglob("*.shp"))
    if not shp_files:
        return None

    try:
        return len(gpd.read_file(shp_files[0]))
    except Exception:
        return None


# =============================================================================
# RDF / GEOMETRY HELPERS
# =============================================================================

def bind_prefixes(graph: Graph) -> None:
    graph.bind("cot", COT)
    graph.bind("census", CACENSUS)
    graph.bind("loc", LOC)
    graph.bind("genprop", GENPROP)
    graph.bind("city", CITY)
    graph.bind("geo", GEO)
    graph.bind("owl", OWL)
    graph.bind("rdfs", RDFS)


def clean_geometry(geom: BaseGeometry) -> BaseGeometry:
    if geom is None or geom.is_empty:
        return geom
    if not geom.is_valid:
        geom = geom.buffer(0)
    return geom


def wkt_literal(geom: BaseGeometry) -> Literal:
    text = shapely_wkt.dumps(
        geom,
        rounding_precision=15,
        trim=True,
    )
    return Literal(text, datatype=GEO.wktLiteral)


def add_location(
    graph: Graph,
    subject: URIRef,
    location: URIRef,
    geom: BaseGeometry,
) -> None:
    graph.add((subject, LOC.hasLocation, location))
    graph.add((location, RDF.type, LOC.Location))
    graph.add((location, RDF.type, OWL.NamedIndividual))
    graph.add((location, GEO.asWKT, wkt_literal(geom)))


def remove_resource_completely(graph: Graph, resource: URIRef) -> None:
    """Remove triples where resource is subject or object."""
    graph.remove((resource, None, None))
    graph.remove((None, None, resource))


def migrate_old_spatialloc_namespace(graph: Graph) -> int:
    """
    Replace URIRefs beginning with the old SpatialLoc namespace by the
    corresponding URI in the current ISO SpatialLoc namespace.
    """
    old_prefix = str(OLD_LOC)
    new_prefix = str(LOC)

    replacements = []

    for s, p, o in list(graph):
        new_s = s
        new_p = p
        new_o = o

        if isinstance(s, URIRef) and str(s).startswith(old_prefix):
            new_s = URIRef(new_prefix + str(s)[len(old_prefix):])

        if isinstance(p, URIRef) and str(p).startswith(old_prefix):
            new_p = URIRef(new_prefix + str(p)[len(old_prefix):])

        if isinstance(o, URIRef) and str(o).startswith(old_prefix):
            new_o = URIRef(new_prefix + str(o)[len(old_prefix):])

        if (new_s, new_p, new_o) != (s, p, o):
            replacements.append(((s, p, o), (new_s, new_p, new_o)))

    for old_triple, new_triple in replacements:
        graph.remove(old_triple)
        graph.add(new_triple)

    return len(replacements)


# =============================================================================
# LOAD SOURCE DATA
# =============================================================================

def load_sources():
    ward_file = find_shapefile(WARD_DIR, "WARD_WGS84")
    neighbourhood_file = find_neighbourhood_file()
    census_file = find_shapefile(CENSUS_DIR, "lct_000a16a_e")

    print("Source files")
    print("------------")
    print("Wards:         ", ward_file)
    print("Neighbourhoods:", neighbourhood_file)
    print("Census tracts: ", census_file)

    wards = gpd.read_file(ward_file)
    neighbourhoods = gpd.read_file(neighbourhood_file)
    census = gpd.read_file(census_file)

    # Normalize neighbourhood column names. GeoJSON and Shapefile versions
    # can use different field names because of DBF truncation.
    rename_map = {}
    if "AREA_SHORT_CODE" in neighbourhoods.columns:
        rename_map["AREA_SHORT_CODE"] = "AREA_SH5"
    if "AREA_NAME" in neighbourhoods.columns:
        rename_map["AREA_NAME"] = "AREA_NA7"

    neighbourhoods = neighbourhoods.rename(columns=rename_map)

    required_ward = {"AREA_S_CD", "AREA_NAME", "geometry"}
    required_neighbourhood = {"AREA_SH5", "AREA_NA7", "geometry"}
    required_census = {"CTUID", "CMAUID", "geometry"}

    checks = [
        ("ward", wards, required_ward),
        ("neighbourhood", neighbourhoods, required_neighbourhood),
        ("census tract", census, required_census),
    ]

    for source_name, frame, required in checks:
        missing = required - set(frame.columns)
        if missing:
            raise KeyError(
                f"{source_name} source is missing fields: {sorted(missing)}\n"
                f"Available fields: {list(frame.columns)}"
            )

    wards = wards.to_crs(OUTPUT_CRS)
    neighbourhoods = neighbourhoods.to_crs(OUTPUT_CRS)
    census = census.to_crs(OUTPUT_CRS)

    wards["geometry"] = wards.geometry.map(clean_geometry)
    neighbourhoods["geometry"] = neighbourhoods.geometry.map(clean_geometry)
    census["geometry"] = census.geometry.map(clean_geometry)

    return wards, neighbourhoods, census


# =============================================================================
# LEGACY RELATIONSHIP EXTRACTION
# =============================================================================

def extract_legacy_ward_neighbourhood_pairs(
    legacy_graph: Graph,
) -> Set[Tuple[int, int]]:
    """
    Recover exact historical neighbourhood->ward links from Toronto2.ttl.
    """
    pairs: Set[Tuple[int, int]] = set()

    for neighbourhood in legacy_graph.subjects(RDF.type, COT.Neighborhood):
        n_match = re.search(r"neighborhood(\d+)$", str(neighbourhood))
        if not n_match:
            continue

        neighbourhood_id = int(n_match.group(1))

        for ward in legacy_graph.objects(neighbourhood, COT.inWard):
            w_match = re.search(r"ward(\d+)$", str(ward))
            if w_match:
                pairs.add((neighbourhood_id, int(w_match.group(1))))

    return pairs


# =============================================================================
# CENSUS TRACT SELECTION + NEIGHBOURHOOD ASSIGNMENT
# =============================================================================

def prepare_census_tracts(
    census: gpd.GeoDataFrame,
    neighbourhoods: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """
    Keep Toronto CMA tracts that spatially overlap Toronto's historical
    neighbourhood geography, then assign each tract to the neighbourhood
    with the largest intersection area.
    """
    census = census[
        census["CMAUID"].astype(str) == TORONTO_CMAUID
    ].copy()

    census["CTUID"] = census["CTUID"].astype(str)

    census_proj = census.to_crs(ANALYSIS_CRS).copy()
    neighbourhoods_proj = neighbourhoods.to_crs(ANALYSIS_CRS).copy()

    neighbourhoods_proj["_nid"] = (
        neighbourhoods_proj["AREA_SH5"].astype(str).astype(int)
    )

    city_union = neighbourhoods_proj.geometry.union_all()

    keep_indices: List[int] = []
    assigned_neighbourhood: Dict[int, int] = {}

    for idx, row in census_proj.iterrows():
        tract_geom = clean_geometry(row.geometry)

        if (
            tract_geom is None
            or tract_geom.is_empty
            or tract_geom.area == 0
        ):
            continue

        city_overlap = (
            tract_geom.intersection(city_union).area
            / tract_geom.area
        )

        if city_overlap < CT_MIN_CITY_OVERLAP:
            continue

        candidate_positions = list(
            neighbourhoods_proj.sindex.query(
                tract_geom,
                predicate="intersects",
            )
        )

        candidates = neighbourhoods_proj.iloc[candidate_positions]

        best_nid: Optional[int] = None
        best_area = -1.0

        for _, nrow in candidates.iterrows():
            overlap_area = tract_geom.intersection(
                clean_geometry(nrow.geometry)
            ).area

            if overlap_area > best_area:
                best_area = overlap_area
                best_nid = int(nrow["_nid"])

        if best_nid is None or best_area <= 0:
            continue

        keep_indices.append(idx)
        assigned_neighbourhood[idx] = best_nid

    selected = census.loc[keep_indices].copy()
    selected["_neighbourhood_id"] = [
        assigned_neighbourhood[idx]
        for idx in selected.index
    ]

    return selected


# =============================================================================
# REMOVE OLD ADMIN-AREA INSTANCES FROM BASE GRAPH
# =============================================================================

def remove_old_admin_instances(graph: Graph) -> Dict[str, int]:
    """
    Remove old Ward, Neighborhood, and CensusTract individuals plus their
    location nodes. Class/property/schema declarations are preserved.
    """
    targets = {
        "wards": set(graph.subjects(RDF.type, COT.Ward)),
        "neighbourhoods": set(
            graph.subjects(RDF.type, COT.Neighborhood)
        ),
        "census_tracts": set(
            graph.subjects(RDF.type, CACENSUS.CensusTract)
        ),
    }

    all_entities = set().union(*targets.values())
    locations: Set[URIRef] = set()

    for entity in all_entities:
        for loc in graph.objects(entity, OLD_LOC.hasLocation):
            if isinstance(loc, URIRef):
                locations.add(loc)
        for loc in graph.objects(entity, LOC.hasLocation):
            if isinstance(loc, URIRef):
                locations.add(loc)

    for resource in all_entities | locations:
        remove_resource_completely(graph, resource)

    # Remove city links that may remain after entity deletion.
    for predicate in (
        COT.hasWard,
        COT.hasNeighbourhood,
        COT.hasCensusTract,
    ):
        graph.remove((COT.toronto, predicate, None))

    return {
        "old_wards_removed": len(targets["wards"]),
        "old_neighbourhoods_removed": len(targets["neighbourhoods"]),
        "old_census_tracts_removed": len(targets["census_tracts"]),
        "old_locations_removed": len(locations),
    }


# =============================================================================
# ADD REBUILT ADMIN-AREA CONTENT
# =============================================================================

def add_rebuilt_admin_areas(
    graph: Graph,
    wards: gpd.GeoDataFrame,
    neighbourhoods: gpd.GeoDataFrame,
    census_tracts: gpd.GeoDataFrame,
    ward_neighbourhood_pairs: Set[Tuple[int, int]],
) -> None:

    toronto = COT.toronto

    # Make sure Toronto has a readable name.
    graph.add((toronto, GENPROP.hasName, Literal("Toronto")))

    # -------------------------------------------------------------------------
    # WARDS
    # -------------------------------------------------------------------------
    for _, row in wards.sort_values("AREA_S_CD").iterrows():
        ward_id = int(str(row["AREA_S_CD"]))
        ward = COT[f"ward{ward_id}"]
        location = COT[f"ward{ward_id}Location"]

        graph.add((ward, RDF.type, COT.Ward))
        graph.add((ward, RDF.type, OWL.NamedIndividual))
        graph.add(
            (ward, GENPROP.hasName, Literal(str(row["AREA_NAME"])))
        )
        graph.add(
            (ward, GENPROP.hasIdentifier, Literal(str(row["AREA_S_CD"])))
        )
        # Preserve the legacy Toronto-specific relationship and also use the
        # ISO 5087-2 administrative-area relationship for new mappings.
        graph.add((ward, COT.inCity, toronto))
        graph.add((ward, CITY.administrativeAreaOf, toronto))
        graph.add((toronto, COT.hasWard, ward))

        add_location(graph, ward, location, row.geometry)

    # -------------------------------------------------------------------------
    # NEIGHBOURHOODS
    # -------------------------------------------------------------------------
    for _, row in neighbourhoods.sort_values("AREA_SH5").iterrows():
        neighbourhood_id = int(str(row["AREA_SH5"]))
        neighbourhood = COT[f"neighborhood{neighbourhood_id}"]
        location = COT[f"neighborhood{neighbourhood_id}Location"]

        raw_name = str(row["AREA_NA7"])
        clean_name = re.sub(r"\s*\(\d+\)\s*$", "", raw_name).strip()

        graph.add((neighbourhood, RDF.type, COT.Neighborhood))
        graph.add((neighbourhood, RDF.type, OWL.NamedIndividual))
        graph.add(
            (neighbourhood, GENPROP.hasName, Literal(clean_name))
        )
        graph.add(
            (
                neighbourhood,
                GENPROP.hasIdentifier,
                Literal(str(row["AREA_SH5"])),
            )
        )

        # Preserve the existing Toronto-specific relationship and add the
        # uniform ISO 5087-2 administrative-area -> city relationship.
        graph.add((toronto, COT.hasNeighbourhood, neighbourhood))
        graph.add((neighbourhood, CITY.administrativeAreaOf, toronto))

        add_location(
            graph,
            neighbourhood,
            location,
            row.geometry,
        )

    # -------------------------------------------------------------------------
    # HISTORICAL WARD <-> NEIGHBOURHOOD CROSSWALK
    # -------------------------------------------------------------------------
    for neighbourhood_id, ward_id in sorted(
        ward_neighbourhood_pairs
    ):
        neighbourhood = COT[f"neighborhood{neighbourhood_id}"]
        ward = COT[f"ward{ward_id}"]

        graph.add((neighbourhood, COT.inWard, ward))
        graph.add((ward, COT.hasNeighbourhood, neighbourhood))

    # -------------------------------------------------------------------------
    # CENSUS TRACTS
    # -------------------------------------------------------------------------
    for _, row in census_tracts.sort_values("CTUID").iterrows():
        ctuid = str(row["CTUID"])

        # Avoid malformed URIs and preserve the true identifier separately.
        uri_id = ctuid.replace(".", "-")

        tract = COT[f"ct-{uri_id}"]
        location = COT[f"ct-{uri_id}Location"]

        neighbourhood_id = int(row["_neighbourhood_id"])
        neighbourhood = COT[f"neighborhood{neighbourhood_id}"]

        graph.add((tract, RDF.type, CACENSUS.CensusTract))
        graph.add((tract, RDF.type, OWL.NamedIndividual))
        graph.add(
            (tract, GENPROP.hasName, Literal(f"Census Tract {ctuid}"))
        )
        graph.add((tract, GENPROP.hasIdentifier, Literal(ctuid)))

        graph.add((tract, COT.inNeighbourhood, neighbourhood))
        graph.add((tract, CITY.administrativeAreaOf, toronto))
        graph.add((neighbourhood, COT.hasCensusTract, tract))

        add_location(graph, tract, location, row.geometry)


# =============================================================================
# SMALL CORRECTIONS TO PRESERVED LEGACY LAYERS
# =============================================================================

def add_names_to_preserved_layers(graph: Graph) -> Dict[str, int]:
    """
    Preserve legacy PoliceDivision / CommunityCouncil / PopulationCentre data,
    but add genprop:hasName where a readable name is already available or can be
    safely recovered from the legacy URI.
    """
    added_police_names = 0
    added_council_names = 0
    added_population_centre_names = 0

    # Police division old graph used rdfs:comment as the label.
    for division in graph.subjects(RDF.type, COT.PoliceDivision):
        if any(graph.objects(division, GENPROP.hasName)):
            continue

        comments = list(graph.objects(division, RDFS.comment))
        if comments:
            graph.add((division, GENPROP.hasName, comments[0]))
            added_police_names += 1

    council_names = {
        COT.etobicokeYorkCommunityCouncil: "Etobicoke York Community Council",
        COT.northYorkCommunityCouncil: "North York Community Council",
        COT.scarboroughCommunityCouncil: "Scarborough Community Council",
        COT.torontoEastYorkCommunityCouncil:
            "Toronto and East York Community Council",
    }

    for council, name in council_names.items():
        if (council, RDF.type, COT.CommunityCouncil) in graph:
            if not any(graph.objects(council, GENPROP.hasName)):
                graph.add((council, GENPROP.hasName, Literal(name)))
                added_council_names += 1

    # Population centres are preserved from the legacy graph. Reuse an
    # existing human-readable label/comment when available rather than
    # inventing a new name from the URI.
    for centre in graph.subjects(RDF.type, CACENSUS.PopulationCentre):
        if any(graph.objects(centre, GENPROP.hasName)):
            continue

        labels = list(graph.objects(centre, RDFS.label))
        comments = list(graph.objects(centre, RDFS.comment))
        candidates = labels + comments

        readable_name = next(
            (
                value for value in candidates
                if isinstance(value, Literal) and str(value).strip()
            ),
            None,
        )

        if readable_name is not None:
            graph.add((centre, GENPROP.hasName, readable_name))
            added_population_centre_names += 1

    return {
        "police_names_added": added_police_names,
        "community_council_names_added": added_council_names,
        "population_centre_names_added": added_population_centre_names,
    }


# =============================================================================
# VALIDATION
# =============================================================================

def count_type(graph: Graph, rdf_type: URIRef) -> int:
    return len(set(graph.subjects(RDF.type, rdf_type)))


def count_named_type(graph: Graph, rdf_type: URIRef) -> int:
    """Count typed individuals that have at least one genprop:hasName."""
    return len({
        subject
        for subject in graph.subjects(RDF.type, rdf_type)
        if any(graph.objects(subject, GENPROP.hasName))
    })


def count_admin_areas_in_toronto(graph: Graph, rdf_type: URIRef) -> int:
    """
    Count typed administrative-area individuals explicitly associated with
    Toronto using ISO 5087-2 city:administrativeAreaOf.
    """
    return len({
        subject
        for subject in graph.subjects(RDF.type, rdf_type)
        if (subject, CITY.administrativeAreaOf, COT.toronto) in graph
    })


def count_old_spatialloc_uris(graph: Graph) -> int:
    old_prefix = str(OLD_LOC)
    count = 0

    for s, p, o in graph:
        terms = (s, p, o)
        if any(
            isinstance(term, URIRef)
            and str(term).startswith(old_prefix)
            for term in terms
        ):
            count += 1

    return count


def build_validation_report(
    graph: Graph,
    source_counts: Dict[str, int],
    removal_stats: Dict[str, int],
    correction_stats: Dict[str, int],
    spatialloc_replacements: int,
    community_source_rows: Optional[int],
    police_source_rows: Optional[int],
) -> str:

    ward_count = count_type(graph, COT.Ward)
    neighbourhood_count = count_type(graph, COT.Neighborhood)
    census_count = count_type(graph, CACENSUS.CensusTract)
    police_count = count_type(graph, COT.PoliceDivision)
    council_count = count_type(graph, COT.CommunityCouncil)
    popcentre_count = count_type(graph, CACENSUS.PopulationCentre)

    ward_named_count = count_named_type(graph, COT.Ward)
    neighbourhood_named_count = count_named_type(graph, COT.Neighborhood)
    census_named_count = count_named_type(graph, CACENSUS.CensusTract)
    police_named_count = count_named_type(graph, COT.PoliceDivision)
    council_named_count = count_named_type(graph, COT.CommunityCouncil)
    popcentre_named_count = count_named_type(graph, CACENSUS.PopulationCentre)

    ward_city_count = count_admin_areas_in_toronto(graph, COT.Ward)
    neighbourhood_city_count = count_admin_areas_in_toronto(
        graph,
        COT.Neighborhood,
    )
    census_city_count = count_admin_areas_in_toronto(
        graph,
        CACENSUS.CensusTract,
    )

    toronto_neighbourhood_count = len(
        set(graph.objects(COT.toronto, COT.hasNeighbourhood))
    )

    ward_neighbourhood_count = len(
        list(graph.triples((None, COT.inWard, None)))
    )

    ct_neighbourhood_count = len(
        list(graph.triples((None, COT.inNeighbourhood, None)))
    )

    lines = [
        "Toronto2 Rebuild Validation",
        "===========================",
        "",
        "Generated entity counts",
        "-----------------------",
        f"Wards:                         {ward_count}",
        f"Neighbourhoods:                {neighbourhood_count}",
        f"Census tracts:                 {census_count}",
        f"Police divisions (preserved):  {police_count}",
        f"Community councils (preserved):{council_count}",
        f"Population centres (preserved):{popcentre_count}",
        "",
        "genprop:hasName coverage",
        "------------------------",
        f"Wards with names:                {ward_named_count}/{ward_count}",
        f"Neighbourhoods with names:       {neighbourhood_named_count}/{neighbourhood_count}",
        f"Census tracts with names:        {census_named_count}/{census_count}",
        f"Police divisions with names:     {police_named_count}/{police_count}",
        f"Community councils with names:   {council_named_count}/{council_count}",
        f"Population centres with names:   {popcentre_named_count}/{popcentre_count}",
        "",
        "ISO 5087-2 administrativeAreaOf coverage",
        "-----------------------------------------",
        f"Wards -> Toronto:                  {ward_city_count}/{ward_count}",
        f"Neighbourhoods -> Toronto:         {neighbourhood_city_count}/{neighbourhood_count}",
        f"Census tracts -> Toronto:          {census_city_count}/{census_count}",
        "",
        "Relationship counts",
        "-------------------",
        f"Toronto -> neighbourhood:       {toronto_neighbourhood_count}",
        f"Neighbourhood -> ward:          {ward_neighbourhood_count}",
        f"Census tract -> neighbourhood:  {ct_neighbourhood_count}",
        "",
        "Public source row counts used",
        "-----------------------------",
        f"Ward source rows:               {source_counts['wards']}",
        f"Neighbourhood source rows:      {source_counts['neighbourhoods']}",
        f"Selected Toronto CT rows:       {source_counts['census_tracts']}",
        "",
        "Legacy replacement stats",
        "------------------------",
        f"Old wards removed:              {removal_stats['old_wards_removed']}",
        f"Old neighbourhoods removed:     {removal_stats['old_neighbourhoods_removed']}",
        f"Old census tracts removed:      {removal_stats['old_census_tracts_removed']}",
        f"Old location nodes removed:     {removal_stats['old_locations_removed']}",
        "",
        "Corrections",
        "-----------",
        f"SpatialLoc triples remapped:    {spatialloc_replacements}",
        f"Remaining old SpatialLoc triples:{count_old_spatialloc_uris(graph)}",
        f"Police genprop names added:     {correction_stats['police_names_added']}",
        f"Council genprop names added:    {correction_stats['community_council_names_added']}",
        f"Population centre names added:  {correction_stats['population_centre_names_added']}",
        "",
        "Optional source folders detected",
        "--------------------------------",
        f"Community council source rows:  {community_source_rows}",
        f"Current police source rows:     {police_source_rows}",
        "",
        "Important notes",
        "---------------",
        "- Ward, neighbourhood, and census-tract instances were regenerated",
        "  from the public source datasets.",
        "- Historical ward-neighbourhood membership was recovered from Toronto2.ttl",
        "  because the public source files do not directly encode that crosswalk.",
        "- Police divisions are preserved from Toronto2.ttl for now because the",
        "  current public police-boundary dataset represents a newer division model",
        "  than the historical 17-division model in Toronto2.ttl.",
        "- Population centres are preserved from Toronto2.ttl because the 2016",
        "  Population Centre source file is not present in the current project folder.",
        "- Community councils are preserved from Toronto2.ttl for compatibility;",
        "  the public source folder is detected for later full regeneration.",
        "",
        "Expected historical counts",
        "--------------------------",
        "25 wards",
        "140 neighbourhoods",
        "572 census tracts",
        "17 police divisions",
        "4 community councils",
        "23 population centres",
    ]

    warnings = []

    if ward_count != 25:
        warnings.append(f"Expected 25 wards, found {ward_count}.")
    if neighbourhood_count != 140:
        warnings.append(
            f"Expected 140 neighbourhoods, found {neighbourhood_count}."
        )
    if census_count != 572:
        warnings.append(
            f"Expected 572 census tracts, found {census_count}."
        )
    if police_count != 17:
        warnings.append(
            f"Legacy Toronto2 expected 17 police divisions, found {police_count}."
        )
    if council_count != 4:
        warnings.append(
            f"Expected 4 community councils, found {council_count}."
        )
    if popcentre_count != 23:
        warnings.append(
            f"Expected 23 population centres, found {popcentre_count}."
        )

    admin_area_city_checks = [
        ("wards", ward_count, ward_city_count),
        ("neighbourhoods", neighbourhood_count, neighbourhood_city_count),
        ("census tracts", census_count, census_city_count),
    ]
    for label, total, associated in admin_area_city_checks:
        if associated != total:
            warnings.append(
                f"Only {associated} of {total} {label} use "
                "city:administrativeAreaOf tor:toronto."
            )

    name_checks = [
        ("wards", ward_count, ward_named_count),
        ("neighbourhoods", neighbourhood_count, neighbourhood_named_count),
        ("census tracts", census_count, census_named_count),
        ("police divisions", police_count, police_named_count),
        ("community councils", council_count, council_named_count),
        ("population centres", popcentre_count, popcentre_named_count),
    ]
    for label, total, named in name_checks:
        if named != total:
            warnings.append(
                f"Only {named} of {total} {label} have genprop:hasName."
            )

    if count_old_spatialloc_uris(graph) != 0:
        warnings.append(
            "Some old SpatialLoc namespace URIs remain."
        )

    if warnings:
        lines += ["", "WARNINGS", "--------"] + [
            f"- {warning}" for warning in warnings
        ]
    else:
        lines += [
            "",
            "All expected historical entity counts were reproduced.",
        ]

    lines += [
        "",
        f"Total RDF triples: {len(graph)}",
    ]

    return "\n".join(lines)


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    print("\nToronto2 Geography Rebuilder")
    print("============================\n")
    print("Project folder:", PROJECT_DIR)

    if not LEGACY_TTL.exists():
        raise FileNotFoundError(
            f"Toronto2.ttl was not found here:\n{LEGACY_TTL}\n\n"
            "Place Toronto2.ttl in the same folder as this script."
        )

    if not DATA_DIR.exists():
        raise FileNotFoundError(
            f"Data folder not found:\n{DATA_DIR}"
        )

    print("\nLoading legacy Toronto2.ttl...")
    graph = Graph()
    graph.parse(LEGACY_TTL, format="turtle")
    bind_prefixes(graph)

    # Separate reference graph so we can extract the historical crosswalk before
    # removing old admin-area instances.
    legacy_reference = Graph()
    legacy_reference.parse(LEGACY_TTL, format="turtle")

    print("Legacy graph triples:", len(graph))

    print("\nLoading public source data...")
    wards, neighbourhoods, census = load_sources()

    print("\nPreparing Toronto census tracts...")
    selected_census = prepare_census_tracts(
        census,
        neighbourhoods,
    )
    print("Selected Toronto census tracts:", len(selected_census))

    print("\nRecovering historical ward-neighbourhood links...")
    ward_neighbourhood_pairs = (
        extract_legacy_ward_neighbourhood_pairs(
            legacy_reference
        )
    )
    print(
        "Historical ward-neighbourhood links:",
        len(ward_neighbourhood_pairs),
    )

    print("\nRemoving old ward/neighbourhood/census instances...")
    removal_stats = remove_old_admin_instances(graph)

    print("Rebuilding administrative-area content...")
    add_rebuilt_admin_areas(
        graph,
        wards,
        neighbourhoods,
        selected_census,
        ward_neighbourhood_pairs,
    )

    print("Adding corrected names to preserved layers...")
    correction_stats = add_names_to_preserved_layers(graph)

    print("Migrating old SpatialLoc namespace...")
    spatialloc_replacements = migrate_old_spatialloc_namespace(graph)

    # Rebind prefixes after namespace migration.
    bind_prefixes(graph)

    community_source_rows = optional_source_count(
        COMMUNITY_COUNCIL_DIR
    )
    police_source_rows = optional_source_count(POLICE_DIR)

    source_counts = {
        "wards": len(wards),
        "neighbourhoods": len(neighbourhoods),
        "census_tracts": len(selected_census),
    }

    print("\nWriting rebuilt Turtle file...")
    graph.serialize(
        destination=OUTPUT_TTL,
        format="turtle",
    )

    report = build_validation_report(
        graph=graph,
        source_counts=source_counts,
        removal_stats=removal_stats,
        correction_stats=correction_stats,
        spatialloc_replacements=spatialloc_replacements,
        community_source_rows=community_source_rows,
        police_source_rows=police_source_rows,
    )

    OUTPUT_VALIDATION.write_text(
        report,
        encoding="utf-8",
    )

    print("\n" + report)

    print("\nFiles created")
    print("-------------")
    print("TTL:       ", OUTPUT_TTL)
    print("Validation:", OUTPUT_VALIDATION)
    print("\nDone.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("\nERROR")
        print("-----")
        print(exc)
        print(
            "\nThe script stopped before producing a complete output."
        )
        sys.exit(1)
