# -*- coding: utf-8 -*-
"""
Park.py

Author: Anderson Wong

Date: November 27, 2025

Description: This is a Python program that generates RDF triples 
for parks using OpenStreetMap data in a geojson file.
    
"""
# Import modules
import rdflib
import json
import shapely
import re
import usaddress
import geopandas

from shapely.geometry import shape
from pyproj import Geod
from rdflib import Graph, Literal, XSD, RDF

def toUpperCamelCase(string):
    """
    The toUpperCamelCase function takes a string and returns it as
    a upper camel case string (e.g., "upper camel case" -> "UpperCamelCase")
    """
    
    # Replace non-alphanumeric with spaces (so words don't merge)
    cleaned = re.sub(r'[^A-Za-z0-9]+', ' ', string)
    
    # Split into words
    words = cleaned.split()
    
    # Capitalize each word and join
    uppercamelcase = ''.join(word.capitalize() for word in words)

    return uppercamelcase

def polyareaperimeter(geometry):
    """
    The polyareaperimeter function takes a polygon geometry and returns the area and
    perimeter of the polygon 
    """
    polygon = shapely.geometry.shape(geometry)
    geod = Geod(ellps="WGS84")
    poly_area, poly_perimeter = geod.geometry_area_perimeter(polygon)
    return poly_area, poly_perimeter


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
                days += day_keys[start_idx:end_idx+1]
            else:
                days.append(item)

        for day in days:
            if day in days_map:                
                result[days_map[day]] = wrap_time_range(time_part)

    return result

# Declare namespaces
toronto = rdflib.Namespace('http://ontology.eil.utoronto.ca/Toronto/Toronto#')
genprop = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/')
cdt = rdflib.Namespace('http://ontology.eil.utoronto.ca/CDT#')
gcir = rdflib.Namespace('http://ontology.eil.utoronto.ca/GCI/Recreation/GCIRecreation.owl#')
loc = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/')
geo = rdflib.Namespace('http://www.opengis.net/ont/geosparql#')
gci = rdflib.Namespace('http://ontology.eil.utoronto.ca/GCI/Foundation/GCI-Foundation.owl#')
code = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Code/')
rdfs = rdflib.Namespace('http://www.w3.org/2000/01/rdf-schema#')
contact = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Contact/')
cityunits = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/CityUnits/')
iso21972 = rdflib.Namespace('http://ontology.eil.utoronto.ca/ISO21972/iso21972#')
schema = rdflib.Namespace('http://schema.org/')
org_city = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Organization/')
org = rdflib.Namespace('http://www.w3.org/ns/org#')
hp = rdflib.Namespace('http://ontology.eil.utoronto.ca/HPCDM/')
recurringevent = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/RecurringEvent/')
service = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/CityService/')
res = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Resource/')


# Create RDF graph
g = Graph()
g2 = Graph()

# Initialize variables
filename = "park.geojson"
amenityname = "Park"

# Get the data
parks = json.loads(open(filename, encoding='utf8').read())

# Generate triples for Park class
g.add((cdt.Park, org_city.hasIndustryType, cdt.natureParksNAICS))

g.add((cdt.natureParksNAICS, RDF.type, org_city.IndustryType))
g.add((cdt.natureParksNAICS, code.hasCode, cdt.natureParksNAICSCode))

g.add((cdt.natureParksNAICSCode, RDF.type, cdt.NAICSCode))
g.add((cdt.natureParksNAICSCode, genprop.hasName, Literal("71219 - Nature parks and other similar institutions")))
g.add((cdt.natureParksNAICSCode, genprop.hasDescription, Literal("This industry comprises establishments, not classified to any other industry, primarily engaged in operating other heritage institutions. Establishments primarily engaged in operating, maintaining and protecting nature parks, nature reserves or conservation areas, are included.")))
g.add((cdt.natureParksNAICSCode, genprop.hasIdentifier, Literal("71219")))

g.add((cdt.NAICSCode, rdfs.subClassOf, code.Code))

g.add((cdt.CDTCompleteCommunityAmenity, cdt.providesService, hp[amenityname + "Service"]))
g.add((hp[amenityname + "Service"], rdfs.subClassOf, cdt.Service))

g.add((contact.workPhone, RDF.type, contact.PhoneType))
g.add((contact.faxPhone, RDF.type, contact.PhoneType))

# Generate triple for displayColor
g.add((cdt.Park, cdt.displayColor, Literal("#24b34a")))

# Generate triples for displayProperties
g.add((cdt.Park, cdt.displayProperties, genprop.hasName))
g.add((cdt.Park, cdt.displayProperties, cdt.website))
g.add((cdt.Park, cdt.displayProperties, cdt.openingHours))
g.add((cdt.Park, cdt.displayProperties, genprop.hasIdentifier))
g.add((cdt.Park, cdt.displayProperties, org.hasSite))
g.add((cdt.Park, cdt.displayProperties, contact.hasAddress))

g.add((cdt.Site, cdt.displayProperties, cdt.lit))
g.add((cdt.Site, cdt.displayProperties, cdt.surface))
g.add((cdt.Site, cdt.displayProperties, cityunits.hasArea))

