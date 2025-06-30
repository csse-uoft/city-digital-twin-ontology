"""
Generate TTL file with ORN Road Data mapped onto the Transportation ontology.
"""

import geopandas as gpd
import pandas as pd
from rdflib import Graph, Namespace, Literal, RDFS, XSD, RDF
from datetime import datetime

# Define namespaces
BASE_URI = "https://standards.iso.org/iso-iec/5087/-3/ed-1/en/ontology/"
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
TRANSPORT = Namespace(BASE_URI + "TransportationNetwork/")
ROAD = Namespace(BASE_URI + "RoadNetwork/")
INFRAS = Namespace("https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/TransportationInfrastructure/")
INFRASTRUCTURE = Namespace("https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Infrastructure/")
GEO_LOC = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/")
PARTWHOLE = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Mereology/")
CITYUNITS = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/CityUnits/")
CDT = Namespace("http://ontology.eil.utoronto.ca/CDT#")
I72 = Namespace("http://ontology.eil.utoronto.ca/5087/2/iso21972/")
GEN = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/")
ORG = Namespace("https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Organization/")
CODE = Namespace("https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Code/")
CITY = Namespace("https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/City/")
CONTACT = Namespace("https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Contact/")

"""
BASE_URI: The root base for ISO/IEC 5087-3 ontology definitions
GEO: Geospatial ontology from GeoSPARQL — used for spatial concepts like Geometry, WKT literals
TRANSPORT: Transportation Network pattern from ISO/IEC 5087-3 — includes core classes like Road, RoadLink, Junction, etc.
INFRAS: Transportation Infrastructure pattern from ISO/IEC 5087-2 — specialized types of infrastructure (e.g., RoadLink, RoadSegment)
GEO_LOC: Spatial Location pattern from ISO/IEC 5087-1 — used to define spatial positions (e.g., hasLocation, asWKT)
PARTWHOLE: Mereology (part-whole relationships) from ISO/IEC 5087-1 — defines hasProperPart / properPartOf relationships
CITYUNITS: City Units pattern from ISO/IEC 5087-1 — used for physical measures (e.g., speed, length) with measurementValue + unitOfMeasure
CDT: City Digital Twin namespace — used to define custom/extended properties not in the ISO standard
RDFS: RDF Schema vocabulary — used to define class hierarchies and metadata (e.g., subClassOf, label, comment)
I72: # ISO 21972-based ontology for standardized quantity/value modeling (e.g., Length, Speed, Weight)
GEN: # ISO 5087-1 Generic Properties — used for linking general metadata like identifiers
RDF: # RDF standard namespace for core RDF types and structures (e.g., rdf:type)
"""

# Load the shapefile
shapefile_path = "ORN_ROAD_NET_ELEMENT.shp"
road_network_gdf = gpd.read_file(shapefile_path)

# Ensure OGF_ID is a string since we need to link it with ORN_ROAD_NET_ELEMENT_ID which is a string
road_network_gdf["OGF_ID"] = road_network_gdf["OGF_ID"].astype(str)


# Define Toronto bounding box. This defines the geographic boundaries of Toronto,
# ensuring only junctions and roads within this area are included.

toronto_bounds = {
    "lat_min": 43.5810,
    "lat_max": 43.8555,
    "lon_min": -79.6393,
    "lon_max": -79.1152,
}

# Load CSV files with proper column renaming
csv_files = {
    "speed_limits": "ORN_SPEED_LIMIT.csv",
    "road_classes": "ORN_ROAD_CLASS.csv",
    "road_names": "ORN_OFFICIAL_STREET_NAME.csv",
    "junctions": "ORN_JUNCTION.csv",
    "blocked_passage": "ORN_BLOCKED_PASSAGE.csv",
    "address_info": "ORN_ADDRESS_INFO.csv",
    "jurisdiction": "ORN_JURISDICTION.csv",
    "num_lanes": "ORN_NUMBER_OF_LANES.csv",
    "road_surface": "ORN_ROAD_SURFACE.csv",
    "route_name": "ORN_ROUTE_NAME.csv",
    "route_number": "ORN_ROUTE_NUMBER.csv",
    "structure": "ORN_STRUCTURE.csv",
    "toll_point": "ORN_TOLL_POINT.csv",
    "underpass": "ORN_UNDERPASS.csv"
}

