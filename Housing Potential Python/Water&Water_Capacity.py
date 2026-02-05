# =========================
# Water + Water Capacity TTL Generator
# =========================
# This script reads:
#   (1) a watermain (distribution pipe) CSV with geometry,
#   (2) a ward-level synthetic capacity CSV (total + available),
#   (3) many yearly ward-level water consumption spreadsheets,
# and produces two TTL files:
#   - water.ttl: water service + pipes + ward-year sub-services + consumption ("capacity in use")
#   - water_capacity.ttl: ward-year total capacity + available capacity
#
# It also queries an existing GraphDB repository for ward locations (WKT) so that
# each ward catchment area can reuse the ward geometry already in the knowledge graph.

import pandas as pd
from rdflib import Graph, Namespace, Literal, RDFS, URIRef
from rdflib.namespace import RDF, XSD
import json
from pathlib import Path
import requests


# -------------------------
# Input file paths
# -------------------------
# Distribution watermain dataset (pipes) with geometry in GeoJSON string form.
csv_path_main = "Distribution Watermain - 4326.csv"

# Synthetic capacity dataset by ward/year (total capacity + available capacity).
csv_path_capacity = "Water_Consumption_Capacity_2020(Water_Consumption_2020).csv"

# Load the two CSVs into pandas DataFrames.
water_df = pd.read_csv(csv_path_main)
capacity_df = pd.read_csv(csv_path_capacity)

# List of ward-level annual consumption files (older ones are .xls, newer are .xlsx).
# The script iterates through all these and adds ward-year "capacity in use" measures.
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


# -------------------------
# RDF Namespace setup
# -------------------------
# These namespaces define the vocabularies used in the City Digital Twin.
TOR = Namespace("http://ontology.eil.utoronto.ca/Toronto/Toronto#")
GENPROP = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/")
LOC = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
HP = Namespace('http://ontology.eil.utoronto.ca/HPCDM/')
SERVICE = Namespace("https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/CityService/")
CHANGE = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Change/")
TIME = Namespace("http://www.w3.org/2006/time#")
RES = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Resource/")
I72 = Namespace("http://ontology.eil.utoronto.ca/ISO21972/iso21972#")


# -------------------------
# RDF Graph initialization
# -------------------------
# g will hold:
#   - the top-level WaterService
#   - distribution pipe sites + their geospatial locations
#   - ward-year subservices
#   - ward catchment area links + time intervals
#   - ward-year consumption values (capacityInUse)
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

# capacity_g will hold:
#   - ward-year total capacity values (hasCapacity)
#   - ward-year available capacity values (hasAvailableCapacity)
capacity_g = Graph()
capacity_g.bind("hp", HP)
capacity_g.bind('tor', TOR)
capacity_g.bind('res', RES)
capacity_g.bind('i72', I72)

# -------------------------
# Create the top-level WaterService node
# -------------------------
# URI for the city-wide water service.
water_serv_uri = TOR["waterservice"]

# Declare it as a WaterService in the HPCDM ontology.
g.add((water_serv_uri, RDF.type, HP.WaterService))

# NOTE: This triple says the resource is a subclass of HP.Service.
# In typical OWL modeling, subclass relationships are between classes,
# but this line is kept as-is (no changes requested).
g.add((water_serv_uri, RDFS.subClassOf, HP.Service))