g.add((contact.Address, cdt.displayProperties, contact.hasUnitNumber))
g.add((contact.Address, cdt.displayProperties, contact.hasStreet))
g.add((contact.Address, cdt.displayProperties, contact.hasStreetType))
g.add((contact.Address, cdt.displayProperties, contact.hasStreetDirection))
g.add((contact.Address, cdt.displayProperties, contact.hasStreetNumber))
g.add((contact.Address, cdt.displayProperties, contact.hasBuilding))
g.add((contact.Address, cdt.displayProperties, contact.hasPostalBox))
g.add((contact.Address, cdt.displayProperties, contact.hasPostalCode))
g.add((contact.Address, cdt.displayProperties, contact.hasCity))
g.add((contact.Address, cdt.displayProperties, contact.hasProvince))
g.add((contact.Address, cdt.displayProperties, contact.hasCountry))

g.add((contact.PhoneNumber, cdt.displayProperties, contact.hasCountryCode))
g.add((contact.PhoneNumber, cdt.displayProperties, contact.hasAreaCode))
g.add((contact.PhoneNumber, cdt.displayProperties, contact.hasPhoneNumber))
g.add((contact.PhoneNumber, cdt.displayProperties, contact.hasPhoneType))

g.add((cityunits.Area, cdt.displayProperties, iso21972.value))

g.add((iso21972.Measure, cdt.displayProperties, iso21972.numerical_value))

# Generate an instance for Ontario and Canada
g.add((cdt.ontario, RDF.type, schema.State))
g.add((cdt.canada, RDF.type, schema.Country))

g.add((cdt[amenityname + "Site"], rdfs.subClassOf, cdt.Site))


