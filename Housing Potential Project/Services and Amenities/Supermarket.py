# -*- coding: utf-8 -*-
"""
Supermarket.py

Author: Anderson Wong

Date: March 19, 2025

Description: This is a Python program that generates RDF triples 
for supermarkets using OpenStreetMap data in a geojson file.
    
"""

# Import modules
import rdflib
import json
import rdftools
import re
import geopandas
import shapely
import usaddress
import phonenumbers
import pandas

from shapely.validation import make_valid
from shapely.geometry import shape
from rdflib import Graph, Literal, XSD, RDF

# Declare namespaces
toronto = rdflib.Namespace('http://ontology.eil.utoronto.ca/Toronto/Toronto#')
genprop = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/')
cdt = rdflib.Namespace('http://ontology.eil.utoronto.ca/CDT#')
gcir = rdflib.Namespace('http://ontology.eil.utoronto.ca/GCI/Recreation/GCIRecreation.owl#')
loc = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/')
geo = rdflib.Namespace('http://www.opengis.net/ont/geosparql#')
gci = rdflib.Namespace('http://ontology.eil.utoronto.ca/GCI/Foundation/GCI-Foundation.owl#')
code = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Code/')
gcie = rdflib.Namespace('http://ontology.eil.utoronto.ca/GCI/Education/GCI-Education.owl#')
rdfs = rdflib.Namespace('http://www.w3.org/2000/01/rdf-schema#')
contact = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Contact/')
org_city = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Organization/')
org = rdflib.Namespace('http://www.w3.org/ns/org#')
hp = rdflib.Namespace('http://ontology.eil.utoronto.ca/HPCDM/')
service = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/CityService/')
res = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Resource/')
iso21972 = rdflib.Namespace('http://ontology.eil.utoronto.ca/ISO21972/iso21972#')
recurringevent = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/RecurringEvent/')


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


# Create RDF graph
g = Graph()
g2 = Graph()

# Initialize variables
filename = "supermarket.geojson"
amenityname = "Supermarket"

# List of supermarkets that have numerator data
numeratorlist = []

# Get the data
amenity = json.loads(open(filename, encoding='utf8').read())
df = pandas.read_csv("SupermarketNumerator.csv")
# Generate triples
g.add((cdt.Supermarket, org_city.hasIndustryType, cdt.GroceryAndConvenienceRetailersNAICS))

g.add((cdt.GroceryAndConvenienceRetailersNAICS, RDF.type, org_city.IndustryType))
g.add((cdt.GroceryAndConvenienceRetailersNAICS, code.hasCode, cdt.GroceryAndConvenienceRetailersNAICSCode))

g.add((cdt.GroceryAndConvenienceRetailersNAICSCode, RDF.type, cdt.NAICSCode))
g.add((cdt.GroceryAndConvenienceRetailersNAICSCode, genprop.hasName, Literal("4451 - Grocery and convenience retailers")))
g.add((cdt.GroceryAndConvenienceRetailersNAICSCode, genprop.hasDescription, Literal("This industry group comprises establishments primarily engaged in retailing a general line of food products.")))
g.add((cdt.GroceryAndConvenienceRetailersNAICSCode, genprop.hasIdentifier, Literal("4451")))

g.add((cdt.CDTCompleteCommunityAmenity, cdt.providesService, hp[amenityname + "Service"]))
g.add((hp[amenityname + "Service"], rdfs.subClassOf, cdt.Service))

# Generate triples for CompleteCommunityAmneity superclass and displayColor
g.add((cdt.Supermarket, rdfs.subClassOf, cdt.Organization))
g.add((cdt.Supermarket, cdt.displayColor, Literal("#f59042")))

# Generate triples for displayProperties
g.add((cdt.Supermarket, cdt.displayProperties, genprop.hasName))
g.add((cdt.Supermarket, cdt.displayProperties, cdt.website))
g.add((cdt.Supermarket, cdt.displayProperties, contact.hasTelephone))
g.add((cdt.Supermarket, cdt.displayProperties, genprop.hasIdentifier))
g.add((cdt.Supermarket, cdt.displayProperties, org.hasSite))
g.add((cdt.Supermarket, cdt.displayProperties, contact.hasAddress))
g.add((cdt.Supermarket, cdt.displayProperties, org_city.operatingHours))
g.add((cdt.Supermarket, cdt.displayProperties, cdt.email))

