# -*- coding: utf-8 -*-
"""
FederalBuildings.py

Author: Anderson Wong

Date: February 3, 2025

Description: This is a Python program that generates RDF triples 
for Federal buildings using data from a GeoJSON file.
"""

# Import modules
import rdflib
import json
import shapely
import geopandas
import usaddress
import xml.etree.ElementTree as ET

from shapely.validation import make_valid
from rdflib import Graph, Literal, RDF, URIRef, XSD

# Declare namespaces
toronto = rdflib.Namespace('http://ontology.eil.utoronto.ca/Toronto/Toronto#')
genprop = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/')
cdt = rdflib.Namespace('http://ontology.eil.utoronto.ca/CDT#')
loc = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/')
geo = rdflib.Namespace('http://www.opengis.net/ont/geosparql#')
code = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Code/')
rdfs = rdflib.Namespace('http://www.w3.org/2000/01/rdf-schema#')
contact = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Contact/')
org = rdflib.Namespace('http://www.w3.org/ns/org#')
hp = rdflib.Namespace('http://ontology.eil.utoronto.ca/HPCDM/')
iso21972 = rdflib.Namespace('http://ontology.eil.utoronto.ca/ISO21972/iso21972#')
cityunits = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/CityUnits/')
bdg = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Building/')
time = rdflib.Namespace('http://www.w3.org/2006/time#')
org_city = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Organization/')
service = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/CityService/')
cityunits = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/CityUnits/')

# Create RDF graph
g = Graph()

# Load the data
building1 = geopandas.read_file("FederalBuildings1.geojson")
building2 = geopandas.read_file("FederalBuildings2.geojson")

# Get XML data
tree = ET.parse("FederalBuildings.xml") 
root = tree.getroot()