# -------------------------
# 1) Synthetic capacity mapping (total + available) into capacity_g
# -------------------------
# For each ward/year row in the synthetic capacity CSV, generate:
#   distribution_uri --res:hasCapacity--> capacity_uri (typed WaterDistributionRate)
#   capacity_uri --i72:hasValue--> measure_uri
#   measure_uri --i72:hasNumericalValue--> decimal literal
#   measure_uri --i72:hasUnit--> hp:cubic_metre_per_year
#
# and similarly:
#   distribution_uri --res:hasAvailableCapacity--> avacapacity_uri ... etc
for _, row in capacity_df.iterrows():
    # Skip rows missing ward or year.
    if not(pd.isna(row['city ward'])) and not(pd.isna(row['year'])):
        # Ward-year distribution service identifier.
        distribution_uri = TOR[f"water_distributionservice_ward{int(row['city ward'])}_{int(row['year'])}"]

        # Total capacity rate node and its measure node.
        capacity_uri = TOR[f"water_distributionservice_ward{int(row['city ward'])}_{int(row['year'])}_Capacity"]
        measure_uri = TOR[f"water_distributionservice_ward{int(row['city ward'])}_{int(row['year'])}_CapacityMeasure"]

        # Available capacity rate node and its measure node.
        avacapacity_uri = TOR[f"water_distributionservice_ward{int(row['city ward'])}_{int(row['year'])}_AvailCapacity"]
        avameasure_uri = TOR[f"water_distributionservice_ward{int(row['city ward'])}_{int(row['year'])}_AvailCapacityMeasure"]

        # Link ward-year service to its TOTAL capacity.
        capacity_g.add((distribution_uri, RES.hasCapacity, capacity_uri))
        capacity_g.add((capacity_uri, RDF.type, HP.WaterDistributionRate))
        capacity_g.add((capacity_uri, I72.hasValue, measure_uri))

        # Convert "Synthetic Capacity" to float:
        # - remove commas (e.g., "1,234.5")
        # - store as XSD.decimal
        capacity_g.add(
            (measure_uri, I72.hasNumericalValue,
             Literal(float(row['Synthetic Capacity'].replace(',', '')), datatype=XSD.decimal))
        )

        # Unit is cubic metres per year.
        capacity_g.add((measure_uri, I72.hasUnit, HP.cubic_metre_per_year))

        # Link ward-year service to its AVAILABLE capacity.
        capacity_g.add((distribution_uri, RES.hasAvailableCapacity, avacapacity_uri))
        capacity_g.add((avacapacity_uri, RDF.type, HP.WaterDistributionRate))
        capacity_g.add((avacapacity_uri, I72.hasValue, avameasure_uri))

        # Convert "Synthetic Available Capacity" similarly (remove commas, store decimal).
        capacity_g.add(
            (avameasure_uri, I72.hasNumericalValue,
             Literal(float(row['Synthetic Available Capacity'].replace(',', '')), datatype=XSD.decimal))
        )

        # Same unit.
        capacity_g.add((avameasure_uri, I72.hasUnit, HP.cubic_metre_per_year))


# -------------------------
# 2) Distribution watermain (pipe) mapping into g
# -------------------------
# For each watermain row:
#   WaterService --hp:providedFromSite--> Pipe
#   Pipe --genprop:hasIdentifier--> asset id literal
#   Pipe --loc:hasLocation--> Location node
#   Location --geo:asWKT--> LINESTRING(...) geometry
#
# Geometry source is a GeoJSON string in the 'geometry' column.
for _, row in water_df.iterrows():
    # Unique URIs based on the internal _id field.
    water_pipe_uri = TOR[f"waterservice_distributionpipes{row['_id']}"]
    loc_uri = TOR[f"waterservice_distributionpipes_loc{row['_id']}"]

    # Connect the pipe as a site from which the water service is provided.
    g.add((water_serv_uri, HP.providedFromSite, water_pipe_uri))

    # Add a human-meaningful identifier from the dataset.
    g.add((water_pipe_uri,
           GENPROP.hasIdentifier,
           Literal(row['Watermain Asset Identification'], datatype=XSD.string)))

    # Create/link a location node for geospatial representation.
    g.add((water_pipe_uri, LOC.hasLocation, loc_uri))

    # Parse GeoJSON geometry stored as a JSON string.
    geom_json = json.loads(row['geometry'])
    geom_type = geom_json.get("type")
    coords = geom_json.get("coordinates")

    # Handle either MultiLineString or LineString.
    # If MultiLineString, this script only uses coords[0] (first line).
    if geom_type == "MultiLineString":
        line_coords = coords[0]
    elif geom_type == "LineString":
        line_coords = coords
    else:
        # Skip any unsupported geometry types.
        continue

    # Convert coordinates into WKT "x y" pairs and build a LINESTRING WKT literal.
    coord_strings = [f"{x} {y}" for x, y in line_coords]
    wkt = f"LINESTRING ({', '.join(coord_strings)})"

    # Store geometry in GeoSPARQL WKT literal form.
    g.add((loc_uri, GEO.asWKT, Literal(wkt, datatype=GEO.wktLiteral)))


# -------------------------
# 3) Ward geometry lookup (GraphDB SPARQL)
# -------------------------
# The goal here is:
#   - retrieve each Ward instance and its Location node from an existing repository
#   - build a local index {ward_num -> loc_uri}
#   - create a catchment URI per ward and link it to the ward location
#   - also try to retrieve and re-assert the ward's WKT geometry for downstream use
REPO = "CityDigitalTwin"
WARD_SPARQL_URL = f"http://ec2-3-97-59-180.ca-central-1.compute.amazonaws.com:7200/repositories/{REPO}"