# Load CSVs into a dictionary with renamed columns
data_frames = {}
for name, path in csv_files.items():
    df = pd.read_csv(path, delimiter=";")

    # Ensure ORN_ROAD_NET_ELEMENT_ID is a string for merging
    if "ORN_ROAD_NET_ELEMENT_ID" in df.columns:
        df["ORN_ROAD_NET_ELEMENT_ID"] = df["ORN_ROAD_NET_ELEMENT_ID"].astype(str)

    # Rename columns to prevent merging conflicts
    df = df.rename(columns={col: f"{col}_{name}" for col in df.columns if col != "ORN_ROAD_NET_ELEMENT_ID"})

    data_frames[name] = df

# Merge all CSVs with the shapefile data using LEFT JOIN
for name, df in data_frames.items():
    if "ORN_ROAD_NET_ELEMENT_ID" in df.columns:
        road_network_gdf = road_network_gdf.merge(
            df, left_on="OGF_ID", right_on="ORN_ROAD_NET_ELEMENT_ID", how="left", suffixes=("", f"_{name}")
        )

# Final Check for Duplicate Columns
road_network_gdf = road_network_gdf.loc[:, ~road_network_gdf.columns.duplicated()]  # Remove duplicate columns

# Create RDF graph
g = Graph()
g.bind("rdfs", RDFS)
g.bind("geo", GEO)
g.bind("transnet", TRANSPORT)
g.bind("loc", GEO_LOC)
g.bind("partwhole", PARTWHOLE)
g.bind("cityunits", CITYUNITS)
g.bind("cdt", CDT)
g.bind("transinfras", INFRAS)
g.bind("infras", INFRASTRUCTURE)
g.bind ("rdf", RDF)
g.bind("i72", I72)
g.bind("genprop", GEN)
g.bind("org_city", ORG)
g.bind("code", CODE)
g.bind("city", CITY)
g.bind("contact", CONTACT)
g.bind("road", ROAD)

# ***

direction_enum_uris = {
    "Forward": CDT.Forward,
    "Reverse": CDT.Reverse,
    "Bi-directional": CDT.Bidirectional
}

for label, enum_uri in direction_enum_uris.items():
    g.add((enum_uri, RDF.type, TRANSPORT.LinkDirection))
    g.add((enum_uri, RDFS.label, Literal(label)))

# Function to safely convert date strings to XSD.date format
def format_date(value: str) -> str | None:
    """
    Formats a date string into the standard "YYYY-MM-DD" format for RDF serialization.

    Parameters:
    date_str (str): The date string in the format "YYYYMMDDHHMMSS" or other variations.

    Returns:
    str or None: The formatted date string as "YYYY-MM-DD" if conversion is successful,
                 otherwise None if the input is invalid or empty.

    Example:
    >>> format_date("20210731081808")
    '2021-07-31'

    >>> format_date("")
    None
    """

    if pd.notna(value):
        try:
            return datetime.strptime(str(value), "%Y%m%d%H%M%S").date().isoformat()  # Convert to YYYY-MM-DD
        except ValueError:
            return None  # If parsing fails, ignore the date
    return None