# Generate synthetic capacity triples
for row in df.itertuples(index=False):
    str_id = "".join(filter(str.isdigit, row.s))
    numeratorlist.append(str_id)
    
    g2.add((toronto[str_id + "SupermarketServiceCapacityUse"], iso21972.numerator, toronto[str_id + "CatchmentSupermarketCount"]))
    g2.add((toronto[str_id + "CatchmentSupermarketCount"], RDF.type, iso21972.Population))
    g2.add((toronto[str_id + "CatchmentSupermarketCount"], iso21972.hasValue, toronto[str_id + "CatchmentSupermarketCountMeasure"]))
    g2.add((toronto[str_id + "CatchmentSupermarketCountMeasure"], RDF.type, iso21972.Measure))
    g2.add((toronto[str_id + "CatchmentSupermarketCountMeasure"], iso21972.hasNumericalValue, Literal(row.nearbySchoolCount)))
    g2.add((toronto[str_id + "CatchmentSupermarketCountMeasure"], iso21972.hasUnit, iso21972.population_cardinality_unit))

    g2.add((toronto[str_id + "SupermarketServiceCapacityUse"], iso21972.hasValue, toronto[str_id + "SupermarketServiceCapacityUseMeasure"]))
    g2.add((toronto[str_id + "SupermarketServiceCapacityUseMeasure"], RDF.type, iso21972.Measure))
    g2.add((toronto[str_id + "SupermarketServiceCapacityUseMeasure"], iso21972.hasNumericalValue, Literal(row.nearbySchoolCount/22139)))
    g2.add((toronto[str_id + "SupermarketServiceCapacityUseMeasure"], iso21972.hasUnit, hp.sites_per_person))
    
    g2.add((toronto[str_id + "SupermarketService"], res.hasAvailableCapacity, toronto[str_id + "SupermarketServiceCapacityAvail"]))
    g2.add((toronto[str_id + "SupermarketServiceCapacityAvail"], RDF.type, hp.SupermarketsPopulationRatio))

    g2.add((toronto[str_id + "SupermarketServiceCapacityAvail"], iso21972.hasValue, toronto[str_id + "SupermarketServiceCapacityAvailMeasure"]))
    g2.add((toronto[str_id + "SupermarketServiceCapacityAvailMeasure"], RDF.type, iso21972.Measure))
    g2.add((toronto[str_id + "SupermarketServiceCapacityAvailMeasure"], iso21972.hasNumericalValue, Literal(0.001 - row.nearbySchoolCount/22139)))
    g2.add((toronto[str_id + "SupermarketServiceCapacityAvailMeasure"], iso21972.hasUnit, hp.sites_per_person))