# Query: get up to 100 wards and their hasLocation target.
WARD_QUERY = """
PREFIX iso50871: <http://ontology.eil.utoronto.ca/5087/1/SpatialLoc/>
PREFIX toronto: <http://ontology.eil.utoronto.ca/Toronto/Toronto#>
SELECT * WHERE {
  ?s a toronto:Ward ;
     iso50871:hasLocation ?loc .
}
LIMIT 100
"""

# Will store ward number -> location URI, so later consumption rows can reuse the correct location.
ward_loc_index: dict[str, str] = {}

# Execute the SPARQL query.
resp = requests.get(
    WARD_SPARQL_URL,
    params={
        "query": WARD_QUERY,
        "infer": "true",
        "sameAs": "true",
    },
    headers={"Accept": "application/sparql-results+json"},
    timeout=15,
)

if resp.status_code == 200:
    # Parse SPARQL JSON results.
    data = resp.json()
    bindings = data["results"]["bindings"]
    print(f"[WARD-SPARQL] got {len(bindings)} rows")

    for b in bindings:
        # Ward URI and corresponding location URI from SPARQL results.
        s_uri = b["s"]["value"]
        loc_uri = b["loc"]["value"]

        # Extract ward number from the ward URI fragment (digits).
        # Example: "...#Ward_01" -> "01" -> lstrip -> "1"
        local = s_uri.split("#")[-1]
        digits = "".join(ch for ch in local if ch.isdigit())
        ward_num = (digits.lstrip("0") or "0")

        # Create a catchment resource for the ward and link it to the ward's location.
        catchment_uri = TOR[f"water_distributionservice_ward_catchment{ward_num}"]
        g.add((catchment_uri, LOC.hasLocation, URIRef(loc_uri)))

        # Save for later: consumption mapping can attach catchment -> loc directly.
        ward_loc_index[ward_num] = loc_uri

        # For each ward location, attempt to pull the WKT literal from the repository.
        # This lets the output TTL include the ward geometry even if not otherwise present.
        wkt_query = f"""
        SELECT ?wkt WHERE {{
          <{loc_uri}> <http://www.opengis.net/ont/geosparql#asWKT> ?wkt .
        }}
        LIMIT 1
        """
        wkt_resp = requests.get(
            WARD_SPARQL_URL,
            params={"query": wkt_query, "infer": "true", "sameAs": "true"},
            headers={"Accept": "application/sparql-results+json"},
            timeout=15,
        )

        if wkt_resp.status_code == 200:
            wkt_data = wkt_resp.json()
            rows = wkt_data["results"]["bindings"]
            if rows:
                # Get the WKT string and add it into our local graph.
                wkt_literal = rows[0]["wkt"]["value"]

                loc_ref = URIRef(loc_uri)
                g.add((loc_ref, RDF.type, LOC.Location))
                g.add((loc_ref, GEO.asWKT, Literal(wkt_literal, datatype=GEO.wktLiteral)))
        else:
            # Non-fatal: catchment still exists, but without re-asserted WKT in output TTL.
            print(f"[WARD-SPARQL] couldn't get WKT for {loc_uri}: {wkt_resp.status_code}")
else:
    # If the initial ward lookup fails, ward_loc_index stays empty and later logic
    # will not attach catchment locations for ward-year consumption rows.
    print("[WARD-SPARQL] failed:", resp.status_code, resp.text)



# -------------------------
# Helper functions for reading consumption spreadsheets
# -------------------------
def read_excel_any(path: str):
    # Choose engine based on file extension:
    #   - .xlsx uses openpyxl
    #   - .xls uses xlrd
    # If reading fails, print skip reason and return None.
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
    # Build a normalization map:
    #   "City\nWard" -> "city ward"
    #   extra spaces/newlines collapsed
    norm_map = {}
    for c in df.columns:
        key = " ".join(c.lower().split())
        norm_map[key] = c

    # Return the first matching original column name among candidates.
    for cand in candidates:
        cand_key = " ".join(cand.lower().split())
        if cand_key in norm_map:
            return norm_map[cand_key]
    return None


