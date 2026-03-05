# -*- coding: utf-8 -*-
"""
PublicSchools.py

Author: Anderson Wong

Date: January 26, 2026

Description: This is a Python program that generates RDF triples 
for public schools using Microsoft Excel data from the Government of Ontario.
"""

import pandas
import rdflib
import usaddress
import phonenumbers
import math

from shapely.geometry import Point
from geopy.geocoders import ArcGIS
from rdflib import Graph, Literal, XSD, RDF, URIRef

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

geolocator = ArcGIS()

# Create RDF graph
g = Graph()

# Get the data
df = pandas.read_excel("OntarioPublicSchools.xlsx")

# Generate triples for superclass and displayColor
g.add((cdt.School, rdfs.subClassOf, cdt.Organization))
g.add((cdt.School, cdt.displayColor, Literal("#4287f5")))

# Generate triples for displayProperties
g.add((cdt.School, cdt.displayProperties, genprop.hasName))
g.add((cdt.School, cdt.displayProperties, cdt.website))
g.add((cdt.School, cdt.displayProperties, contact.hasTelephone))
g.add((cdt.School, cdt.displayProperties, genprop.hasIdentifier))
g.add((cdt.School, cdt.displayProperties, org.hasSite))
g.add((cdt.School, cdt.displayProperties, contact.hasAddress))
g.add((cdt.School, cdt.displayProperties, cdt.languageOfInstruction))

g.add((cdt.Site, cdt.displayProperties, cdt.wheelchairAccess))

g.add((contact.PhoneNumber, cdt.displayProperties, contact.hasCountryCode))
g.add((contact.PhoneNumber, cdt.displayProperties, contact.hasAreaCode))
g.add((contact.PhoneNumber, cdt.displayProperties, contact.hasPhoneNumber))
g.add((contact.PhoneNumber, cdt.displayProperties, contact.hasPhoneType))

# Generate triples for elementary school and secondary school
g.add((cdt.ElementarySchool, rdfs.subClassOf, cdt.School))
g.add((cdt.SecondarySchool, rdfs.subClassOf, cdt.School))
g.add((cdt.ElementarySchool, org_city.hasIndustryType, cdt.elementaryAndSecondarySchoolsNAICS))
g.add((cdt.SecondarySchool, org_city.hasIndustryType, cdt.elementaryAndSecondarySchoolsNAICS))

g.add((cdt.NAICSCode, rdfs.subClassOf, code.Code))

g.add((cdt.elementaryAndSecondarySchoolsNAICSCode, RDF.type, cdt.NAICSCode))
g.add((cdt.elementaryAndSecondarySchoolsNAICSCode, genprop.hasName, Literal("6111 - Elementary and secondary schools")))
g.add((cdt.elementaryAndSecondarySchoolsNAICSCode, genprop.hasDescription, Literal("This industry group comprises establishments primarily engaged in providing academic courses that comprise a basic preparatory education, that is, Kindergarten to Grade 12.")))
g.add((cdt.elementaryAndSecondarySchoolsNAICSCode, genprop.hasIdentifier, Literal("6111")))

# Generate triples for the school boards
g.add((toronto.B67059SchoolBoard, RDF.type, cdt.Organization))
g.add((toronto.B67059SchoolBoard, genprop.hasIdentifier, Literal("B67059")))
g.add((toronto.B67059SchoolBoard, genprop.hasName, Literal("Toronto CDSB")))
g.add((toronto.B67059SchoolBoard, cdt.website, Literal("http://www.tcdsb.org")))


g.add((toronto.B66052SchoolBoard, RDF.type, cdt.Organization))
g.add((toronto.B66052SchoolBoard, genprop.hasIdentifier, Literal("B66052")))
g.add((toronto.B66052SchoolBoard, genprop.hasName, Literal("Toronto DSB")))
g.add((toronto.B66052SchoolBoard, cdt.website, Literal("http://www.tdsb.on.ca")))


g.add((cdt.SchoolSite, rdfs.subClassOf, cdt.Site))