# Generate triples for each instance
for element in amenity["features"]:
    osmid = re.sub("[^0-9]", "", element["id"])
    instancename = osmid + amenityname
    
    g.add((toronto[instancename], RDF.type, cdt.Supermarket))

    # Convert GeoJSON to Shapely geometry
    geom = make_valid(shape(element["geometry"]))
    
    # Put geometry into a GeoDataFrame with CRS = EPSG:4326 (WGS84 lat/lon)
    gdf = geopandas.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[geom])
    
    # Reproject to a meter-based CRS (UTM zone for Toronto is EPSG:32617)
    gdf = gdf.to_crs(epsg=32617)
    
    # Apply buffer of 5000 meters
    gdf = gdf.buffer(5000)
    
    # Convert back to WGS84
    gdf = gdf.to_crs(epsg=4326)
    
    # Generate triples for capacity data and catchment
    g2.add((toronto[instancename + "ServiceCatchmentLoc"], RDF.type, loc.Location))
    g2.add((toronto[instancename + "ServiceCatchmentLoc"], geo.asWKT, Literal(gdf.iloc[0].wkt, datatype=geo.wktLiteral)))
    g2.add((toronto[instancename + "Service"], service.hasCatchmentArea, toronto[instancename + "ServiceCatchmentLoc"]))
    
    g2.add((toronto[instancename + "Service"], res.capacityInUse, toronto[instancename + "ServiceCapacityUse"]))
    g2.add((toronto[instancename + "ServiceCapacityUse"], RDF.type, hp.SupermarketsPopulationRatio))

    g2.add((toronto[instancename + "ServiceCapacityUse"], iso21972.denominator, toronto[instancename + "ServiceCatchmentPopSize"]))
    g2.add((toronto[instancename + "ServiceCatchmentPopSize"], RDF.type, hp.ResidentPopulation))
    g2.add((toronto[instancename + "ServiceCatchmentPopSize"], iso21972.hasValue, toronto[instancename + "ServiceCatchmentPopSizeMeasure"]))
    g2.add((toronto[instancename + "ServiceCatchmentPopSizeMeasure"], RDF.type, iso21972.Measure))
    g2.add((toronto[instancename + "ServiceCatchmentPopSizeMeasure"], iso21972.hasNumericalValue, Literal(22139)))
    g2.add((toronto[instancename + "ServiceCatchmentPopSizeMeasure"], iso21972.hasUnit, iso21972.population_cardinality_unit))
        
    g2.add((toronto[instancename + "Service"], res.hasCapacity, toronto[instancename + "ServiceCapacity"]))
    g2.add((toronto[instancename + "ServiceCapacity"], RDF.type, hp.MinSupermarketsPopulationRatio))    
    g2.add((toronto[instancename + "ServiceCapacity"], iso21972.hasValue, toronto[instancename + "ServiceCapacityMeasure"]))
    g2.add((toronto[instancename + "ServiceCapacityMeasure"], RDF.type, iso21972.Measure))
    g2.add((toronto[instancename + "ServiceCapacityMeasure"], iso21972.hasNumericalValue, Literal(0.001)))
    g2.add((toronto[instancename + "ServiceCapacityMeasure"], iso21972.hasUnit, hp.sites_per_person))
    
    # If the current supermarket does not have a numerator, assume a numerator 
    # value of 1 and create triples for available capacity information
    if str(osmid) not in numeratorlist:
        str_id = str(osmid)
        
        g2.add((toronto[str_id + "SupermarketServiceCapacityUse"], iso21972.numerator, toronto[str_id + "CatchmentSupermarketCount"]))
        g2.add((toronto[str_id + "CatchmentSupermarketCount"], RDF.type, iso21972.Population))
        g2.add((toronto[str_id + "CatchmentSupermarketCount"], iso21972.hasValue, toronto[str_id + "CatchmentSupermarketCountMeasure"]))
        g2.add((toronto[str_id + "CatchmentSupermarketCountMeasure"], RDF.type, iso21972.Measure))
        g2.add((toronto[str_id + "CatchmentSupermarketCountMeasure"], iso21972.hasNumericalValue, Literal(1)))
        g2.add((toronto[str_id + "CatchmentSupermarketCountMeasure"], iso21972.hasUnit, iso21972.population_cardinality_unit))

        g2.add((toronto[str_id + "SupermarketServiceCapacityUse"], iso21972.hasValue, toronto[str_id + "SupermarketServiceCapacityUseMeasure"]))
        g2.add((toronto[str_id + "SupermarketServiceCapacityUseMeasure"], RDF.type, iso21972.Measure))
        g2.add((toronto[str_id + "SupermarketServiceCapacityUseMeasure"], iso21972.hasNumericalValue, Literal(1/22139)))
        g2.add((toronto[str_id + "SupermarketServiceCapacityUseMeasure"], iso21972.hasUnit, hp.sites_per_person))
        
        g2.add((toronto[str_id + "SupermarketService"], res.hasAvailableCapacity, toronto[str_id + "SupermarketServiceCapacityAvail"]))
        g2.add((toronto[str_id + "SupermarketServiceCapacityAvail"], RDF.type, hp.SupermarketsPopulationRatio))

        g2.add((toronto[str_id + "SupermarketServiceCapacityAvail"], iso21972.hasValue, toronto[str_id + "SupermarketServiceCapacityAvailMeasure"]))
        g2.add((toronto[str_id + "SupermarketServiceCapacityAvailMeasure"], RDF.type, iso21972.Measure))
        g2.add((toronto[str_id + "SupermarketServiceCapacityAvailMeasure"], iso21972.hasNumericalValue, Literal(0.001 - 1/22139)))
        g2.add((toronto[str_id + "SupermarketServiceCapacityAvailMeasure"], iso21972.hasUnit, hp.sites_per_person))


    
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

    # Generate triple for identifier
    g.add((toronto[instancename], genprop.hasIdentifier, Literal(osmid)))

    g.add((toronto[sitename], RDF.type, cdt[amenityname + "Site"]))
    g.add((toronto[instancename], org.hasSite, toronto[sitename]))
    g.add((toronto[sitename], loc.hasLocation, toronto[instancename + "Site" + "Location"]))


    # Generate triple for location instance
    g.add((toronto[instancename + "Site" + "Location"], RDF.type, loc.Location))
    g.add((toronto[instancename + "Site" + "Location"], geo.asWKT, Literal(shapely.to_wkt(make_valid(shapely.geometry.shape(element["geometry"])), rounding_precision=-1), datatype=geo.wktLiteral)))
    
    # Generate triples for service
    g.add((toronto[instancename + "Service"], RDF.type, toronto.TorSupermarketService))
    g.add((cdt.CDTCompleteCommunityAmenityToronto, cdt.providesService, toronto[instancename + "Service"]))
    g.add((toronto[instancename], cdt.providesService, toronto[instancename + "Service"]))
    g.add((toronto[instancename + "Service"], hp.providedFromSite, toronto[sitename]))

    
    # Generate triples for optional properties
    # Generate triples for name
    try:    
        g.add((toronto[instancename], genprop.hasName, Literal(element['properties']['name'])))
        g.add((toronto[sitename], genprop.hasName, Literal(element['properties']['name'])))
    except:
        pass
    
    # Generate triples for operating hours
    try: 
        hours_dict = parse_opening_hours(element['properties']['opening_hours'])
        for day in hours_dict:
            operationday = instancename + "OperatingHours" + day
            g.add((toronto[instancename], org_city.openingHours, toronto[operationday]))
            g.add((toronto[operationday], RDF.type, org_city.Operation))
            g.add((toronto[operationday], org_city.hasOpeningTime, Literal(hours_dict[day].split('-')[0], datatype=XSD.time)))
            g.add((toronto[operationday], org_city.hasClosingTime, Literal(hours_dict[day].split('-')[1], datatype=XSD.time)))
            g.add((toronto[operationday], recurringevent.hasDayOfWeek, recurringevent[day.lower()]))
    except:
        pass
    
    # Generate triples for website
    try: 
        g.add((toronto[instancename], cdt.website, Literal(element['properties']['website'])))
    except:
        pass
    
    # Generate triples for email
    try:    
        g.add((toronto[instancename], cdt.email, Literal(element['properties']['email'])))
    except:
        pass
    try:    
        g.add((toronto[instancename], cdt.email, Literal(element['properties']['contact:email'])))
    except:
        pass
    
    # Generate triples for operator and organization type
    try: 
        g.add((toronto[toUpperCamelCase(element['properties']['operator'])], org.hasSubOrganization, toronto[instancename]))
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
        g.add((toronto[instancename], contact.hasAddress, toronto[addressname]))
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
    
    # Generate triples for telephone number information
    try:
        phonenumber = phonenumbers.parse(element['properties']['phone'], None)
        g.add((toronto[instancename], contact.hasTelephone, toronto[telephonename]))
        g.add((toronto[telephonename], RDF.type, contact.PhoneNumber))
        g.add((toronto[telephonename], contact.hasCountryCode, Literal(phonenumber.country_code)))
        g.add((toronto[telephonename], contact.hasAreaCode, Literal(int(str(phonenumber.national_number)[:3]))))
        g.add((toronto[telephonename], contact.hasPhoneNumber, Literal(int(str(phonenumber.national_number)[3:]))))
        g.add((toronto[telephonename], contact.hasPhoneType, contact.workPhone))
    except:
        pass
    
    # Generate triples for fax number information
    try:
        faxnumber = phonenumbers.parse(element['properties']['fax'], None)
        g.add((toronto[instancename], contact.hasTelephone, toronto[faxname]))
        g.add((toronto[faxname], RDF.type, contact.PhoneNumber))
        g.add((toronto[faxname], contact.hasCountryCode, Literal(faxnumber.country_code)))
        g.add((toronto[faxname], contact.hasAreaCode, Literal(int(str(faxnumber.national_number)[:3]))))
        g.add((toronto[faxname], contact.hasPhoneNumber, Literal(int(str(faxnumber.national_number)[3:]))))
        g.add((toronto[faxname], contact.hasPhoneType, contact.faxPhone))
    except:
        pass


# Export the RDF graph as a .ttl file
g.serialize(destination= amenityname + ".ttl")
g2.serialize(destination= amenityname + "Capacity.ttl")





