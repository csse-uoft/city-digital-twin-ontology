import pandas as pd
import json
from shapely.geometry import shape
from rdflib import Graph, Namespace, Literal, RDFS
from rdflib.namespace import RDF, XSD

# ---------------- inputs ----------------
run_df = pd.read_csv("toronto-fire-services-run-areas - 4326.csv")
station_df = pd.read_csv("fire-station-locations - 4326.csv")

# --------------- namespaces -------------
TOR = Namespace("http://ontology.eil.utoronto.ca/Toronto/Toronto#")
HP  = Namespace("http://ontology.eil.utoronto.ca/HPCDM/")
GENPROP = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
SERVICE = Namespace("https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/CityService/")

# NOTE: change these to the exact namespaces you use in your project
ORG = Namespace("https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Organization/")
CONTACT = Namespace("https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Contact/")
LOC = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/")
CDT = Namespace("http://ontology.eil.utoronto.ca/CDT#")
RES = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Resource/")
I72 = Namespace("http://ontology.eil.utoronto.ca/ISO21972/iso21972#")

g = Graph()
g.bind("tor", TOR)
g.bind("hp", HP)
g.bind("genprop", GENPROP)
g.bind("geo", GEO)
g.bind("service", SERVICE)
g.bind("org_city", ORG)
g.bind("contact", CONTACT)
g.bind("loc", LOC)
g.bind("cdt", CDT)
g.bind("res", RES)
g.bind("i72", I72)


def infer_geom_type(coords):
    # coords could be Point, LineString, Polygon, MultiPolygon...
    try:
        if isinstance(coords, (list, tuple)) and len(coords) == 2 and all(isinstance(x, (int, float)) for x in coords):
            return "Point"
        if isinstance(coords, (list, tuple)) and coords and isinstance(coords[0], (list, tuple)):
            a = coords[0]
            if len(a) == 2 and all(isinstance(x, (int, float)) for x in a):
                return "LineString"
            if a and isinstance(a[0], (list, tuple)) and len(a[0]) == 2:
                return "Polygon"
            if a and isinstance(a[0], (list, tuple)) and isinstance(a[0][0], (list, tuple)) and len(a[0][0]) == 2:
                return "MultiPolygon"
    except Exception:
        pass
    return None

def geom_to_wkt(geom_val: str, default_type: str | None = None) -> str | None:
    if pd.isna(geom_val):
        return None
    s = str(geom_val).strip()

    # already WKT?
    if s.startswith(("POLYGON", "MULTIPOLYGON", "LINESTRING", "MULTILINESTRING", "POINT", "MULTIPOINT")):
        return s

    d = json.loads(s)

    # some Toronto CSVs store {"coordinates": ...} without "type"
    if "type" not in d:
        coords = d.get("coordinates", None)
        if coords is None:
            return None
        gtype = default_type or infer_geom_type(coords)
        if gtype is None:
            return None
        d = {"type": gtype, "coordinates": coords}

    return shape(d).wkt

# ---------------- RUN AREAS (your existing mapping) ----------------
for _, row in run_df.iterrows():
    run_area = str(row["RUN_AREA"]).strip()
    area_id = str(row["AREA_ID"]).strip()

    fire_service_uri = TOR[f"fire_service{run_area}"]
    catchment_uri    = TOR[f"fire_catchment_{area_id}"]

    wkt = geom_to_wkt(row["geometry"], default_type="MultiPolygon")
    if wkt is None:
        continue

    g.add((fire_service_uri, RDF.type, TOR.TorFireEmergencyService))
    g.add((fire_service_uri, SERVICE.hasCatchmentArea, catchment_uri))
    g.add((catchment_uri, GENPROP.hasIdentifier, Literal(area_id, datatype=XSD.string)))
    g.add((catchment_uri, GEO.asWKT, Literal(wkt, datatype=GEO.wktLiteral)))

# ---------------- STATION LOCATIONS (new dataset mapping) ----------------

# global org triples from your screenshot
fire_services_org = TOR["fire_services"]
emergency_service = TOR["emergency_service"]
g.add((TOR.TorFireEmergencyService, RDFS.subClassOf, HP.FireEmergencyService))
g.add((fire_services_org, RDF.type, ORG.Organization))
g.add((fire_services_org, CDT.providesService, emergency_service))