# Generate triples for each row
for row in building1.itertuples():
    # Initialize variables
    parcelid = str(row.PARCELID)
    structureid = str(row.Structure_)
    
    # Find structure in XML file that has the same structure number
    for struct in root.findall(".//Structure"): 
        sn = struct.find("Structure_Number") 
        if sn.text == structureid: 
            structure = struct
            break
    if structure is None: 
        print("Error structure not found")
    
    # Create instance
    g.add((toronto[structureid + "Building"], RDF.type, hp.Building))
    g.add((toronto[structureid + "Building"], genprop.hasIdentifier, Literal(structureid)))
    g.add((toronto[structureid + "Building"], genprop.hasName, Literal(structureid)))
    
    # Create address triples
    addr = str(row.Structur_6)
    
    if addr not in ("Toronto", "Zoo Road"):
        street = usaddress.tag(addr)
        
        g.add((toronto[structureid + "Building"], contact.hasAddress, toronto[structureid + "Address"]))
        g.add((toronto[structureid + "Address"], RDF.type, contact.Address))
        
        streetname = ""
        try:
            streetname = " ".join([streetname, street[0]["StreetNamePreModifier"]])
        except: 
            pass
        try:
            streetname = " ".join([streetname, street[0]["StreetNamePreDirectional"]])
        except: 
            pass
        try:
            streetname += " ".join([streetname, street[0]["StreetName"]])
        except: 
            pass
        
        g.add((toronto[structureid + "Address"], contact.hasStreet, Literal(streetname)))
        
        try:
            g.add((toronto[structureid + "Address"], contact.hasStreetType, contact[street[0]["StreetNamePostType"].lower()]))
        except:
            pass
        try:
            g.add((toronto[structureid + "Address"], contact.hasStreetDirection, contact[street[0]["StreetNamePostDirectional"].lower()]))
        except:
            pass
        try:
            g.add((toronto[structureid + "Address"], contact.hasStreetNumber, Literal(street[0]["AddressNumber"])))
        except:
            pass
    
    # Generate triples for floor area
    try: 
        g.add((toronto[structureid + "BuildingFloorAreaMeasure"], iso21972.hasNumericalValue, Literal(row.Floor_Area)))
        g.add((toronto[structureid + "BuildingFloorAreaMeasure"], RDF.type, iso21972.Measure))
        g.add((toronto[structureid + "BuildingFloorArea"], RDF.type, cityunits.Area))
        g.add((toronto[structureid + "BuildingFloorArea"], iso21972.hasValue, toronto[structureid + "BuildingFloorAreaMeasure"]))
        g.add((toronto[structureid + "Building"], hp.hasFloorArea, toronto[structureid + "BuildingFloorArea"]))
        
        floor_area = structure.find("Floor_Area")
        if floor_area is None: 
            print("Floor_Area element not found in this structure") 
        else: 
            uom = floor_area.get("unitofMeasure") 
            if uom == "sqm":
                g.add((toronto[structureid + "BuildingFloorAreaMeasure"], iso21972.hasUnit, iso21972.square_metre))
            elif uom == "sqft":
                g.add((toronto[structureid + "BuildingFloorAreaMeasure"], iso21972.hasUnit, iso21972.square_feet))
            else:
                print("error")
    except:
        pass
    
    # Generate triples for year of construction
    try:
        g.add((toronto["Year" + str(row.Constructi)], bdg.yearOfConstruction, Literal(row.Constructi, datatype=XSD.gYear)))
        g.add((toronto[structureid + "Building"], bdg.yearOfConstruction, toronto["Year" + str(row.Constructi)]))
    except:
        pass

    # Generate triples for building condition
    try:
        g.add((toronto[structureid + "BuildingConditionCode"], genprop.hasName, Literal(row.Structur_9)))
        g.add((toronto[structureid + "BuildingConditionCode"], genprop.hasIdentifier, Literal(row.Structur_8)))
        g.add((toronto[structureid + "BuildingConditionCode"], RDF.type, code.Code))
        g.add((toronto[structureid + "Building"], hp.hasCondition, toronto[structureid + "BuildingCondition"]))
        g.add((toronto[structureid + "BuildingCondition"], code.hasCode, toronto[structureid + "BuildingConditionCode"]))
        g.add((toronto[structureid + "BuildingCondition"], RDF.type, hp.BuildingCondition))
    except:
       pass
   
    # Generate triples for location        
    g.add((toronto[structureid + "Building"], loc.hasLocation, toronto[structureid + "BuildingLoc"]))
    g.add((toronto[structureid + "BuildingLoc"], RDF.type, loc.Location))
    g.add((toronto[structureid + "BuildingLoc"], geo.asWKT, Literal(shapely.to_wkt(make_valid(shapely.geometry.shape(row.geometry)), rounding_precision=-1), datatype=geo.wktLiteral)))

    # Generate triples for building use
    use_types = structure.findall(".//UseType")
    for ut in use_types: 
        usecode = str(ut.get("code"))
        name_e = ut.find("Use_Name_E").text 

        g.add((toronto[structureid + "BuildingUse" + usecode + "Code"], genprop.hasName, Literal(name_e)))
        g.add((toronto[structureid + "BuildingUse" + usecode + "Code"], genprop.hasIdentifier, Literal(usecode)))
        g.add((toronto[structureid + "BuildingUse" + usecode + "Code"], RDF.type, code.Code))
        g.add((toronto[structureid + "Building"], bdg.use, toronto[structureid + "BuildingUse" + usecode]))
        g.add((toronto[structureid + "BuildingUse" + usecode], code.hasCode, toronto[structureid + "BuildingUse" + usecode + "Code"]))
        g.add((toronto[structureid + "BuildingUse" + usecode], RDF.type, bdg.BuildingUse))
    
    # Generate triples for the building tenant
    try: 
        g.add((toronto[structureid + "Building"], hp.occupiedBy, toronto[str(row.FGO_Identi) + "Tenant"]))
        g.add((toronto[str(row.FGO_Identi) + "Tenant"], RDF.type, org_city.Organization))
        g.add((toronto[str(row.FGO_Identi) + "Tenant"], genprop.hasName, Literal(row.FGO_Name_E)))
    except:
        pass
    
    # Generate triple linking the building to its parcel
    g.add((toronto[structureid + "Building"], hp.occupies, toronto["Property" + parcelid]))

