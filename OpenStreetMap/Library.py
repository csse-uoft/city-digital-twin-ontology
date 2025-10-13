import json
from types import NoneType

import pandas as pd
import re
from rdflib import Graph, Namespace, Literal, RDFS
from rdflib.namespace import RDF, XSD
from shapely.geometry import shape


# Reload data files
geojson_path = "Library.geojson"
csv_path = "tpl-branch-general-information-2023.csv"

with open(geojson_path, encoding="utf8") as f:
    geojson_data = json.load(f)

tpl_df = pd.read_csv(csv_path)

# Define namespaces
ORG = Namespace("https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Organization/")
CONTACT = Namespace("https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Contact/")
GENPROP = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/")
LOC = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/")
CDT = Namespace("http://ontology.eil.utoronto.ca/CDT#")
CODE = Namespace("https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Code/")
CITY = Namespace("https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/City/")
RECURRINGEVENT = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/RecurringEvent/")
GEO_LOC = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
CEN = Namespace("http://ontology.eil.utoronto.ca/tove/cacensus#")
TORONTO = Namespace("http://ontology.eil.utoronto.ca/Toronto/Toronto#")

# Create RDF graph
g = Graph()
g.bind("org", ORG)
g.bind("contact", CONTACT)
g.bind("genprop", GENPROP)
g.bind("loc", LOC)
g.bind("cdt", CDT)
g.bind("code", CODE)
g.bind("city", CITY)
g.bind("recurringevent", RECURRINGEVENT)
g.bind('loc', GEO_LOC)
g.bind('geo', GEO)
g.bind('uoft', CEN)
g.bind('toronto', TORONTO)

g.add((CDT.Library, RDFS.subClassOf, CDT.GovernmentOrganization))
g.add((CDT.GovernmentOrganization, RDFS.subClassOf, ORG.GovernmentOrganization))
g.add((ORG.GovernmentOrganization, RDFS.subClassOf, ORG.Organization))

tpl_uri = CDT[f"Toronto_Public_Library_1"]

g.add((tpl_uri, RDF.type, ORG.GovernmentOrganization))
g.add((CDT.LibraryService, RDFS.subClassOf, CDT.Service))