# Adding Junctions to the RDF Graph
for _, row in data_frames["junctions"].iterrows():
    junction_id = row["JUNCTION_ID_junctions"]
    latitude = row["LATITUDE_DECIMAL_DEGREES_junctions"]
    longitude = row["LONGITUDE_DECIMAL_DEGREES_junctions"]
    junction_type = row["JUNCTION_TYPE_junctions"]
    junc_exit_num = row["EXIT_NUMBER_junctions"]
    junc_uuid = row["NATIONAL_UUID_junctions"]
    junc_effec_date = row["EFFECTIVE_DATETIME_junctions"]

    # Ensure junctions are within Toronto bounds
    if not (toronto_bounds["lat_min"] <= latitude <= toronto_bounds["lat_max"] and
            toronto_bounds["lon_min"] <= longitude <= toronto_bounds["lon_max"]):
        continue

    # Create URIs
    junction_uri = CDT[f"junction_{junction_id}"]
    location_uri = GEO_LOC[f"junction_loc_{junction_id}"]
    junction_type_uri = CDT[f"junction_type_{junction_id}"]
    junction_type_code = CODE[f"junctionType_Code{junction_id}"]

    # Add triples for the junction
    g.add((junction_uri, GEN.hasIdentifier, Literal(int(junction_id), datatype=XSD.integer)))
    g.add((TRANSPORT.Junction, RDFS.subClassOf, TRANSPORT.TransportNode))
    g.add((CDT.Junction, RDFS.subClassOf, TRANSPORT.Junction))
    g.add((junction_uri, GEO_LOC.hasLocation, location_uri))
    g.add((junction_uri, RDF.type, CDT.Junction))

    g.add((junction_uri, CDT.hasJunctionType, junction_type_uri))
    g.add((junction_type_uri, RDF.type, CDT.JunctionType))
    g.add((junction_type_uri, CODE.hasCode, junction_type_code))
    g.add((junction_type_code, RDF.type, CODE.Code))
    g.add((junction_type_code, GEN.hasName, Literal(junction_type, datatype=XSD.string)))

    g.add((junction_uri, CDT.exitNumber, Literal(str(junc_exit_num), datatype=XSD.string)))
    g.add((junction_uri, CDT.nationUUID, Literal(junc_uuid, datatype=XSD.string)))
    g.add((junction_uri, CDT.effectiveDate, Literal(format_date(junc_effec_date), datatype=XSD.date)))

    # Add geospatial coordinates
    wkt_point = f"POINT ({longitude} {latitude})"
    g.add((location_uri, RDF.type, GEO_LOC.Location))
    g.add((GEO_LOC.Location, RDFS.subClassOf, GEO.Geometry))
    g.add((location_uri, GEO.asWKT, Literal(wkt_point, datatype=GEO.wktLiteral)))


# Adding Roads to the RDF Graph
id = 1
road_groups = road_network_gdf.groupby("FULL_STREET_NAME_road_names")
jurisdiction_dict = {}

