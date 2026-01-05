# -*- coding: utf-8 -*-
"""
Buildings.py

Author: Anderson Wong

Date: January 5, 2025

Description: This is a Python program that generates RDF triples 
for buildings and land parcels using data from a GeoJSON file.
"""

# Import modules
import rdflib
import re
import shapely
import usaddress
import gc
import geopandas

from rdflib import Graph, Literal, RDF

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

# Create RDF graph
g = Graph()

# Get the data and remove unused columns
building = geopandas.read_file("TorontoBuildings2.geojson")
building = building.drop(columns=["Join_Count", "TARGET_FID", "JOIN_FID", "source_id", "source", "dataset", "csduid", "csdname", "prov_terr", "units", "F_id", "FEATURE_TYPE", "DATE_EFFECTIVE", "DATE_EXPIRY", "TRANS_ID_CREATE", "TRANS_ID_EXPIRE", "Shape_Length_1", "Shape_Area_1"])

parcel = geopandas.read_file("Parcel.geojson")
parcel = parcel.drop(columns= ["F_TYPE"])
parcel = parcel.rename(columns={"OBJECTID": "PARCELID"})

# Merge datasets using PARCELID
df = building.merge(parcel, on="PARCELID")

# Counter for number of data entries
counter = 0

# Counter for output file number (i.e., Buildings{counter2}.ttl)
# Should start with 1 if working on the first file or 6 if working on the second to avoid overwriting the files
counter2 = 6

