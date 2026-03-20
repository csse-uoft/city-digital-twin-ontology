# -*- coding: utf-8 -*-
"""
Hospital.py

Author: Anderson Wong

Date: March 19, 2025

Description: This is a Python program that generates RDF triples 
for hospitals using OpenStreetMap data in a geojson file.
    
"""

# Import modules
import rdflib
import json
import re
import shapely
import usaddress
import phonenumbers

from shapely.validation import make_valid
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
sc = rdflib.Namespace('http://schema.org/')
gcih = rdflib.Namespace('http://ontology.eil.utoronto.ca/GCI/Health/GCI-Health.owl#')
contact = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Contact/')
org_city = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Organization/')
org = rdflib.Namespace('http://www.w3.org/ns/org#')
hp = rdflib.Namespace('http://ontology.eil.utoronto.ca/HPCDM/')
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

# Initialize variables
filename = "hospital.geojson"
amenityname = "Hospital"

# Get the data
amenity = json.loads(open(filename, encoding='utf8').read())

# Generate triples
g.add((cdt.Hospital, org_city.hasIndustryType, cdt.hospitalsNAICS))

g.add((cdt.hospitalsNAICS, RDF.type, org_city.IndustryType))
g.add((cdt.hospitalsNAICS, code.hasCode, cdt.hospitalsNAICSCode))

g.add((cdt.hospitalsNAICSCode, RDF.type, cdt.NAICSCode))
g.add((cdt.hospitalsNAICSCode, genprop.hasName, Literal("622 - Hospitals")))
g.add((cdt.hospitalsNAICSCode, genprop.hasDescription, Literal("This subsector comprises establishments, licensed as hospitals, primarily engaged in providing diagnostic and medical treatment services, and specialized accommodation services to in-patients. These establishments have an organized medical staff of physicians, nurses and other health professionals, technologists and technicians. Hospitals use specialized facilities and equipment that form a significant and integral part of the production process. Hospitals may also provide a wide variety of out-patient services as a secondary activity.")))
g.add((cdt.hospitalsNAICSCode, genprop.hasIdentifier, Literal("622")))

g.add((cdt.PublicHospital, rdfs.subClassOf, cdt.Hospital))
g.add((cdt.PublicHospital, rdfs.subClassOf, cdt.GovernmentOrganization))

g.add((cdt.PrivateHospital, rdfs.subClassOf, cdt.Hospital))
g.add((cdt.PrivateHospital, rdfs.subClassOf, cdt.ForProfitOrganization))

g.add((hp[amenityname + "Site"], rdfs.subClassOf, cdt.Site))

# Generate triples for CompleteCommunityAmneity superclass and displayColor
g.add((cdt.Hospital, rdfs.subClassOf, cdt.Organization))
g.add((cdt.Hospital, cdt.displayColor, Literal("#fc2323")))

# Generate triples for displayProperties
g.add((cdt.Hospital, cdt.displayProperties, genprop.hasName))
g.add((cdt.Hospital, cdt.displayProperties, cdt.website))
g.add((cdt.Hospital, cdt.displayProperties, contact.hasTelephone))
g.add((cdt.Hospital, cdt.displayProperties, genprop.hasIdentifier))
g.add((cdt.Hospital, cdt.displayProperties, org.hasSite))
g.add((cdt.Hospital, cdt.displayProperties, contact.hasAddress))
g.add((cdt.Hospital, cdt.displayProperties, org_city.operatingHours))

# Generate triples for each instance
for element in amenity["features"]:
    osmid = re.sub("[^0-9]", "", element["id"])
    instancename = osmid + amenityname
    addressname = instancename + "Address"
    areaname = instancename + "Area"
    areameasurename = areaname + "Measure"
    sitename = instancename + "Site"
    telephonename = instancename + "Telephone"
    faxname = instancename + "Faxphone"
    streetname = ""  
    
    # Generate triples for optional properties
    try:
        print(element['properties']['operator:type'])
    except:
        g.add((toronto[instancename], RDF.type, cdt.Hospital))
    else:
        if "public" in element['properties']['operator:type']:
            g.add((toronto[instancename], RDF.type, cdt.PublicHospital))
        elif "private" in element['properties']['operator:type']:
            g.add((toronto[instancename], RDF.type, cdt.PrivateHospital))
        else:
            g.add((toronto[instancename], RDF.type, cdt.Hospital))
            
    # Generate triple for identifier
    g.add((toronto[instancename], genprop.hasIdentifier, Literal(osmid)))

    g.add((toronto[sitename], RDF.type, hp[amenityname + "Site"]))
    g.add((toronto[instancename], org.hasSite, toronto[sitename]))
    g.add((toronto[sitename], loc.hasLocation, toronto[instancename + "Site" + "Location"]))


    # Generate triple for location instance
    g.add((toronto[instancename + "Site" + "Location"], RDF.type, loc.Location))
    g.add((toronto[instancename + "Site" + "Location"], geo.asWKT, Literal(shapely.to_wkt(make_valid(shapely.geometry.shape(element["geometry"])), rounding_precision=-1), datatype=geo.wktLiteral)))
    
    # Generate triples for service
    g.add((toronto[instancename + "Service"], RDF.type, toronto.TorHospitalService))
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
    
    # Generate triple for wheelchair access
    try:    
        g.add((toronto[instancename], cdt.wheelchairAccess, Literal(element['properties']['wheelchair'])))
    except:
        pass
    
    # Generate triples for hospital emergency services
    try:  
        if amenityname == "Hospital" and element['properties']['emergency'] == "yes":
            g.add((toronto[instancename + "EmergencyService"], RDF.type, toronto.TorHospitalEmergencyService))
            g.add((toronto[instancename + "EmergencyDepartment"], RDF.type, org.OrganizationalUnit))
            
            g.add((toronto[instancename], cdt.providesService, toronto[instancename + "EmergencyService"]))
            g.add((toronto[instancename], cdt.hasUnit, toronto[instancename + "EmergencyDepartment"]))
            
            g.add((toronto[instancename + "EmergencyService"], hp.providedFromSite, toronto[instancename + "Site"]))

    except:
        pass    

# Export the RDF graph as a .ttl file
g.serialize(destination= amenityname + ".ttl")