for _, row in station_df.iterrows():
    if pd.isna(row["STATION"]):
        continue

    station = int(row["STATION"])

    # columns (keep it robust to slight name differences)
    addr_point_id = str(row.get("ADDRESS_POINT_ID", "")).strip()
    addr_number   = row.get("ADDRESS_NUMBER")
    street_name   = str(row.get("LINEAR_NAME_FULL", row.get("LINEAR_NAME_FU", ""))).strip()

    fire_service_uri = TOR[f"fire_service{station}"]
    station_uri      = TOR[f"fire_station_{station}"]

    address_uri = TOR[f"fire_station_address_{addr_point_id}"]
    loc_uri     = TOR[f"fire_station_loc_{addr_point_id}"]


    g.add((station_uri, GENPROP.hasName, Literal(f"Fire Station {station}", datatype=XSD.string)))


    # hp:providedFromSite
    g.add((fire_service_uri, HP.providedFromSite, station_uri))

    # org:siteAddress -> address node
    g.add((station_uri, ORG.siteAddress, address_uri))
    g.add((address_uri, RDF.type, CONTACT.Address))

    if addr_number:
        g.add((address_uri, CONTACT.hasStreetNumber, Literal(int(addr_number), datatype=XSD.integer)))
    if street_name:
        g.add((address_uri, CONTACT.hasStreetName, Literal(street_name, datatype=XSD.string)))

    wkt = geom_to_wkt(row["geometry"], default_type="Point")
    if wkt:
        g.add((station_uri, LOC.hasLocation, loc_uri))
        g.add((loc_uri, GEO.asWKT, Literal(wkt, datatype=GEO.wktLiteral)))

    cap_uri = TOR[f"fire_service{station}Capacity"]
    meas_uri = TOR[f"fire_service{station}CapacityMeasure"]

    g.add((fire_service_uri, RES.hasCapacity, cap_uri))
    g.add((cap_uri, RDF.type, HP.MinFirefighterPerPopulation))
    g.add((cap_uri, I72.hasValue, meas_uri))
    g.add((meas_uri, I72.hasNumericalValue, Literal(0.001, datatype=XSD.decimal)))
    g.add((meas_uri, I72.hasUnit, I72.population_ratio_unit))

g.serialize("fire.ttl", format="turtle")
print('Fire')


# -------- Synthetic --------
df = pd.read_csv("synthetic firefighter and population counts(in).csv")

# -------- namespaces (set these to match your project) --------
TOR = Namespace("http://ontology.eil.utoronto.ca/Toronto/Toronto#")
HP = Namespace('http://ontology.eil.utoronto.ca/HPCDM/')

# If you already have the exact IRI for res: and i72: in your other scripts, reuse it here.
I72 = Namespace("http://ontology.eil.utoronto.ca/ISO21972/iso21972#")
RES = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Resource/")       # <-- adjust if needed

g = Graph()
g.bind("tor", TOR)
g.bind("hp", HP)
g.bind("res", RES)
g.bind("i72", I72)

def dec_lit(x):
    return Literal(float(x), datatype=XSD.decimal)

VAL_COL = "Firefighters per person in run area"

for _, row in df.iterrows():
    run_area = int(row["RUN_AREA"])

    # tor:fire_service{RUN_AREA}
    fire_service_uri = TOR[f"fire_service{run_area}"]

    # Treat STATION as RUN_AREA for this synthetic dataset
    cap_uri = TOR[f"fire_service{run_area}CapacityUse"]
    measure_uri = TOR[f"fire_service{run_area}CapacityUseMeasure"]
    avail = TOR[f"fire_service{run_area}AvailCapacity"]
    availmeasure = TOR[f"fire_service{run_area}AvailCapacityMeasure"]

    # RUN_AREA → res:capacityInUse → CapacityU
    g.add((fire_service_uri, RES.capacityInUse, cap_uri))

    # CapacityU rdf:type hp:FirefighterPerPopulation
    g.add((cap_uri, RDF.type, HP.FirefighterPerPopulation))

    # CapacityU i72:hasValue CapacityUseMeasure
    g.add((cap_uri, I72.hasValue, measure_uri))

    # CapacityUseMeasure i72:hasNumericalValue {Firefighters per person...}
    ff_per_person = row[VAL_COL]
    g.add((measure_uri, I72.hasNumericalValue, dec_lit(ff_per_person)))

    # CapacityUseMeasure i72:hasUnit hp:firefighter_per_person
    g.add((measure_uri, I72.hasUnit, I72.population_ratio_unit))

    g.add((fire_service_uri, RES.hasAvailableCapacity, avail))
    g.add((avail, RDF.type, HP.AvailableFirefightersPerPopulation))
    g.add((avail, I72.hasValue, availmeasure))
    g.add((availmeasure, I72.hasNumericalValue, Literal(0.001 - float(dec_lit(ff_per_person)), datatype=XSD.decimal)))
    g.add((availmeasure, I72.hasUnit, I72.population_ratio_unit))


g.serialize("fire_synthetic.ttl", format="turtle")
print('Synthetic')