# Generate triples for each row
for idx, row in df.iterrows():
    # Initialize variables
    parcelid = str(row['PARCELID'])
    buildingid = str(row['id'])
    
    # Generate triples for area data
    try:
        g.add((toronto["PropertyAreaMeasure" + parcelid], iso21972.hasNumericalValue, Literal(float(re.findall(r'\d+(?:\.\d+)?', row['STATEDAREA'])[0]))))

        g.add((toronto["Property" + parcelid], RDF.type, hp.Parcel))
        g.add((toronto["PropertyArea" + parcelid], RDF.type, cityunits.Area))
        g.add((toronto["PropertyAreaMeasure" + parcelid], RDF.type, iso21972.Measure))
    
        g.add((toronto["Property" + parcelid], hp.hasArea, toronto["PropertyArea" + parcelid]))
        g.add((toronto["PropertyArea" + parcelid], iso21972.hasValue, toronto["PropertyAreaMeasure" + parcelid]))
        g.add((toronto["PropertyAreaMeasure" + parcelid], iso21972.hasUnit, iso21972.square_metre))
    except:
        pass
    
    # Generate triples for geometry data
    g.add((toronto["PropertyLoc" + parcelid], RDF.type, loc.Location))

    g.add((toronto["Property" + parcelid], loc.hasLocation, toronto["PropertyLoc" + parcelid]))
    g.add((toronto["PropertyLoc" + parcelid], geo.asWKT, Literal(shapely.to_wkt(shapely.geometry.shape(row["geometry_y"])), datatype=geo.wktLiteral)))

    # Generate triples for building data
    g.add((toronto["Building" + buildingid], RDF.type, hp.Building))
    
    # Generate triples for building name

    if row['name'] != "..":
        g.add((toronto["Building" + buildingid], genprop.hasName, Literal(row['name'])))
    
    # Generate triples for address data    
    try:
        if row['address'] != "..":
            streetstring = row['address']
        elif row['ADDRESS_NUMBER'] != "None":
            streetstring = " ".join([str(row['ADDRESS_NUMBER']), row['LINEAR_NAME_FULL']])

        # Split by semicolon
        addr_list = streetstring.split(";")
        
        # Strip extra spaces
        addr_list = [addr.strip() for addr in addr_list]
        
        addrcounter = 1
        
        # Create address triples for each address in addr_list
        for addr in addr_list:
            street = usaddress.tag(addr)
            addrcounterstr = "_" + str(addrcounter)
            
            g.add((toronto["Building" + buildingid], contact.hasAddress, toronto["BuildingAddress" + addrcounterstr + buildingid]))
            g.add((toronto["BuildingAddress" + addrcounterstr  + buildingid], RDF.type, contact.Address))
            
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
            
            g.add((toronto["BuildingAddress" + addrcounterstr + buildingid], contact.hasStreet, Literal(streetname)))
            
            try:
                g.add((toronto["BuildingAddress" + addrcounterstr + buildingid], contact.hasStreetType, contact[street[0]["StreetNamePostType"].lower()]))
            except:
                pass
            try:
                g.add((toronto["BuildingAddress" + addrcounterstr + buildingid], contact.hasStreetDirection, contact[street[0]["StreetNamePostDirectional"].lower()]))
            except:
                pass
            try:
                g.add((toronto["BuildingAddress" + addrcounterstr + buildingid], contact.hasStreetNumber, Literal(street[0]["AddressNumber"])))
            except:
                pass
            
            addrcounter += 1
    except:
        pass
    
    # Generate triples for building type
    if row['type'] != "..":
        buildingtype = str(row['type'].replace(" ", ""))
        
        g.add((toronto["BuildingUse" + buildingtype], RDF.type, bdg.BuildingUse))
        g.add((toronto["BuildingUseCode" + buildingtype], RDF.type, code.Code))

        g.add((toronto["Building" + buildingid], bdg.use, toronto["BuildingUse" + buildingtype]))
        
        g.add((toronto["BuildingUse" + buildingtype], code.hasCode, toronto["BuildingUseCode" + buildingtype]))
        g.add((toronto["BuildingUseCode" + buildingtype], genprop.hasName, Literal(buildingtype)))
        
    if row['height'] != "..":
        g.add((toronto["BuildingHeight" + buildingid], RDF.type, hp.BuildingHeight))
        
        g.add((toronto["Building" + buildingid], hp.hasHeight, toronto["BuildingHeight" + buildingid]))
    
        g.add((toronto["BuildingHeight" + buildingid], iso21972.hasValue, toronto["BuildingHeightMeasure" + buildingid]))
        
        g.add((toronto["BuildingHeightMeasure" + buildingid], RDF.type, iso21972.Measure))
        g.add((toronto["BuildingHeightMeasure" + buildingid], iso21972.hasNumericalValue, Literal(row['height'])))
        g.add((toronto["BuildingHeightMeasure" + buildingid], iso21972.hasUnit, iso21972.metre))
    
    # Generate triples for year built
    if row['year_built'] != "..":
        year = str(row['year_built'])
        
        g.add((toronto["Year" + year], RDF.type, time.DateTimeDescription))
        
        g.add((toronto["Building" + buildingid], bdg.yearOfConstruction, toronto["Year" + year]))

        g.add((toronto["Year" + year], time.year, Literal(row['year_built'])))
    
    # Generate triples for geometry data
    g.add((toronto["BuildingLoc" + buildingid], RDF.type, loc.Location))

    g.add((toronto["Building" + buildingid], loc.hasLocation, toronto["BuildingLoc" + buildingid]))
    g.add((toronto["BuildingLoc" + buildingid], geo.asWKT, Literal(shapely.to_wkt(shapely.geometry.shape(row["geometry_x"])), datatype=geo.wktLiteral)))

    
    # Generate triple for linking the building with the parcel
    g.add((toronto["Building" + buildingid], hp.occupies, toronto["Property" + parcelid]))
    
    counter += 1
    print(counter)
    if counter == 100000:
        g.serialize(destination="Buildings" + str(counter2) + ".nt", format="nt")
        counter2 += 1
        counter = 0
        g = Graph()
        gc.collect()
        
    
# Export the RDF graph as a .nt file    
g.serialize(destination="Buildings" + str(counter2) + ".nt", format="nt")
    
    
    