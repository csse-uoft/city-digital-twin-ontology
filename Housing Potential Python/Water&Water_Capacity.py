import pandas as pd
from rdflib import Graph, Namespace, Literal, RDFS, URIRef
from rdflib.namespace import RDF, XSD
import json
from pathlib import Path
import requests


csv_path_main = "Distribution Watermain - 4326.csv"
csv_path_capacity = "Water_Consumption_Capacity_2020(Water_Consumption_2020).csv"
water_df = pd.read_csv(csv_path_main)
capacity_df = pd.read_csv(csv_path_capacity)

consumption_files = [
    "Water_Consumption_2000.xls",
    "Water_Consumption_2001.xls",
    "Water_Consumption_2002.xls",
    "Water_Consumption_2003.xls",
    "Water_Consumption_2004.xls",
    "Water_Consumption_2005.xls",
    "Water_Consumption_2006.xls",
    "Water_Consumption_2007.xls",
    "Water_Consumption_2008.xls",
    "Water_Consumption_2009.xls",
    "Water_Consumption_2010.xls",
    "Water_Consumption_2011.xls",
    "Water_Consumption_2012.xls",
    "Water_Consumption_2013.xls",
    "Water_Consumption_2014.xls",
    "Water_Consumption_2015.xls",
    "Water_Consumption_2016.xlsx",
    "Water_Consumption_2017.xlsx",
    "Water_Consumption_2018.xlsx",
    "Water_Consumption_2019.xlsx",
    "Water_Consumption_2020.xlsx",
]


GENPROP = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/")
LOC = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
HP = Namespace('http://ontology.eil.utoronto.ca/HPCDM/')
SERVICE = Namespace("https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/CityService/")
CHANGE = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Change/")
TIME = Namespace("http://www.w3.org/2006/time#")
RES = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Resource/")
I72 = Namespace("http://ontology.eil.utoronto.ca/ISO21972/iso21972#")
TOR = Namespace("http://ontology.eil.utoronto.ca/HPCDM/TorontoHPCDM/")


g = Graph()
g.bind("hp", HP)
g.bind("genprop", GENPROP)
g.bind("loc", LOC)
g.bind('geo', GEO)
g.bind('tor', TOR)
g.bind('service', SERVICE)
g.bind('change', CHANGE)
g.bind('time', TIME)
g.bind('res', RES)
g.bind('i72', I72)

capacity_g = Graph()
capacity_g.bind("hp", HP)
capacity_g.bind('tor', TOR)
capacity_g.bind('res', RES)
capacity_g.bind('i72', I72)

water_serv_uri = TOR["waterservice"]
g.add((water_serv_uri, RDF.type, TOR.TorWaterService))
g.add((TOR.TorWaterService, RDFS.subClassOf, HP.WaterService))
g.add((water_serv_uri, RDFS.subClassOf, HP.Service))

for _, row in capacity_df.iterrows():
    if not(pd.isna(row['city ward'])) and not(pd.isna(row['year'])):
        distribution_uri = TOR[f"water_distributionservice_ward{int(row['city ward'])}_{int(row['year'])}"]
        capacity_uri = TOR[f"water_distributionservice_ward{int(row['city ward'])}_{int(row['year'])}_Capacity"]
        measure_uri = TOR[f"water_distributionservice_ward{int(row['city ward'])}_{int(row['year'])}_CapacityMeasure"]
        avacapacity_uri = TOR[f"water_distributionservice_ward{int(row['city ward'])}_{int(row['year'])}_AvailCapacity"]
        avameasure_uri = TOR[f"water_distributionservice_ward{int(row['city ward'])}_{int(row['year'])}_AvailCapacityMeasure"]

        capacity_g.add((distribution_uri, RES.hasCapacity, capacity_uri))
        capacity_g.add((capacity_uri, RDF.type, HP.WaterDistributionRate))
        capacity_g.add((capacity_uri, I72.hasValue, measure_uri))
        capacity_g.add((measure_uri, I72.hasNumericalValue, Literal(float(row['Synthetic Capacity'].replace(',', '')), datatype=XSD.decimal)))
        capacity_g.add((measure_uri, I72.hasUnit, HP.cubic_metre_per_year))

        capacity_g.add((distribution_uri, RES.hasAvailableCapacity, avacapacity_uri))
        capacity_g.add((avacapacity_uri, RDF.type, HP.AvailableWaterDistributionRate))
        capacity_g.add((avacapacity_uri, I72.hasValue, avameasure_uri))
        capacity_g.add((avameasure_uri, I72.hasNumericalValue, Literal(float(row['Synthetic Available Capacity'].replace(',', '')), datatype=XSD.decimal)))
        capacity_g.add((avameasure_uri, I72.hasUnit, HP.cubic_metre_per_year))