tpl_library = []
# TPL entries
for _, row in tpl_df.iterrows():
    branch_uri = CDT[f"library_{row['_id']}"]
    g.add((branch_uri, GENPROP.hasIdentifier, Literal(row['_id'], datatype=XSD.string)))
    g.add((branch_uri, RDF.type, CDT.Library))
    g.add((branch_uri, CDT.branchCode, Literal(row['BranchCode'], datatype=XSD.string)))

    if row['PhysicalBranch'] == 1:
        g.add((branch_uri, CDT.isPublic, Literal('true', datatype=XSD.boolean)))
    else:
        g.add((branch_uri, CDT.isPublic, Literal('false', datatype=XSD.boolean)))
        continue

    branch_add_uri = CDT[f"addLibrary_{row['_id']}"]
    province_uri = CONTACT[f"state_{row['_id']}"]
    code_uri = CODE[f"state_Code_{row['_id']}"]

    g.add((branch_add_uri, RDF.type, CONTACT.Address))
    g.add((branch_uri, GENPROP.hasName, Literal(row['BranchName'], datatype=XSD.string)))
    g.add((branch_uri, CONTACT.hasAddress, branch_add_uri))

    g.add((province_uri, RDF.type, CONTACT.State))
    g.add((code_uri, RDF.type, CODE.Code))
    g.add((province_uri, CODE.hasCode, code_uri))
    g.add((code_uri, GENPROP.hasName, Literal('Ontario', datatype=XSD.string)))
    g.add((branch_add_uri, CONTACT.hasProvince, province_uri))

    if isinstance(row['Address'], str):
        address = row['Address'].split(',')

        g.add((branch_add_uri, CONTACT.hasStreet, Literal(address[0].split()[1:], datatype=XSD.string)))

        if address[0].split()[0].isdigit():
            g.add((branch_add_uri, CONTACT.hasStreetNumber, Literal((address[0].split()[0]), datatype=XSD.string)))
        else:
            g.add((branch_add_uri, CONTACT.hasStreetNumber, Literal((address[1].split()[0]), datatype=XSD.string)))

        city_uri = CITY[f"city_{row['_id']}"]
        g.add((branch_add_uri, CONTACT.hasCity, city_uri))
        g.add((city_uri, RDF.type, CITY.City))
        g.add((city_uri, CONTACT.legalName, Literal(address[1], datatype=XSD.string)))

    g.add((branch_add_uri, CONTACT.hasPostalCode, Literal(row['PostalCode'], datatype=XSD.string)))

    phone_uri = CONTACT[f"phone_{row['_id']}"]
    g.add((phone_uri, RDF.type, CONTACT.PhoneNumber))
    g.add((branch_uri, CONTACT.hasTelephone, phone_uri))
    g.add((phone_uri, CONTACT.hasTelephoneNumber, Literal(row['Telephone'].replace("-", ""), datatype=XSD.nonNegativeInteger)))
    g.add((branch_uri, CDT.hasWebsite, Literal(row['Website'], datatype=XSD.string)))

    site_uri = CDT[f"site_{row['_id']}"]
    g.add((site_uri, RDF.type, CDT.Site))
    g.add((CDT.Site, RDFS.subClassOf, ORG.Site))
    g.add((branch_uri, ORG.hasSite, site_uri))

    g.add((site_uri, CDT.squareFootage, Literal(int(row['SquareFootage']), datatype=XSD.integer)))

    if row['PublicParking'] != 'shared':
        g.add((site_uri, CDT.numParking, Literal(int(row['PublicParking']), datatype=XSD.integer)))
        g.add((site_uri, CDT.hasSharedParking, Literal('false', datatype=XSD.boolean)))
    else:
        g.add((site_uri, CDT.hasSharedParking, Literal('true', datatype=XSD.boolean)))

    g.add((site_uri, CDT.numComputers, Literal(int(row['Workstations']), datatype=XSD.integer)))
    g.add((site_uri, CDT.openingYear, Literal(int(row['PresentSiteYear']), datatype=XSD.year)))

    service_tier = CDT[f"serviceTier_{row['_id']}"]
    tier_code = CODE[f"tierCode_{row['_id']}"]

    g.add((site_uri, CDT.hasServiceTier, service_tier))
    g.add((service_tier, RDF.type, CDT.ServiceTier))
    g.add((service_tier, CODE.hasCode, tier_code))
    g.add((tier_code, RDF.type, CODE.Code))
    g.add((tier_code, GENPROP.hasName, Literal(row['ServiceTier'], datatype=XSD.string)))

    if row['KidsStop'] == 1:
        kid_uri = CDT[f"kids_stop_{row['_id']}"]
        g.add((kid_uri, RDF.type, CDT.LibraryService))
        g.add((site_uri, CDT.providesService, kid_uri))
        g.add((kid_uri, GENPROP.hasName, Literal('KidsStop', datatype=XSD.string)))

    if row['TPLNIA'] == 1:
        tplnia_uri = CDT[f"tplnia_serv_{row['_id']}"]
        g.add((tplnia_uri, RDF.type, CDT.LibraryService))
        g.add((site_uri, CDT.providesService, tplnia_uri))
        g.add((tplnia_uri, GENPROP.hasName, Literal('TPLNIA', datatype=XSD.string)))

    if row['LeadingReading'] == 1:
        lr_uri = CDT[f"leadingReading_serv_{row['_id']}"]
        g.add((lr_uri, RDF.type, CDT.LibraryService))
        g.add((site_uri, CDT.providesService, lr_uri))
        g.add((lr_uri, GENPROP.hasName, Literal('LeadingReading', datatype=XSD.string)))

    if row['CLC'] == 1:
        clc_uri = CDT[f"clc_serv_{row['_id']}"]
        g.add((clc_uri, RDF.type, CDT.LibraryService))
        g.add((site_uri, CDT.providesService, clc_uri))
        g.add((clc_uri, GENPROP.hasName, Literal('CLC', datatype=XSD.string)))

    if row['DIH'] == 1:
        dih_uri = CDT[f"dih_serv_{row['_id']}"]
        g.add((dih_uri, RDF.type, CDT.LibraryService))
        g.add((site_uri, CDT.providesService, dih_uri))
        g.add((dih_uri, GENPROP.hasName, Literal('DIH', datatype=XSD.string)))

    if row['TeenCouncil'] == 1:
        tc_uri = CDT[f"teenCouncil_serv_{row['_id']}"]
        g.add((tc_uri, RDF.type, CDT.LibraryService))
        g.add((site_uri, CDT.providesService, tc_uri))
        g.add((tc_uri, GENPROP.hasName, Literal('TeenCouncil', datatype=XSD.string)))

    if row['YouthHub'] == 1:
        yh_uri = CDT[f"youthHub_serv_{row['_id']}"]
        g.add((yh_uri, RDF.type, CDT.LibraryService))
        g.add((site_uri, CDT.providesService, yh_uri))
        g.add((yh_uri, GENPROP.hasName, Literal('YouthHub', datatype=XSD.string)))

    if row['AdultLiteracyProgram'] == 1:
        alp_uri = CDT[f"adultLiteracy_serv_{row['_id']}"]
        g.add((alp_uri, RDF.type, CDT.LibraryService))
        g.add((site_uri, CDT.providesService, alp_uri))
        g.add((alp_uri, GENPROP.hasName, Literal('AdultLiteracyProgram', datatype=XSD.string)))

    g.add((tpl_uri, ORG.hasSubOrganization, branch_uri))

    neig_location_uri = TORONTO[f"neighbourhood_{row['_id']}"]
    location_uri = GEO_LOC[f"location_{row['_id']}"]
    ward_uri = TORONTO[f"ward_{row['_id']}"]

    g.add((location_uri, CDT.contains, neig_location_uri))
    g.add((neig_location_uri, RDF.type, TORONTO.Neighbourhood))
    g.add((TORONTO.Neighbourhood, RDFS.subClassOf, CITY.CityAdministrativeArea))
    g.add((ward_uri, RDF.type, TORONTO.Ward))
    g.add((TORONTO.Ward, RDFS.subClassOf, CITY.CityAdministrativeArea))

    g.add((neig_location_uri, GENPROP.hasName, Literal(row['NBHDName'], datatype=XSD.string)))
    g.add((neig_location_uri, CDT.nbhdNum, Literal(int(row['NBHDNo']), datatype=XSD.integer)))
    g.add((neig_location_uri, TORONTO.inWard, ward_uri))
    g.add((ward_uri, TORONTO.hasNeighbourhood, neig_location_uri))
    g.add((ward_uri, GENPROP.hasName, Literal(row['WardName'], datatype=XSD.string)))
    g.add((ward_uri, CDT.wardNum, Literal(int(row['WardNo']), datatype=XSD.integer)))

    g.add((site_uri, GEO_LOC.hasLocation, location_uri))
    wkt_point = f"POINT ({row['Long']} {row['Lat']})"
    g.add((location_uri, GEO.asWKT, Literal(wkt_point, datatype=GEO.wktLiteral)))

    tpl_library.append([row['BranchName'], branch_uri, site_uri, row['_id']])