for road_name, group in road_groups:
    if pd.isna(road_name):
        continue

    road_uri = CDT[f"road_{id}"]
    id += 1
    road_links = []  # Store all road link URIs for a given road

    for _, row in group.iterrows():
        road_id = row["OGF_ID"]
        road_geometry = row["geometry"].wkt  # Convert geometry to WKT

        # Ensure Roads are within Toronto bounds
        if not (toronto_bounds["lat_min"] <= row.geometry.bounds[1] <= toronto_bounds["lat_max"] and
                toronto_bounds["lon_min"] <= row.geometry.bounds[0] <= toronto_bounds["lon_max"]):
            continue

        # Extract metadata
        speed_limit = row.get("SPEED_LIMIT_speed_limits")
        road_class = row.get("ROAD_CLASS_road_classes")
        road_name = row.get("FULL_STREET_NAME_road_names")
        blocked_passage = row.get("BLOCKED_PASSAGE_TYPE_blocked_passage")
        jurisdiction = row.get("JURISDICTION_jurisdiction")
        num_lanes = row.get("NUMBER_OF_LANES_num_lanes")
        pavement_status = row.get("PAVEMENT_STATUS_road_surface")
        surface_type = row.get("SURFACE_TYPE_road_surface")
        route_name = row.get("ROUTE_NAME_ENGLISH_route_name")
        route_number = row.get("ROUTE_NUMBER_route_number")
        structure_type = row.get("STRUCTURE_TYPE_structure")
        toll_point_type = row.get("TOLL_POINT_TYPE_toll_point")
        underpass_type = row.get("UNDERPASS_TYPE_underpass")

        # Junction IDs
        from_junction_id = row.get("FROM_JCT")  # Junction at the start of the road_link
        to_junction_id = row.get("TO_JCT")  # Junction at the end of the road_link

        length = row.get("LENGTH")
        accuracy = row.get("ACCURACY")
        nid = row.get("NID")
        direction = row.get("DIRECTION")
        exit_num = row.get("EXIT_NUM")
        elem_type = row.get("ELEM_TYPE")
        toll_road = row.get("TOLL_ROAD")
        acqtech = row.get("ACQTECH")
        credate = row.get("CREDATE")
        revdate = row.get("REVDATE")
        geo_upd_dt = row.get("GEO_UPDATE_DT")
        eff_date = row.get("EFF_DATE")

        # Create URIs
        location_uri = GEO_LOC[f"location_{road_id}"]
        road_link_uri = CDT[f"roadLink_{road_id}"]
        road_user_uri = INFRAS[f"roadLinkUser_{road_id}"]

        road_links.append(road_link_uri)  # Collect all road links for the road

        # RoadLink
        g.add((road_link_uri, RDF.type, CDT.RoadLink))
        g.add((CDT.RoadLink, RDFS.subClassOf, INFRAS.RoadLink))
        g.add((INFRAS.RoadLink, RDFS.subClassOf, TRANSPORT.TravelledWayLink))
        g.add((TRANSPORT.TravelledWayLink, RDFS.subClassOf, INFRASTRUCTURE.InfrastructureElement))
        g.add((road_link_uri, PARTWHOLE.properPartOf, road_uri))
        g.add((road_link_uri, ROAD.usedBy, road_user_uri))
        g.add((road_user_uri, ROAD.uses, road_link_uri))
        g.add((road_link_uri, GEN.hasIdentifier, Literal(str(road_id), datatype=XSD.string)))

        if elem_type == "Virtual Road": # Filters all Virtual Roads
            continue

        # Add attributes conditionally

        if pd.notna(speed_limit):
            speed_uri = ROAD[f"speed_{road_id}"]
            speed_unit_uri = CITYUNITS[f"speedUnit_{road_id}"]
            speed_measure = CITYUNITS[f"speedMeasure_{road_id}"]

            g.add((speed_measure, RDF.type, CITYUNITS.Measure))
            g.add((speed_uri, RDF.type, CITYUNITS.Speed))
            g.add((speed_unit_uri, RDF.type, I72.kilometersPerHr))

            g.add((CITYUNITS.Speed, RDFS.subClassOf, I72.Quantity))
            g.add((speed_uri, I72.value, speed_measure))

            g.add((speed_measure, I72.unit_of_measure, speed_unit_uri))
            g.add((speed_measure, I72.numerical_value, Literal(int(speed_limit), datatype=XSD.integer)))

            g.add((road_user_uri, ROAD.speedLimit, speed_uri))

        if pd.notna(length):
            length_measurement = CITYUNITS[f"length_{road_id}"]
            length_unit_uri = CITYUNITS[f"lengthUnit_{road_id}"]
            length_measure = CITYUNITS[f"lengthMeasure_{road_id}"]

            g.add((length_measure, RDF.type, CITYUNITS.Measure))
            g.add((length_measurement, RDF.type, CITYUNITS.Length))
            g.add((length_unit_uri, RDF.type, I72.Meters))

            g.add((CITYUNITS.Length, RDFS.subClassOf, I72.Quantity))
            g.add((length_measurement, I72.value, length_measure))

            g.add((length_measure, I72.unit_of_measure, length_unit_uri))
            g.add((length_measure, I72.numerical_value, Literal(int(length), datatype=XSD.decimal)))

            g.add((road_link_uri, CDT.length, length_measurement))

        if pd.notna(accuracy):
            accuracy_measurement = CITYUNITS[f"accuracy_{road_id}"]
            accuracy_unit_uri = CITYUNITS[f"accuracyUnit_{road_id}"]
            accuracy_measure = CITYUNITS[f"accuracyMeasure_{road_id}"]

            g.add((accuracy_measure, RDF.type, CITYUNITS.Measure))
            g.add((accuracy_measurement, RDF.type, CITYUNITS.Length))
            g.add((accuracy_unit_uri, RDF.type, I72.Meters))

            g.add((CITYUNITS.Length, RDFS.subClassOf, I72.Quantity))
            g.add((accuracy_measurement, I72.value, accuracy_measure))

            g.add((accuracy_measure, I72.unit_of_measure, accuracy_unit_uri))
            g.add((accuracy_measure, I72.numerical_value, Literal(int(accuracy), datatype=XSD.decimal)))

            g.add((road_link_uri, CDT.roadAbsoluteAccuracy, accuracy_measurement))

        if pd.notna(nid):
            g.add((road_link_uri, CDT.nationUUID, Literal(nid, datatype=XSD.string)))

        if pd.notna(surface_type):
            surface_type_measurement = CDT[f"surface_type_{road_id}"]
            surface_Code = CODE[f"surfaceType_Code_{road_id}"]

            g.add((road_link_uri, CDT.hasSurfaceType, surface_type_measurement))
            g.add((surface_type_measurement, RDF.type, CDT.SurfaceType))
            g.add((surface_type_measurement, CODE.hasCode, surface_Code))
            g.add((surface_Code, RDF.type, CODE.Code))
            g.add((surface_Code, GEN.hasName, Literal(surface_type, datatype=XSD.string)))

        if pd.notna(direction): # *** Need to be Link Directions
            if direction == "Positive":
                g.add((road_link_uri, TRANSPORT.allowedDirections, CDT.Forward))
            elif direction == "Negative":
                g.add((road_link_uri, TRANSPORT.allowedDirections, CDT.Reverse))
            else:
                g.add((road_link_uri, TRANSPORT.allowedDirections, CDT.Bidirectional))

        if pd.notna(exit_num):
            g.add((road_link_uri, CDT.exitNum, Literal(exit_num, datatype=XSD.string)))

        if pd.notna(toll_road):
            if toll_road == "Yes":
                g.add((road_link_uri, CDT.tollRoad, Literal('true', datatype=XSD.boolean)))
            else:
                g.add((road_link_uri, CDT.tollRoad, Literal('false', datatype=XSD.boolean)))

        if pd.notna(acqtech):
            acqtech_measurement = CDT[f"acqtech_{road_id}"]
            acqtech_Code = CODE[f"acqtechCode_{road_id}"]

            g.add((road_link_uri, CDT.hasAquisitionTechnique, acqtech_measurement))
            g.add((acqtech_measurement, RDF.type, CDT.AquisitionTechnique))
            g.add((acqtech_measurement, CODE.hasCode, acqtech_Code))
            g.add((acqtech_Code, RDF.type, CODE.Code))
            g.add((acqtech_Code, GEN.hasName, Literal(acqtech, datatype=XSD.string)))

        if pd.notna(road_class):
            road_class_uri = CDT[f"roadClass_{road_id}"]
            codeRoadClass_uri = CDT[f"roadClass_Code_{road_id}"]

            g.add((road_link_uri, CDT.roadClass, road_class_uri))
            g.add((road_class_uri, RDF.type, CDT.RoadClass))
            g.add((road_class_uri, CODE.hasCode, codeRoadClass_uri))
            g.add((codeRoadClass_uri, RDF.type, CODE.Code))
            g.add((codeRoadClass_uri, GEN.hasName, Literal(road_class, datatype=XSD.string)))

        if pd.notna(road_name):
            g.add((road_link_uri, GEN.hasName, Literal(road_name, datatype=XSD.string)))

        if pd.notna(blocked_passage):
            blocked_uri = CDT[f"blockedPassage_{road_id}"]
            blocked_code = CDT[f"blockedPassage_Code_{road_id}"]

            g.add((road_link_uri, CDT.hasBlockedPassage, blocked_uri))
            g.add((blocked_uri, RDF.type, CDT.BlockedPassageType))
            g.add((blocked_uri, CODE.hasCode, blocked_code))
            g.add((blocked_code, RDF.type, CODE.Code))
            g.add((blocked_code, GEN.hasName, Literal(blocked_passage, datatype=XSD.string)))

        if pd.notna(jurisdiction):
            gov_org_uri = ORG[f"govOrg_{road_id}"]

            g.add((ORG.GovernmentOrganization, RDFS.subClassOf, ORG.Organization))
            g.add((gov_org_uri, RDF.type, ORG.GovernmentOrganization))

            g.add((gov_org_uri, CDT.responsibleFor, road_link_uri))
            g.add((road_link_uri, CDT.hasCustodian, gov_org_uri))

        if pd.notna(num_lanes):
            g.add((road_link_uri, ROAD.numLanes, Literal(int(num_lanes), datatype=XSD.integer)))

        if pd.notna(pavement_status):
            if pavement_status == "Paved":
                g.add((road_link_uri, CDT.pavementStatus, Literal("true", datatype=XSD.boolean)))
            else:
                g.add((road_link_uri, CDT.pavementStatus, Literal("false", datatype=XSD.boolean)))

        if pd.notna(route_name):
            g.add((road_link_uri, CDT.routeName, Literal(route_name, datatype=XSD.string)))

        if pd.notna(route_number): # Some are Alpha Numeric Values
            g.add((road_link_uri, CDT.routeNumber, Literal(str(route_number), datatype=XSD.string)))

        if pd.notna(structure_type):
            structure_type_measurement = CDT[f"structure_type_{road_id}"]
            structure_type_Code = CODE[f"structureTypeCode_{road_id}"]

            g.add((road_link_uri, CDT.hasStructureType, structure_type_measurement))
            g.add((structure_type_measurement, RDF.type, CDT.StructureType))
            g.add((structure_type_measurement, CODE.hasCode, structure_type_Code))
            g.add((structure_type_Code, RDF.type, CODE.Code))
            g.add((structure_type_Code, GEN.hasName, Literal(structure_type, datatype=XSD.string)))

        if pd.notna(toll_point_type):
            toll_type_measurement = CDT[f"tollPoint_type_{road_id}"]
            toll_type_Code = CODE[f"tollTypeCode_{road_id}"]

            g.add((road_link_uri, CDT.hasTollPointType, toll_type_measurement))
            g.add((toll_type_measurement, RDF.type, CDT.TollPointType))
            g.add((toll_type_measurement, CODE.hasCode, toll_type_Code))
            g.add((toll_type_Code, RDF.type, CODE.Code))
            g.add((toll_type_Code, GEN.hasName, Literal(toll_point_type, datatype=XSD.string)))

        if pd.notna(underpass_type):
            underpass_type_measurement = CDT[f"underpass_type_{road_id}"]
            underpass_type_Code = CODE[f"underpassTypeCode_{road_id}"]

            g.add((road_link_uri, CDT.hasUnderpassType, underpass_type_measurement))
            g.add((underpass_type_measurement, RDF.type, CDT.UnderpassType))
            g.add((underpass_type_measurement, CODE.hasCode, underpass_type_Code))
            g.add((underpass_type_Code, RDF.type, CODE.Code))
            g.add((underpass_type_Code, GEN.hasName, Literal(underpass_type, datatype=XSD.string)))


        # Add Junction relationships
        if pd.notna(from_junction_id):
            from_junction_uri = CDT[f"junction_{from_junction_id}"]
            g.add((road_link_uri, TRANSPORT["from"], from_junction_uri))
            g.add((from_junction_uri, TRANSPORT.egress, road_link_uri))

        if pd.notna(to_junction_id):
            to_junction_uri = CDT[f"junction_{to_junction_id}"]
            g.add((road_link_uri, TRANSPORT.to, to_junction_uri))
            g.add((to_junction_uri, TRANSPORT.ingress, road_link_uri))

        # Convert and add Date Fields
        for date_field, predicate in [("CREDATE", CDT.creationDate),
                                      ("REVDATE", CDT.revisionDate),
                                      ("GEO_UPD_DT", CDT.geoUpdateDate),
                                      ("EFF_DATE", CDT.effectiveDate)]:
            formatted_date = format_date(row.get(date_field))
            if formatted_date:
                g.add((road_link_uri, predicate, Literal(formatted_date, datatype=XSD.date)))

        # Geolocation
        g.add((location_uri, RDF.type, GEO_LOC.Location))
        g.add((GEO_LOC.Location, RDFS.subClassOf, GEO.Geometry))
        g.add((location_uri, GEO.asWKT, Literal(row["geometry"].wkt, datatype=GEO.wktLiteral)))
        g.add((road_link_uri, GEO_LOC.hasLocation, location_uri))

    # Creates the Road entity and adds all RoadLinks as part of the Road entity
    if road_links:
        g.add((CDT.Road, RDFS.subClassOf, INFRAS.Road))
        g.add((road_uri, RDF.type, CDT.Road))
        g.add((road_uri, GEN.hasName, Literal(road_name, datatype=XSD.string)))
        for road_link in road_links:
            g.add((road_uri, PARTWHOLE.hasProperPart, road_link))
        id += 1

# Write RDF Data to Turtle File
output_file = "toronto_roads.ttl"
g.serialize(destination=output_file, format="turtle")

print(f"Written to {output_file}")