# Generate triples for each park
for element in parks["features"]:
    # Initialize variables
    osmid = re.sub("[^0-9]", "", element["id"])
    instancename = osmid + amenityname
    addressname = instancename + "Address"
    areaname = instancename + "Area"
    areameasurename = areaname + "Measure"
    sitename = instancename + "Site"
    telephonename = instancename + "Telephone"
    faxname = instancename + "Faxphone"
    streetname = ""  
    
    # Generate triples for park
    g.add((toronto[instancename + "Org"], RDF.type, cdt.Organization))
    
    # Generate triple for identifier
    g.add((toronto[sitename], genprop.hasIdentifier, Literal(osmid)))

    # Generate triple for site
    g.add((toronto[sitename], RDF.type, cdt[amenityname + "Site"]))
    g.add((toronto[instancename + "Org"], org.hasSite, toronto[sitename]))
    g.add((toronto[sitename], loc.hasLocation, toronto[instancename + "Site" + "Loc"]))


    # Generate triple for location instance
    g.add((toronto[instancename + "Site" + "Loc"], RDF.type, loc.Location))
    g.add((toronto[instancename + "Site" + "Loc"], geo.asWKT, Literal(shapely.to_wkt(shapely.geometry.shape(element["geometry"])), datatype=geo.wktLiteral)))
    
    # Generate triples for service
    g.add((toronto[instancename + "Service"], RDF.type, cdt[amenityname + "Service"]))
    g.add((cdt.CDTCompleteCommunityAmenityToronto, cdt.providesService, toronto[instancename + "Service"]))
    g.add((toronto[instancename + "Org"], cdt.providesService, toronto[instancename + "Service"]))
    g.add((toronto[instancename + "Service"], hp.providedFromSite, toronto[sitename]))

    # Generate triples for optional properties
    # Generate triples for name
    try:    
        g.add((toronto[sitename], genprop.hasName, Literal(element['properties']['name'])))
    except:
        pass
    
    # Generate triples for operating hours
    try: 
        hours_dict = parse_opening_hours(element['properties']['opening_hours'])
        for day in hours_dict:
            operationday = sitename + "OperatingHours" + day
            g.add((toronto[instancename], org_city.openingHours, toronto[operationday]))
            g.add((toronto[operationday], RDF.type, org_city.Operation))
            g.add((toronto[operationday], org_city.hasOpeningTime, Literal(hours_dict[day].split('-')[0], datatype=XSD.time)))
            g.add((toronto[operationday], org_city.hasClosingTime, Literal(hours_dict[day].split('-')[1], datatype=XSD.time)))
            g.add((toronto[operationday], recurringevent.hasDayOfWeek, recurringevent[day.lower()]))
    except:
        pass
    
    # Generate triples for operator and organization type
    try: 
        g.add((toronto[toUpperCamelCase(element['properties']['operator'])], org.hasSubOrganization, toronto[instancename + "Org"]))
        try:
            orgtype = element['properties']['operator:type']
            if orgtype == "public" or orgtype == "government":
                g.add((toronto[toUpperCamelCase(element['properties']['operator'])], RDF.type, cdt.GovernmentOrganization))
            elif orgtype == "ngo":
                g.add((toronto[toUpperCamelCase(element['properties']['operator'])], RDF.type, cdt.NonProfitOrganization))
            elif orgtype == "private":
                g.add((toronto[toUpperCamelCase(element['properties']['operator'])], RDF.type, cdt.ForProfitOrganization))
            else:
                g.add((toronto[toUpperCamelCase(element['properties']['operator'])], RDF.type, cdt.Organization))
        except:
            g.add((toronto[toUpperCamelCase(element['properties']['operator'])], RDF.type, cdt.Organization))
    except:
        pass
    
    # Generate triples for address information
    try:
        street = usaddress.tag(element['properties']['addr:street'])
        try:
            streetname += street[0]["StreetNamePreModifier"]
        except: 
            pass
        try:
            streetname += street[0]["StreetNamePreDirectional"]
        except: 
            pass
        streetname += street[0]["StreetName"]
        g.add((toronto[addressname], contact.hasStreet, Literal(streetname)))
        try:
            g.add((toronto[addressname], contact.hasStreetType, contact[street[0]["StreetNamePostType"].lower()]))
        except:
            pass
        try:
            g.add((toronto[addressname], contact.hasStreetDirection, contact[street[0]["StreetNamePostDirectional"].lower()]))
        except:
            pass
        g.add((toronto[addressname], contact.hasCity, toronto.toronto))
        g.add((toronto[addressname], contact.hasProvince, cdt.ontario))
        g.add((toronto[addressname], contact.hasCountry, cdt.canada))
        g.add((toronto[addressname], RDF.type, contact.Address))
        g.add((toronto[sitename], org.siteAddress, toronto[addressname]))
    except:
        pass
    try:
        g.add((toronto[addressname], contact.hasStreetNumber, Literal(element['properties']['addr:housenumber'])))
    except:
        pass
    try:
        g.add((toronto[addressname], contact.hasPostalCode, Literal(element['properties']['addr:postcode'])))
    except:
        pass
     
    # Calculate surface area
    poly_area, poly_perimeter = polyareaperimeter(element["geometry"])
    
    # Generate triples for surface area
    g.add((toronto[areaname], RDF.type, cityunits.Area))
    g.add((toronto[areameasurename], RDF.type, iso21972.Measure))
    g.add((toronto[sitename], cityunits.hasArea, toronto[areaname]))
    g.add((toronto[areaname], iso21972.hasValue, toronto[areameasurename]))
    g.add((toronto[areameasurename], iso21972.hasUnit, iso21972.square_metre))
    g.add((toronto[areameasurename], iso21972.hasNumericalValue, Literal(poly_area)))
    
    # Generate triples for catchment area
    g2.add((toronto[instancename + "Service"], service.hasCatchmentArea, toronto[osmid + "Catchment"]))
    
    # Convert GeoJSON to Shapely geometry
    geom = shape(element["geometry"])
    
    # Put geometry into a GeoDataFrame with CRS = EPSG:4326 (WGS84 lat/lon)
    gdf = geopandas.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[geom])
    
    # Reproject to a meter-based CRS (UTM zone for Toronto is EPSG:32617)
    gdf = gdf.to_crs(epsg=32617)
    
    # Apply buffer of 800 meters
    gdf = gdf.buffer(800)
    
    # Convert back to WGS84
    gdf = gdf.to_crs(epsg=4326)
    
    # Generate triples for capacity data and catchment
    g2.add((toronto[osmid + "Catchment"], RDF.type, loc.Location))
    g2.add((toronto[osmid + "Catchment"], geo.asWKT, Literal(gdf.iloc[0].wkt, datatype=geo.wktLiteral)))

    g2.add((toronto[instancename + "ServiceCapacityUse"], RDF.type, hp.RecreationAreaPopulationRatio))
    g2.add((toronto[instancename + "Service"], res.capacityInUse, toronto[instancename + "ServiceCapacityUse"]))

    g2.add((toronto[instancename + "ServiceCapacityUse"], iso21972.hasValue, toronto[instancename + "ServiceCapacityUseMeasure"]))
    g2.add((toronto[instancename + "ServiceCapacityUseMeasure"], RDF.type, iso21972.Measure))
    g2.add((toronto[instancename + "ServiceCapacityUseMeasure"], iso21972.hasNumericalValue, Literal(poly_area/8855)))
    g2.add((toronto[instancename + "ServiceCapacityUseMeasure"], iso21972.hasUnit, hp.square_metres_per_person))
    
    g2.add((toronto[instancename + "ServiceCapacity"], RDF.type, hp.MinRecreationAreaPopulationRatio))
    g2.add((toronto[instancename + "Service"], res.hasCapacity, toronto[instancename + "ServiceCapacity"]))

    g2.add((toronto[instancename + "ServiceCapacity"], iso21972.hasValue, toronto[instancename + "ServiceCapacityMeasure"]))
    g2.add((toronto[instancename + "ServiceCapacityMeasure"], RDF.type, iso21972.Measure))
    g2.add((toronto[instancename + "ServiceCapacityMeasure"], iso21972.hasNumericalValue, Literal(20)))
    g2.add((toronto[instancename + "ServiceCapacityMeasure"], iso21972.hasUnit, hp.square_metres_per_person))

    
# Export the RDF graph as a .ttl file
g.serialize(destination="Parks.ttl")
g2.serialize(destination="ParksCapacity.ttl")