def wrap_time_range(range_str):
    """
    Converts a time range (e.g., 20:00-26:00) to a time range that is compatible with
    XSD time format (e.g., 20:00-02:00)
    """
    start_str, end_str = range_str.split("-")

    def wrap_time(time_str):
        hours, minutes = map(int, time_str.split(":"))
        hours %= 24
        return f"{hours:02}:{minutes:02}"

    return f"{wrap_time(start_str)}-{wrap_time(end_str)}"

def parse_opening_hours(opening_str):
    """
    Parses an opening_hours string into a dictionary mapping day codes
    ('Mo', 'Tu', ...) to 'HH:MM-HH:MM' values. Skips days marked 'off'.

     output: { 'Mo': '08:30-23:00', 'Tu': '08:30-23:00', ... }
    """
    if opening_str == "24/7":
        opening_str = "Mo-Su 00:00-24:00"

    days_map = {
        'Mo': 'Monday',
        'Tu': 'Tuesday',
        'We': 'Wednesday',
        'Th': 'Thursday',
        'Fr': 'Friday',
        'Sa': 'Saturday',
        'Su': 'Sunday'
    }

    result = {}

    parts = [p.strip() for p in opening_str.split(';') if p.strip()]

    for part in parts:

        # Skip if it is a monthly operating time or if it is closed (i.e., "off")
        if re.search(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b', part):
            continue
        if 'off' in part.lower():
            continue

            # Extract day and time portion (e.g. "Mo-Fr 09:00-18:00")
        match = re.match(r'([A-Za-z,-]+)\s+([\d:]+-[\d:]+)', part)
        if not match:
            continue

        days_part, time_part = match.groups()

        days = []
        for item in days_part.split(','):
            if '-' in item:
                start_day, end_day = item.split('-')
                day_keys = list(days_map.keys())
                start_idx = day_keys.index(start_day)
                end_idx = day_keys.index(end_day)
                days += day_keys[start_idx:end_idx + 1]
            else:
                days.append(item)

        for day in days:
            if day in days_map:
                result[days_map[day]] = wrap_time_range(time_part)

    return result


#GeoJSON entries
for feature in geojson_data["features"]:
    props = feature["properties"]
    name = props.get("name")
    loc = feature['geometry']
    geometry = shape(loc)

    match_index = None
    match_entry = None

    for idx, entry in enumerate(tpl_library):
        if entry[0] is not None and name is not None:  # avoid NoneType errors
            if entry[0] in name:  # check if name is substring
                match_index = idx
                match_entry = entry
                break

    if match_entry:
        site_uri = tpl_library[match_index][2]
        branch_uri = tpl_library[match_index][1]
        id = tpl_library[match_index][3]

        if "addr:floor" in props:
            g.add((site_uri, CDT.numFloors, Literal(int(props['addr:floor']), datatype=XSD.integer)))

        if "after_hours_return" in props:
            if props["after_hours_return"] == 'yes':
                g.add((site_uri, CDT.afterHoursReturns, Literal('true', datatype=XSD.boolean)))
            else:
                g.add((site_uri, CDT.afterHoursReturns, Literal('false', datatype=XSD.boolean)))

        if "air_conditioning" in props:
            if props["air_conditioning"] == 'yes':
                g.add((site_uri, CDT.airConditioning, Literal('true', datatype=XSD.boolean)))
            else:
                g.add((site_uri, CDT.airConditioning, Literal('false', datatype=XSD.boolean)))

        if "architect" in props:
            g.add((site_uri, CDT.architect, Literal((props['architect']), datatype=XSD.string)))

        if "building" in props:
            if props["building"] == 'yes':
                g.add((branch_uri, CDT.isPublic, Literal('true', datatype=XSD.boolean)))
            else:
                g.add((site_uri, CDT.hasBuildingType, Literal(props['building'], datatype=XSD.string)))

        if "building:colour" in props:
            color_uri = CDT[f"color_{props['building:colour']}"]
            code_uri = CODE[f"color_Code_{props['building:colour']}"]

            g.add((color_uri, RDF.type, CDT.Color))
            g.add((code_uri, RDF.type, CODE.Code))
            g.add((color_uri, CODE.hasCode, code_uri))
            g.add((code_uri, GENPROP.hasName, Literal(props['building:colour'], datatype=XSD.string)))
            g.add((site_uri, CDT.hasColor, color_uri))

        if "building:material" in props:
            material_uri = CDT[f"material_{props['building:material']}"]
            code_uri = CODE[f"material_Code_{props['building:material']}"]

            g.add((material_uri, RDF.type, CDT.Material))
            g.add((code_uri, RDF.type, CODE.Code))
            g.add((material_uri, CODE.hasCode, code_uri))
            g.add((code_uri, GENPROP.hasName, Literal(props['building:material'], datatype=XSD.string)))
            g.add((site_uri, CDT.hasColor, material_uri))
            g.add((site_uri, CDT.madeOf, Literal((props['building:material']), datatype=XSD.string)))

        if "capacity" in props:
            g.add((site_uri, CDT.capacity, Literal(int(props['capacity'].split()[0]), datatype=XSD.integer)))

        if "check_date" in props:
            g.add((site_uri, CDT.revisionDate, Literal((props['check_date']), datatype=XSD.date)))

        if "department" in props:
            g.add((site_uri, CDT.department, Literal((props['department']), datatype=XSD.string)))

        if "description" in props:
            g.add((site_uri, GENPROP.hasDescription, Literal((props['description']), datatype=XSD.string)))

        if "email" in props:
            email_uri = CDT[f"email_{id}"]
            g.add((email_uri, RDF.type, CDT.Email))
            g.add((site_uri, CDT.hasEmail, email_uri))
            g.add((email_uri, CDT.emailAddress, Literal((props['email']), datatype=XSD.string)))

        if "height" in props:
            g.add((site_uri, CDT.height, Literal((props['height']), datatype=XSD.string)))

        if "internet_access" in props:
            g.add((site_uri, CDT.hasWIFI, Literal((props['internet_access']), datatype=XSD.string)))

        if "internet_access:fee" in props:
            if props['internet_access:fee'] == 'yes':
                g.add((site_uri, CDT.hasPaidWIFI, Literal('true', datatype=XSD.string)))
            else:
                g.add((site_uri, CDT.hasPaidWIFI, Literal('false', datatype=XSD.string)))

        if "internet_access:ssid" in props:
            g.add((site_uri, CDT.ssid, Literal((props['internet_access:ssid']), datatype=XSD.string)))

        if "min_height" in props:
            g.add((site_uri, CDT.minHeight, Literal(int(props['min_height']), datatype=XSD.integer)))

        if "name:fr" in props:
            g.add((branch_uri, CDT.frName, Literal(props['name:fr'], datatype=XSD.string)))

        if "name:ta" in props:
            g.add((branch_uri, CDT.taName, Literal(props['name:ta'], datatype=XSD.string)))

        if "name:zh" in props:
            g.add((branch_uri, CDT.zhName, Literal(props['name:zh'], datatype=XSD.string)))

        if "note" in props:
            g.add((site_uri, GENPROP.hasDescription, Literal(props['note'], datatype=XSD.string)))

        if "opening_hours" in props:
            hours_dict = parse_opening_hours(props['opening_hours'])
            for day in hours_dict:
                hours_uri = ORG[f'{day}_{id}']
                g.add((branch_uri, ORG.operatingHours, hours_uri))
                g.add((hours_uri, RDF.type, ORG.Operation))
                g.add((hours_uri, ORG.hasOpeningTime, Literal(hours_dict[day].split('-')[0], datatype=XSD.time)))
                g.add((hours_uri, ORG.hasClosingTime, Literal(hours_dict[day].split('-')[1], datatype=XSD.time)))
                g.add((hours_uri, RECURRINGEVENT.hasDayofWeek, Literal(day, datatype=XSD.string)))

        if "operator" in props:
            if props["operator"] != "Toronto Public Library":
                operator_uri = ORG[f'{props["operator"].replace(" ", "_")}']
                g.add((operator_uri, ORG.hasSubOrganization, branch_uri))
            else:
                g.add((tpl_uri, ORG.hasSubOrganization, branch_uri))

            if "operator:type" in props:
                operator_uri = ORG[f'{props["operator"].replace(" ", "_")}']
                if props['operator:type'] == 'government':
                    g.add((operator_uri, RDF.type, ORG.GovernmentOrganization))
                else:
                    g.add((operator_uri, RDF.type, ORG.Organization))

        if "parking" in props:
            parking_uri = CDT[f"parking_{id}"]
            code_uri = CODE[f"parking_Code_{id}"]

            g.add((parking_uri, RDF.type, CDT.ParkingType))
            g.add((code_uri, RDF.type, CODE.Code))
            g.add((parking_uri, CODE.hasCode, code_uri))
            g.add((code_uri, GENPROP.hasName, Literal(props['parking'], datatype=XSD.string)))
            g.add((site_uri, CDT.hasParkingType, parking_uri))

        if "return_machine" in props:
            if props['return_machine'] == "yes":
                g.add((site_uri, CDT.returnMachine, Literal('true', datatype=XSD.boolean)))
            else:
                g.add((site_uri, CDT.returnMachine, Literal('false', datatype=XSD.boolean)))

        if "roof:colour" in props:
            color_uri = CDT[f"color_{props['roof:colour']}"]
            code_uri = CODE[f"color_Code_{props['roof:colour']}"]

            g.add((color_uri, RDF.type, CDT.Color))
            g.add((code_uri, RDF.type, CODE.Code))
            g.add((color_uri, CODE.hasCode, code_uri))
            g.add((code_uri, GENPROP.hasName, Literal(props['roof:colour'], datatype=XSD.string)))
            g.add((site_uri, CDT.roofColor, color_uri))

        if "roof:material" in props:
            material_uri = CDT[f"material_{props['roof:material']}"]
            code_uri = CODE[f"material_Code_{props['roof:material']}"]

            g.add((material_uri, RDF.type, CDT.Material))
            g.add((code_uri, RDF.type, CODE.Code))
            g.add((material_uri, CODE.hasCode, code_uri))
            g.add((code_uri, GENPROP.hasName, Literal(props['roof:material'], datatype=XSD.string)))
            g.add((site_uri, CDT.hasColor, material_uri))
            g.add((site_uri, CDT.roofMaterial, Literal((props['roof:material']), datatype=XSD.string)))

        if "self_checkout" in props:
            if props['self_checkout'] == "yes":
                g.add((site_uri, CDT.hasSelfCheckout, Literal('true', datatype=XSD.boolean)))
            else:
                g.add((site_uri, CDT.hasSelfCheckout, Literal('false', datatype=XSD.boolean)))

        if "source" in props:
            g.add((branch_uri, CDT.dataSource, Literal((props['source']), datatype=XSD.string)))

        if "stars" in props:
            g.add((site_uri, CDT.rating, Literal(float(props['stars']), datatype=XSD.float)))

        if "stars:system" in props:
            g.add((site_uri, CDT.rating, Literal(float(props['stars:system'].split()[0]), datatype=XSD.string)))

        if "start_date" in props:
            g.add((site_uri, CDT.openingYear, Literal((props['start_date']), datatype=XSD.year)))

        if "toilets" in props:
            if props['toilets'] == "yes":
                g.add((site_uri, CDT.hasToilets, Literal('true', datatype=XSD.boolean)))
            else:
                g.add((site_uri, CDT.hasToilets, Literal('false', datatype=XSD.boolean)))

        if "website" in props:
            g.add((branch_uri, CDT.website, Literal(props['website'], datatype=XSD.string)))

        if "wheelchair" in props:
            if props['wheelchair'] != 'no':
                g.add((site_uri, CDT.wheelchairAccess, Literal('true', datatype=XSD.string)))
            else:
                g.add((site_uri, CDT.wheelchairAccess, Literal('false', datatype=XSD.string)))
    else:
        if "@id" in props:
            id = props['@id'].split('/')[1]
            branch_uri = CDT[f"library_{id}"]
            g.add((branch_uri, GENPROP.hasIdentifier, Literal(id, datatype=XSD.string)))
            g.add((branch_uri, RDF.type, CDT.Library))

            site_uri = CDT[f"site_{id}"]
            g.add((site_uri, RDF.type, CDT.Site))
            g.add((CDT.Site, RDFS.subClassOf, ORG.Site))
            g.add((branch_uri, ORG.hasSite, site_uri))

            branch_add_uri = CDT[f"addLibrary_{id}"]
            g.add((branch_add_uri, RDF.type, CONTACT.Address))
            g.add((branch_uri, CONTACT.hasAddress, branch_add_uri))

            location_uri = GEO_LOC[f"location_{id}"]
            g.add((site_uri, GEO_LOC.hasLocation, location_uri))
            g.add((location_uri, RDF.type, GEO_LOC.Location))
            g.add((GEO_LOC.Location, RDFS.subClassOf, GEO.Geometry))
            g.add((location_uri, GEO.asWKT, Literal(geometry, datatype=GEO.wktLiteral)))

        if "access" in props:
            if props["access"] == 'yes':
                g.add((branch_uri, CDT.isPublic, Literal('true', datatype=XSD.boolean)))
            if props["access"] == 'no':
                g.add((branch_uri, CDT.isPublic, Literal('false', datatype=XSD.boolean)))

        if "addr:city" in props:
            city_uri = CITY[f"city_{id}"]
            g.add((branch_add_uri, CONTACT.hasCity, city_uri))
            g.add((city_uri, RDF.type, CITY.City))
            g.add((city_uri, CONTACT.legalName, Literal(props["addr:city"], datatype=XSD.string)))

        if "addr:floor" in props:
            g.add((site_uri, CDT.numFloors, Literal(int(props['addr:floor']), datatype=XSD.integer)))

        if "addr:housename" in props:
            g.add((branch_uri, GENPROP.hasName, Literal(props['addr:housename'], datatype=XSD.string)))

        if "addr:housenumber" in props: # String since some houseNumbers are alpha numeric codes
            g.add((branch_add_uri, CONTACT.hasStreetNumber, Literal((props['addr:housenumber']), datatype=XSD.string)))

        if "addr:postcode" in props:
            g.add((branch_add_uri, CONTACT.hasPostalCode, Literal((props['addr:postcode']), datatype=XSD.string)))

        if "addr:province" in props:
            province_uri = CONTACT[f"state_{id}"]
            code_uri = CODE[f"state_Code_{id}"]

            g.add((province_uri, RDF.type, CONTACT.State))
            g.add((code_uri, RDF.type, CODE.Code))
            g.add((province_uri, CODE.hasCode, code_uri))
            g.add((code_uri, GENPROP.hasName, Literal('Ontario', datatype=XSD.string)))
            g.add((branch_add_uri, CONTACT.hasProvince, province_uri))

        if "addr:street" in props:
            g.add((branch_add_uri, CONTACT.hasStreet, Literal((props['addr:street']), datatype=XSD.string)))

        if "after_hours_return" in props:
            if props["after_hours_return"] == 'yes':
                g.add((site_uri, CDT.afterHoursReturns, Literal('true', datatype=XSD.boolean)))
            else:
                g.add((site_uri, CDT.afterHoursReturns, Literal('false', datatype=XSD.boolean)))

        if "air_conditioning" in props:
            if props["air_conditioning"] == 'yes':
                g.add((site_uri, CDT.airConditioning, Literal('true', datatype=XSD.boolean)))
            else:
                g.add((site_uri, CDT.airConditioning, Literal('false', datatype=XSD.boolean)))


        if "architect" in props:
            g.add((site_uri, CDT.architect, Literal((props['architect']), datatype=XSD.string)))


        if "building" in props:
            if props["building"] == 'yes':
                g.add((branch_uri, CDT.isPublic, Literal('true', datatype=XSD.boolean)))
            else:
                buildingtype_uri = CDT[f"buildingType_{props['building']}"]
                code_uri = CODE[f"buildingType_Code_{props['building']}"]

                g.add((buildingtype_uri, RDF.type, CDT.BuildingType))
                g.add((code_uri, RDF.type, CODE.Code))
                g.add((buildingtype_uri, CODE.hasCode, code_uri))
                g.add((code_uri, GENPROP.hasName, Literal(props['building'], datatype=XSD.string)))
                g.add((site_uri, CDT.hasBuildingType, buildingtype_uri))

        if "building:colour" in props:
            color_uri = CDT[f"color_{props['building:colour']}"]
            code_uri = CODE[f"color_Code_{props['building:colour']}"]

            g.add((color_uri, RDF.type, CDT.Color))
            g.add((code_uri, RDF.type, CODE.Code))
            g.add((color_uri, CODE.hasCode, code_uri))
            g.add((code_uri, GENPROP.hasName, Literal(props['building:colour'], datatype=XSD.string)))
            g.add((site_uri, CDT.hasColor, color_uri))

        if "building:material" in props:
            material_uri = CDT[f"material_{props['building:material']}"]
            code_uri = CODE[f"material_Code_{props['building:material']}"]

            g.add((material_uri, RDF.type, CDT.Material))
            g.add((code_uri, RDF.type, CODE.Code))
            g.add((material_uri, CODE.hasCode, code_uri))
            g.add((code_uri, GENPROP.hasName, Literal(props['building:material'], datatype=XSD.string)))
            g.add((site_uri, CDT.madeOf, Literal((props['building:material']), datatype=XSD.string)))

        if "built_date" in props:
            g.add((site_uri, CDT.openingYear, Literal((props['built_date']), datatype=XSD.year)))

        if "capacity" in props:
            g.add((site_uri, CDT.capacity, Literal(int(props['capacity'].split()[0]), datatype=XSD.integer)))

        if "check_date" in props:
            g.add((site_uri, CDT.revisionDate, Literal((props['check_date']), datatype=XSD.date)))


        if "description" in props:
            g.add((site_uri, GENPROP.hasDescription, Literal((props['description']), datatype=XSD.string)))

        if "email" in props:
            email_uri = CDT[f"email_{id}"]
            g.add((email_uri, RDF.type, CDT.Email))
            g.add((site_uri, CDT.hasEmail, email_uri))
            g.add((email_uri, CDT.emailAddress, Literal((props['email']), datatype=XSD.string)))

        if "height" in props:
            g.add((site_uri, CDT.height, Literal((props['height']), datatype=XSD.string)))

        if "internet_access" in props:
            if props["internet_access"] != "no":
                g.add((site_uri, CDT.hasInternetAccess, Literal('true', datatype=XSD.boolean)))
            else:
                g.add((site_uri, CDT.hasInternetAccess, Literal('false', datatype=XSD.boolean)))

        if "internet_access:fee" in props:
            if props['internet_access:fee'] == 'yes':
                g.add((site_uri, CDT.hasPaidWIFI, Literal('true', datatype=XSD.boolean)))
            else:
                g.add((site_uri, CDT.hasPaidWIFI, Literal('false', datatype=XSD.boolean)))

        if "internet_access:ssid" in props:
            g.add((site_uri, CDT.ssid, Literal((props['internet_access:ssid']), datatype=XSD.string)))

        if "min_height" in props:
            g.add((site_uri, CDT.minHeight, Literal(int(props['min_height']), datatype=XSD.integer)))

        if "name" in props:
            g.add((branch_uri, GENPROP.hasName, Literal(props['name'], datatype=XSD.string)))

        if "name:fr" in props:
            g.add((branch_uri, CDT.frName, Literal(props['name:fr'], datatype=XSD.string)))

        if "name:ta" in props:
            g.add((branch_uri, CDT.taName, Literal(props['name:ta'], datatype=XSD.string)))

        if "name:zh" in props:
            g.add((branch_uri, CDT.zhName, Literal(props['name:zh'], datatype=XSD.string)))

        if "note" in props:
            g.add((site_uri, GENPROP.hasDescription, Literal(props['note'], datatype=XSD.string)))

        if "opening_hours" in props:
            hours_dict = parse_opening_hours(props['opening_hours'])
            for day in hours_dict:
                    hours_uri = ORG[f'{day}_{id}']
                    g.add((branch_uri, ORG.operatingHours, hours_uri))
                    g.add((hours_uri, RDF.type, ORG.Operation))
                    g.add((hours_uri, ORG.hasOpeningTime, Literal(hours_dict[day].split('-')[0], datatype=XSD.time)))
                    g.add((hours_uri, ORG.hasClosingTime, Literal(hours_dict[day].split('-')[1], datatype=XSD.time)))
                    g.add((hours_uri, RECURRINGEVENT.hasDayofWeek, Literal(day, datatype=XSD.string)))

        if "operator" in props:
            if props["operator"] != "Toronto Public Library":
                operator_uri = ORG[f'{props["operator"].replace(" ", "_")}']
                g.add((operator_uri, ORG.hasSubOrganization, branch_uri))
            else:
                g.add((tpl_uri, ORG.hasSubOrganization, branch_uri))

            if "operator:type" in props:
                operator_uri = ORG[f'{props["operator"].replace(" ", "_")}']
                if props['operator:type'] == 'government':
                    g.add((operator_uri, RDF.type, ORG.GovernmentOrganization))
                else:
                    g.add((operator_uri, RDF.type, ORG.Organization))

        if "parking" in props:
            parking_uri = CDT[f"parking_{props['parking']}"]
            code_uri = CODE[f"parking_Code_{props['parking']}"]

            g.add((parking_uri, RDF.type, CDT.ParkingType))
            g.add((code_uri, RDF.type, CODE.Code))
            g.add((parking_uri, CODE.hasCode, code_uri))
            g.add((code_uri, GENPROP.hasName, Literal(props['parking'], datatype=XSD.string)))
            g.add((site_uri, CDT.hasParkingType, parking_uri))

        if "phone" in props:
            phone_uri = CONTACT[f"phone_{id}"]
            g.add((phone_uri, RDF.type, CONTACT.PhoneNumber))
            g.add((branch_uri, CONTACT.hasTelephone, phone_uri))
            g.add((phone_uri, CONTACT.hasTelephoneNumber, Literal(((props['phone'].replace("-", "")).replace("+", ""))
                                                                  .replace(" ", ""), datatype=XSD.nonNegativeInteger)))

        if "ref" in props:
            g.add((branch_uri, CDT.branchCode, Literal(props['ref'], datatype=XSD.string)))

        if "return_machine" in props:
            if props['return_machine'] == "yes":
                g.add((site_uri, CDT.returnMachine, Literal('true', datatype=XSD.boolean)))
            else:
                g.add((site_uri, CDT.returnMachine, Literal('false', datatype=XSD.boolean)))

        if "roof:colour" in props:
            color_uri = CDT[f"color_{props['roof:colour']}"]
            code_uri = CODE[f"color_Code_{props['roof:colour']}"]

            g.add((color_uri, RDF.type, CDT.Color))
            g.add((code_uri, RDF.type, CODE.Code))
            g.add((color_uri, CODE.hasCode, code_uri))
            g.add((code_uri, GENPROP.hasName, Literal(props['roof:colour'], datatype=XSD.string)))
            g.add((site_uri, CDT.roofColor, color_uri))

        if "roof:material" in props:
            material_uri = CDT[f"material_{props['roof:material']}"]
            code_uri = CODE[f"material_Code_{props['roof:material']}"]

            g.add((material_uri, RDF.type, CDT.Material))
            g.add((code_uri, RDF.type, CODE.Code))
            g.add((material_uri, CODE.hasCode, code_uri))
            g.add((code_uri, GENPROP.hasName, Literal(props['roof:material'], datatype=XSD.string)))
            g.add((site_uri, CDT.hasColor, material_uri))
            g.add((site_uri, CDT.roofMaterial, Literal((props['roof:material']), datatype=XSD.string)))

        if "self_checkout" in props:
            if props['self_checkout'] == "yes":
                g.add((site_uri, CDT.hasSelfCheckout, Literal('true', datatype=XSD.boolean)))
            else:
                g.add((site_uri, CDT.hasSelfCheckout, Literal('false', datatype=XSD.boolean)))

        if "source" in props:
            g.add((branch_uri, CDT.dataSource, Literal((props['source']), datatype=XSD.string)))

        if "stars" in props:
            g.add((site_uri, CDT.rating, Literal(float(props['stars']), datatype=XSD.float)))

        if "stars:system" in props:
            g.add((site_uri, CDT.rating, Literal(float(props['stars:system'].split()[0]), datatype=XSD.string)))

        if "start_date" in props:
            g.add((site_uri, CDT.openingYear, Literal((props['start_date']), datatype=XSD.year)))

        if "toilets" in props:
            if props['toilets'] == "yes":
                g.add((site_uri, CDT.hasToilets, Literal('true', datatype=XSD.boolean)))
            else:
                g.add((site_uri, CDT.hasToilets, Literal('false', datatype=XSD.boolean)))

        if "website" in props:
            g.add((branch_uri, CDT.website, Literal(props['website'], datatype=XSD.string)))

        if "wheelchair" in props:
            if props['wheelchair'] != 'no':
                g.add((site_uri, CDT.wheelchairAccess, Literal('true', datatype=XSD.string)))
            else:
                g.add((site_uri, CDT.wheelchairAccess, Literal('false', datatype=XSD.string)))


# Save to TTL
ttl_output_path = "toronto_libraries.ttl"
g.serialize(destination=ttl_output_path, format="turtle")
ttl_output_path