# Iterate through each row of the Excel table
for idx, row in df.iterrows():
    # Only create data for TDSB and TCDSB schools
    if str(row["Board Number"]) in ("B67059", "B66052"):
        # Instantiate the name for the instance of school
        instancename = str(row["School Number"]) + "School"
        
        # Generate triples for school level
        if row["School Level"] == "Elementary":
            g.add((toronto[instancename], RDF.type, cdt.ElementarySchool))
        elif row["School Level"] == "Secondary":
            g.add((toronto[instancename], RDF.type, cdt.SecondarySchool))
        elif row["School Level"] == "Elem/Sec":
            g.add((toronto[instancename], RDF.type, cdt.ElementarySchool))   
            g.add((toronto[instancename], RDF.type, cdt.SecondarySchool))
    
        g.add((toronto[instancename], cdt.providesService, toronto[instancename + "Service"]))
        g.add((toronto[instancename + "Service"], RDF.type, toronto.TorSchoolService))
        g.add((toronto[instancename + "Service"], hp.providedFromSite, toronto[instancename + "Site"]))

        # Generate triples for name and identifier
        g.add((toronto[instancename], genprop.hasIdentifier, Literal(row["School Number"])))
        g.add((toronto[instancename], genprop.hasName, Literal(row["School Name"])))
        
        # Links the school instance to its corresponding school board
        if str(row["Board Number"]) == "B67059":
            g.add((toronto.B67059SchoolBoard, org.hasSubOrganization, toronto[instancename]))
        else:
            g.add((toronto.B66052SchoolBoard, org.hasSubOrganization, toronto[instancename]))
        
        # Use geocoder to get geospatial point coordinates from the address            
        address = str(row["Street"]) + ", " + str(row["City"]) + ", " + str(row["Province"]) + ", " + str(row["Postal Code"])
        location = geolocator.geocode(address)
        print(address)
        point = Point(location.longitude, location.latitude)
        print(point)
        
        # Generate triples for site and site location
        g.add((toronto[instancename + "Site"], RDF.type, cdt.SchoolSite))
        g.add((toronto[instancename + "Site"], genprop.hasName, Literal(row["School Name"])))
        g.add((toronto[instancename], org.hasSite, toronto[instancename + "Site"]))
        g.add((toronto[instancename + "Site"], loc.hasLocation, toronto[instancename + "SiteLocation"]))
        
        g.add((toronto[instancename + "Site" + "Location"], RDF.type, loc.Location))
        g.add((toronto[instancename + "SiteLocation"], geo.asWKT, Literal(point.wkt, datatype=geo.wktLiteral)))
        
        # Generate triples for address information
        g.add((toronto[instancename + "Site"], org.siteAddress, toronto[instancename + "Address"]))

        g.add((toronto[instancename + "Address"], RDF.type, contact.Address))
        
        street = usaddress.tag(str(row["Street"]))
        print(street)
        streetname = ""
        try:
            streetname += street[0]["StreetNamePreModifier"]
        except: 
            pass
        try:
            streetname += street[0]["StreetNamePreDirectional"]
        except: 
            pass
        try:
            streetname += street[0]["StreetName"]
        except: 
            pass
        
        g.add((toronto[instancename + "Address"], contact.hasStreet, Literal(streetname)))
        
        try:
            g.add((toronto[instancename + "Address"], contact.hasStreetType, contact[street[0]["StreetNamePostType"].lower()]))
        except:
            pass
        try:
            g.add((toronto[instancename + "Address"], contact.hasStreetDirection, contact[street[0]["StreetNamePostDirectional"].lower()]))
        except:
            pass
        try:
            g.add((toronto[instancename + "Address"], contact.hasStreetNumber, Literal(street[0]["AddressNumber"])))
        except:
            pass
        
        try:
            words = row["City"].split()
            cityname = words[0].lower() + ''.join(word.capitalize() for word in words[1:])
            
            g.add((toronto[instancename + "Address"], contact.hasCity, toronto[cityname]))
        except:
            pass
        
        g.add((toronto[instancename + "Address"], contact.hasProvince, cdt.ontario))
        g.add((toronto[instancename + "Address"], contact.hasCountry, cdt.canada))
        
        # Generate triples for telephone number information
        try:
            phonenumber = phonenumbers.parse(row["Phone"], None)
            g.add((toronto[instancename], contact.hasTelephone, toronto[instancename + "Telephone"]))
            g.add((toronto[instancename + "Telephone"], RDF.type, contact.PhoneNumber))
            g.add((toronto[instancename + "Telephone"], contact.hasCountryCode, Literal(phonenumber.country_code)))
            g.add((toronto[instancename + "Telephone"], contact.hasAreaCode, Literal(int(str(phonenumber.national_number)[:3]))))
            g.add((toronto[instancename + "Telephone"], contact.hasPhoneNumber, Literal(int(str(phonenumber.national_number)[3:]))))
            g.add((toronto[instancename + "Telephone"], contact.hasPhoneType, contact.workPhone))
        except:
            pass
        
        # Generate triples for fax number information
        try:
            faxnumber = phonenumbers.parse(row["Fax"], None)
            g.add((toronto[instancename], contact.hasTelephone, toronto[instancename + "Faxphone"]))
            g.add((toronto[instancename + "Faxphone"], RDF.type, contact.PhoneNumber))
            g.add((toronto[instancename + "Faxphone"], contact.hasCountryCode, Literal(faxnumber.country_code)))
            g.add((toronto[instancename + "Faxphone"], contact.hasAreaCode, Literal(int(str(faxnumber.national_number)[:3]))))
            g.add((toronto[instancename + "Faxphone"], contact.hasPhoneNumber, Literal(int(str(faxnumber.national_number)[3:]))))
            g.add((toronto[instancename + "Faxphone"], contact.hasPhoneType, contact.faxPhone))
        except:
            pass
        
        # Generate triples for website
        try:
            print(math.isnan(row["Website"]))
                
        except:
            g.add((toronto[instancename], cdt.website, Literal(row["Website"])))
        
        # Generate triples for email
        try:  
            print(math.isnan(row["Email"]))
        except:
            g.add((toronto[instancename], cdt.email, Literal(row["Email"])))
        
# Export the RDF graph as a .ttl file    
g.serialize(destination="PublicSchools.ttl")
        
    
   