# -------------------------
# 4) Consumption mapping (ward-year capacity in use) into g
# -------------------------
# For each yearly file:
#   - load DataFrame
#   - identify ward/year/total consumption columns robustly
#   - create ward-year distribution service
#   - attach catchment
#   - attach time interval (begin/end timestamps for the year)
#   - attach capacityInUse rate and its measurement (m^3/year)
for xls_path in consumption_files:
    df = read_excel_any(xls_path)
    if df is None:
        continue

    # Print file info for debugging/verification.
    print("\n==============================")
    print(f"FILE: {xls_path}")
    print("columns:", list(df.columns))

    # Identify the key columns with tolerant matching (newlines, spacing, naming variants).
    ward_col = pick_col(df, ["city ward", "city\nward", "ward", "ward number"])
    year_col = pick_col(df, ["year"])
    total_col = pick_col(df, ["total consumption", "total\nconsumption", "total_consumption", "consumption total"])

    # If any column is missing, skip RDF generation for that file.
    if ward_col and year_col and total_col:
        print(df[[ward_col, year_col, total_col]].head(10).to_string(index=False))
    else:
        print("-> cannot find ward/year/total in this file; skipping RDF for it.")
        continue

    # Row-by-row: create ward-year service + time + consumption measure.
    for _, row in df.iterrows():
        # Skip incomplete rows.
        if pd.isna(row[ward_col]) or pd.isna(row[year_col]) or pd.isna(row[total_col]):
            continue

        # Normalize ward number:
        # sometimes ward values can be floats or strings; convert to int-like string.
        ward_raw = str(row[ward_col]).strip()
        ward_num = str(int(float(ward_raw)))

        # Parse year and total consumption numeric.
        year = int(row[year_col])
        total = float(row[total_col])

        # Construct URIs for the ward-year service, catchment, and time interval.
        distribution_uri = TOR[f"water_distributionservice_ward{ward_num}_{year}"]
        catchment_uri = TOR[f"water_distributionservice_ward_catchment{ward_num}"]
        interval_uri = TOR[f"interval_{year}"]
        start_uri = TOR[f"instant_{year}_start"]
        end_uri = TOR[f"instant_{year}_end"]

        # URIs for the "capacity in use" rate object and its measure node.
        capacity_uri = TOR[f"water_distributionservice_ward{ward_num}_{year}_capacityuse"]
        measure_uri = TOR[f"water_distributionservice_ward{ward_num}_{year}_capacityuse_measure"]

        # Link the ward-year service as a sub-service of the city-wide water service.
        g.add((water_serv_uri, HP.hasSubService, distribution_uri))

        # Link ward-year service to the ward catchment area.
        g.add((distribution_uri, SERVICE.hasCatchmentArea, catchment_uri))

        # Type the ward-year node as a WaterService.
        g.add((distribution_uri, RDF.type, HP.WaterService))

        # If we successfully looked up this ward's location earlier, attach it to catchment.
        if ward_num in ward_loc_index:
            g.add((catchment_uri, RDF.type, SERVICE.CatchmentArea))
            g.add((catchment_uri, LOC.hasLocation, URIRef(ward_loc_index[ward_num])))

        # Attach a time interval for the service's existence/validity (the given year).
        g.add((distribution_uri, CHANGE.existAt, interval_uri))
        g.add((interval_uri, TIME.hasBeginning, start_uri))
        g.add((interval_uri, TIME.hasEnd, end_uri))

        # Define explicit timestamps for the year boundaries (timezone offset included).
        g.add((start_uri, TIME.inXSDDateTimeStamp,
               Literal(f"{year}-01-01T00:00:00-05:00", datatype=XSD.dateTime)))
        g.add((end_uri, TIME.inXSDDateTimeStamp,
               Literal(f"{year}-12-31T23:59:59-05:00", datatype=XSD.dateTime)))

        # Model consumption as "capacity in use" (rate + measure).
        g.add((distribution_uri, RES.capacityInUse, capacity_uri))
        g.add((capacity_uri, RDF.type, HP.WaterDistributionRate))
        g.add((capacity_uri, I72.hasValue, measure_uri))
        g.add((measure_uri, I72.hasNumericalValue, Literal(total, datatype=XSD.decimal)))
        g.add((measure_uri, I72.hasUnit, HP.cubic_metre_per_year))


# -------------------------
# Output serialization
# -------------------------
# Write the two graphs to Turtle files.
g.serialize("water.ttl", format="turtle")
capacity_g.serialize("water_capacity.ttl", format="turtle")
print("\nwrote water.ttl")
