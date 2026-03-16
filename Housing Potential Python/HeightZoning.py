import pandas as pd
import json
import re
from shapely.geometry import shape
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD
from shapely.geometry import shape
from shapely import to_wkt, is_valid, make_valid

df = pd.read_csv("zoning-height-overlay-4326.csv")

TOR = Namespace("http://ontology.eil.utoronto.ca/Toronto/Toronto#")
HP  = Namespace("http://ontology.eil.utoronto.ca/HPCDM/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
gen = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/")

LOC = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/")
I72 = Namespace("http://ontology.eil.utoronto.ca/ISO21972/iso21972#")

g = Graph()
g.bind("tor", TOR)
g.bind("hp", HP)
g.bind("geo", GEO)
g.bind("loc", LOC)
g.bind("i72", I72)

ZBL = TOR["zoning_by-law_569-2013"]

# -------- helpers --------

def to_decimal(val):
    if pd.isna(val):
        return None
    # HT_LABEL can be "12", 12.0, "12 m", etc.
    m = re.search(r"[-+]?\d*\.?\d+", str(val))
    return None if not m else m.group(0)



height_var = HP["hasBuildingHeight"]

g.add((TOR.BuildingPopulation, RDFS.subClassOf, I72.Population))

for _, row in df.iterrows():
    zid = row.get('_id')
    ht  = to_decimal(row.get('HT_LABEL'))
    wkt = None
    geom_col = row.get("geometry")

    if geom_col:
        try:
            geom_dict = json.loads(geom_col)
            geom_obj = shape(geom_dict)

            if not is_valid(geom_obj):
                geom_obj = make_valid(geom_obj)

            if not geom_obj.is_empty:
                wkt = to_wkt(geom_obj, rounding_precision=-1)
        except Exception as e:
            print(f"Skipping geometry for _id={zid}: {e}")


    if not zid or ht is None or wkt is None:
        continue


    # URIs from the mapping
    zone_uri       = TOR[f"height_zone{zid}"]
    area_uri       = TOR[f"height_zone{zid}Area"]
    area_loc_uri   = TOR[f"height_zone{zid}AreaLoc"]
    cons_uri       = TOR[f"height_zone{zid}HeightConstraint"]
    cons_val_uri   = TOR[f"height_zone{zid}HeightConstraintValue"]
    max_uri        = TOR[f"height_zone{zid}MaxHeight"]
    build        = TOR[f"height_zone{zid}BuildingHeight"]
    pop_in_zone    = TOR[f"buildingPopulationHeightZone{zid}"]

    # tor:height_zone_{id} rdf:type hp:Regulation ; hp:definedIn zoning bylaw ; hp:definedFor Area ; hp:specifiesConstraint HeightConstraint
    g.add((zone_uri, RDF.type, HP.Regulation))
    g.add((zone_uri, gen.hasName, Literal(f"Height regulation {zid}", datatype=XSD.string)))

    g.add((ZBL,HP.definesRegulation, zone_uri))
    g.add((zone_uri, HP.definedFor, area_uri))
    g.add((zone_uri, HP.specifiesConstraint, cons_uri))

    # Area + location + WKT
    g.add((area_uri, RDF.type, HP.AdministrativeArea))
    g.add((area_uri, LOC.hasLocation, area_loc_uri))
    g.add((area_loc_uri, GEO.asWKT, Literal(wkt, datatype=GEO.wktLiteral)))

    # Height constraint: QuantityAllowance -> hasValue -> NumericalValue (metres)
    g.add((cons_uri, RDF.type, HP.QuantityAllowance))
    g.add((cons_uri, I72.hasValue, cons_val_uri))
    g.add((cons_val_uri, I72.hasNumericalValue, Literal(ht, datatype=XSD.decimal)))
    g.add((cons_val_uri, I72.hasUnit, I72.metre))

    # Maximum structure
    g.add((cons_uri, HP.specifiesMaximumFor, max_uri))
    g.add((max_uri, RDF.type, HP.Maximum))
    g.add((max_uri, HP.maximumOf, pop_in_zone))

    # population-in-zone typing (as in your mapping table)
    g.add((pop_in_zone, RDF.type, TOR.BuildingPopulation))
    g.add((max_uri, I72.parameter_of_var, build))
    g.add((build, I72.hasName, height_var))

g.serialize("Height.ttl", format="turtle")