# Generate triples for each row
for row in building2.itertuples():
    # Initialize variables
    parcelid = str(row.PARCELID)
    structureid = str(row.Structure_)
    
    # Find structure in XML file that has the same structure number
    for struct in root.findall(".//Structure"): 
        sn = struct.find("Structure_Number") 
        if sn.text == structureid: 
            structure = struct
            break
    if structure is None: 
        print("Error structure not found")
    
    # Create instance
    g.add((toronto[structureid + "Building"], RDF.type, hp.Building))
    g.add((toronto[structureid + "Building"], genprop.hasIdentifier, Literal(structureid)))
    g.add((toronto[structureid + "Building"], genprop.hasName, Literal(structureid)))
    
    # Create address triples
    addr = str(row.Structur_6)
    
    if addr not in ("Toronto", "Zoo Road"):
        street = usaddress.tag(addr)
        
        g.add((toronto[structureid + "Building"], contact.hasAddress, toronto[structureid + "Address"]))
        g.add((toronto[structureid + "Address"], RDF.type, contact.Address))
        
        streetname = ""
        try:
            streetname = " ".join([streetname, street[0]["StreetNamePreModifier"]])
        except: 
            pass
        try:
            streetname = " ".join([streetname, street[0]["StreetNamePreDirectional"]])
        except: 
            pass
        try:
            streetname += " ".join([streetname, street[0]["StreetName"]])
        except: 
            pass
        
        g.add((toronto[structureid + "Address"], contact.hasStreet, Literal(streetname)))
        
        try:
            g.add((toronto[structureid + "Address"], contact.hasStreetType, contact[street[0]["StreetNamePostType"].lower()]))
        except:
            pass
        try:
            g.add((toronto[structureid + "Address"], contact.hasStreetDirection, contact[street[0]["StreetNamePostDirectional"].lower()]))
        except:
            pass
        try:
            g.add((toronto[structureid + "Address"], contact.hasStreetNumber, Literal(street[0]["AddressNumber"])))
        except:
            pass
    
    # Generate triples for floor area
    try: 
        g.add((toronto[structureid + "BuildingFloorAreaMeasure"], iso21972.hasNumericalValue, Literal(row.Floor_Area)))
        g.add((toronto[structureid + "BuildingFloorAreaMeasure"], RDF.type, iso21972.Measure))
        g.add((toronto[structureid + "BuildingFloorArea"], RDF.type, cityunits.Area))
        g.add((toronto[structureid + "BuildingFloorArea"], iso21972.hasValue, toronto[structureid + "BuildingFloorAreaMeasure"]))
        g.add((toronto[structureid + "Building"], hp.hasFloorArea, toronto[structureid + "BuildingFloorArea"]))
        
        floor_area = structure.find("Floor_Area")
        if floor_area is None: 
            print("Floor_Area element not found in this structure") 
        else: 
            uom = floor_area.get("unitofMeasure") 
            if uom == "sqm":
                g.add((toronto[structureid + "BuildingFloorAreaMeasure"], iso21972.hasUnit, iso21972.square_metre))
            elif uom == "sqft":
                g.add((toronto[structureid + "BuildingFloorAreaMeasure"], iso21972.hasUnit, iso21972.square_feet))
            else:
                print("error")
    except:
        pass
    
    # Generate triples for year of construction
    try:
        if str(row.Constructi) not in  (" ", ""):
            g.add((toronto["Year" + str(row.Constructi)], bdg.yearOfConstruction, Literal(row.Constructi, datatype=XSD.gYear)))
            g.add((toronto[structureid + "Building"], bdg.yearOfConstruction, toronto["Year" + str(row.Constructi)]))
    except:
        pass

    # Generate triples for building condition
    try:
        g.add((toronto[structureid + "BuildingConditionCode"], genprop.hasName, Literal(row.Structur_9)))
        g.add((toronto[structureid + "BuildingConditionCode"], genprop.hasIdentifier, Literal(row.Structur_8)))
        g.add((toronto[structureid + "BuildingConditionCode"], RDF.type, code.Code))
        g.add((toronto[structureid + "Building"], hp.hasCondition, toronto[structureid + "BuildingCondition"]))
        g.add((toronto[structureid + "BuildingCondition"], code.hasCode, toronto[structureid + "BuildingConditionCode"]))
        g.add((toronto[structureid + "BuildingCondition"], RDF.type, hp.BuildingCondition))
    except:
       pass
   
    # Generate triples for location        
    g.add((toronto[structureid + "Building"], loc.hasLocation, toronto[structureid + "BuildingLoc"]))
    g.add((toronto[structureid + "BuildingLoc"], RDF.type, loc.Location))
    g.add((toronto[structureid + "BuildingLoc"], geo.asWKT, Literal(shapely.to_wkt(make_valid(shapely.geometry.shape(row.geometry)), rounding_precision=-1), datatype=geo.wktLiteral)))

    # Generate triples for building use
    use_types = structure.findall(".//UseType")
    for ut in use_types: 
        usecode = str(ut.get("code"))
        name_e = ut.find("Use_Name_E").text 

        g.add((toronto[structureid + "BuildingUse" + usecode + "Code"], genprop.hasName, Literal(name_e)))
        g.add((toronto[structureid + "BuildingUse" + usecode + "Code"], genprop.hasIdentifier, Literal(usecode)))
        g.add((toronto[structureid + "BuildingUse" + usecode + "Code"], RDF.type, code.Code))
        g.add((toronto[structureid + "Building"], bdg.use, toronto[structureid + "BuildingUse" + usecode]))
        g.add((toronto[structureid + "BuildingUse" + usecode], code.hasCode, toronto[structureid + "BuildingUse" + usecode + "Code"]))
        g.add((toronto[structureid + "BuildingUse" + usecode], RDF.type, bdg.BuildingUse))
    
    # Generate triples for the building tenant
    try: 
        g.add((toronto[structureid + "Building"], hp.occupiedBy, toronto[str(row.FGO_Identi) + "Tenant"]))
        g.add((toronto[str(row.FGO_Identi) + "Tenant"], RDF.type, org_city.Organization))
        g.add((toronto[str(row.FGO_Identi) + "Tenant"], genprop.hasName, Literal(row.FGO_Name_E)))
    except:
        pass
    
    # Generate triple linking the building to its parcel
    g.add((toronto[structureid + "Building"], hp.occupies, toronto["Property" + parcelid]))


# Export the rdf graph as a TTL file
g.serialize(destination="FederalBuildings.ttl", format="ttl")


    