for _, row in water_df.iterrows():
    water_pipe_uri = TOR[f"waterservice_distributionpipes{row['_id']}"]
    loc_uri = TOR[f"waterservice_distributionpipes_loc{row['_id']}"]

    g.add((water_serv_uri, HP.providedFromSite, water_pipe_uri))
    g.add((water_pipe_uri, GENPROP.hasName, Literal(f"Watermain {row['Watermain Asset Identification']}", datatype=XSD.string)))

    g.add((water_pipe_uri,
           GENPROP.hasIdentifier,
           Literal(row['Watermain Asset Identification'], datatype=XSD.string)))
    g.add((water_pipe_uri, LOC.hasLocation, loc_uri))

    geom_json = json.loads(row['geometry'])
    geom_type = geom_json.get("type")
    coords = geom_json.get("coordinates")

    if geom_type == "MultiLineString":
        line_coords = coords[0]
    elif geom_type == "LineString":
        line_coords = coords
    else:
        continue

    coord_strings = [f"{x} {y}" for x, y in line_coords]
    wkt = f"LINESTRING ({', '.join(coord_strings)})"
    g.add((loc_uri, GEO.asWKT, Literal(wkt, datatype=GEO.wktLiteral)))


# ---- OFFLINE ward locations (Toronto2.ttl) ----
from rdflib import Graph, Namespace
from rdflib.namespace import RDF

TORONTO_TTL_PATH = "Toronto2.ttl"  # adjust if needed

TORONTO_NS = Namespace("http://ontology.eil.utoronto.ca/Toronto/Toronto#")
ISO50871 = Namespace("http://ontology.eil.utoronto.ca/5087/1/SpatialLoc/")  # ns1 in Toronto2.ttl

toronto_g = Graph()
toronto_g.parse(TORONTO_TTL_PATH, format="turtle")

ward_loc_index: dict[str, str] = {}

for ward_uri in toronto_g.subjects(RDF.type, TORONTO_NS.Ward):
    # ward URIs look like ...#ward16, ...#ward3, etc.
    local = str(ward_uri).split("#")[-1]
    digits = "".join(ch for ch in local if ch.isdigit())
    ward_num = digits.lstrip("0") or "0"

    loc_uri = next(toronto_g.objects(ward_uri, ISO50871.hasLocation), None)
    if loc_uri is None:
        continue

    ward_loc_index[ward_num] = str(loc_uri)

    # create the catchment + link to the ward location
    catchment_uri = TOR[f"water_distributionservice_ward_catchment{ward_num}"]
    g.add((catchment_uri, RDF.type, SERVICE.CatchmentArea))
    g.add((catchment_uri, LOC.hasLocation, loc_uri))

    # OPTIONAL (recommended): copy the geometry into your output TTL so it's self-contained
    for wkt_lit in toronto_g.objects(loc_uri, GEO.asWKT):
        g.add((loc_uri, RDF.type, LOC.Location))
        g.add((loc_uri, GEO.asWKT, wkt_lit))

print(f"[WARD-OFFLINE] loaded {len(ward_loc_index)} wards from {TORONTO_TTL_PATH}")



def read_excel_any(path: str):
    ext = Path(path).suffix.lower()
    try:
        if ext == ".xlsx":
            return pd.read_excel(path, engine="openpyxl")
        else:
            return pd.read_excel(path, engine="xlrd")
    except Exception as e:
        print(f"[SKIP] {path}: {e}")
        return None

def pick_col(df: pd.DataFrame, candidates: list[str]):
    """match columns even if they have newlines / extra spaces"""
    norm_map = {}
    for c in df.columns:
        key = " ".join(c.lower().split())
        norm_map[key] = c

    for cand in candidates:
        cand_key = " ".join(cand.lower().split())
        if cand_key in norm_map:
            return norm_map[cand_key]
    return None


for xls_path in consumption_files:
    df = read_excel_any(xls_path)
    if df is None:
        continue

    print("\n==============================")
    print(f"FILE: {xls_path}")
    print("columns:", list(df.columns))

    ward_col = pick_col(df, ["city ward", "city\nward", "ward", "ward number"])
    year_col = pick_col(df, ["year"])
    total_col = pick_col(df, ["total consumption", "total\nconsumption", "total_consumption", "consumption total"])

    if ward_col and year_col and total_col:
        print(df[[ward_col, year_col, total_col]].head(10).to_string(index=False))
    else:
        print("-> cannot find ward/year/total in this file; skipping RDF for it.")
        continue

    for _, row in df.iterrows():
        if pd.isna(row[ward_col]) or pd.isna(row[year_col]) or pd.isna(row[total_col]):
            continue

        ward_raw = str(row[ward_col]).strip()
        ward_num = str(int(float(ward_raw)))
        year = int(row[year_col])
        total = float(row[total_col])

        distribution_uri = TOR[f"water_distributionservice_ward{ward_num}_{year}"]
        catchment_uri = TOR[f"water_distributionservice_ward_catchment{ward_num}"]
        interval_uri = TOR[f"interval_{year}"]
        start_uri = TOR[f"instant_{year}_start"]
        end_uri = TOR[f"instant_{year}_end"]
        capacity_uri = TOR[f"water_distributionservice_ward{ward_num}_{year}_capacityuse"]
        measure_uri = TOR[f"water_distributionservice_ward{ward_num}_{year}_capacityuse_measure"]

        g.add((water_serv_uri, HP.hasSubService, distribution_uri))
        g.add((distribution_uri, SERVICE.hasCatchmentArea, catchment_uri))
        g.add((distribution_uri, RDF.type, TOR.TorWaterService))

        if ward_num in ward_loc_index:
            g.add((catchment_uri, RDF.type, SERVICE.CatchmentArea))
            g.add((catchment_uri, LOC.hasLocation, URIRef(ward_loc_index[ward_num])))

        g.add((distribution_uri, CHANGE.existsAt, interval_uri))
        g.add((interval_uri, TIME.hasBeginning, start_uri))
        g.add((interval_uri, TIME.hasEnd, end_uri))
        g.add((start_uri, TIME.inXSDDateTimeStamp,
               Literal(f"{year}-01-01T00:00:00-05:00", datatype=XSD.dateTime)))
        g.add((end_uri, TIME.inXSDDateTimeStamp,
               Literal(f"{year}-12-31T23:59:59-05:00", datatype=XSD.dateTime)))

        g.add((distribution_uri, RES.capacityInUse, capacity_uri))
        g.add((capacity_uri, RDF.type, HP.WaterDistributionRate))
        g.add((capacity_uri, I72.hasValue, measure_uri))
        g.add((measure_uri, I72.hasNumericalValue, Literal(total, datatype=XSD.decimal)))
        g.add((measure_uri, I72.hasUnit, HP.cubic_metre_per_year))


g.serialize("water.ttl", format="turtle")
capacity_g.serialize("water_capacity.ttl", format="turtle")
print("\nwrote water.ttl")
