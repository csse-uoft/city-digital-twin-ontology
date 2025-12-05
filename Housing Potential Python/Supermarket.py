# -*- coding: utf-8 -*-
"""
Supermarket.py

Author: Anderson Wong

Date: December 1, 2025

Description: This is a Python program that generates RDF triples 
for supermarkets using OpenStreetMap data in a geojson file.
    
"""

# Import modules
import rdflib
import json
import rdftools
import re
import geopandas

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

# Create RDF graph
g = Graph()
g2 = Graph()

# Initialize variables
filename = "supermarket.geojson"
amenityname = "Supermarket"

# Get the data
amenity = json.loads(open(filename, encoding='utf8').read())

# Generate triples
g.add((cdt.Supermarket, org_city.hasIndustryType, cdt.GroceryAndConvenienceRetailersNAICS))

g.add((cdt.GroceryAndConvenienceRetailersNAICS, RDF.type, org_city.IndustryType))
g.add((cdt.GroceryAndConvenienceRetailersNAICS, code.hasCode, cdt.GroceryAndConvenienceRetailersNAICSCode))

g.add((cdt.GroceryAndConvenienceRetailersNAICSCode, RDF.type, cdt.NAICSCode))
g.add((cdt.GroceryAndConvenienceRetailersNAICSCode, genprop.hasName, Literal("4451 - Grocery and convenience retailers")))
g.add((cdt.GroceryAndConvenienceRetailersNAICSCode, genprop.hasDescription, Literal("This industry group comprises establishments primarily engaged in retailing a general line of food products.")))
g.add((cdt.GroceryAndConvenienceRetailersNAICSCode, genprop.hasIdentifier, Literal("4451")))

g.add((cdt.CDTCompleteCommunityAmenity, cdt.providesService, cdt[amenityname + "Service"]))
g.add((cdt[amenityname + "Service"], rdfs.subClassOf, cdt.Service))

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

# Generate triples for each instance
for element in amenity["features"]:
    osmid = re.sub("[^0-9]", "", element["id"])
    instancename = osmid + amenityname
    
    g.add((toronto[instancename], RDF.type, cdt.Supermarket))

    # Convert GeoJSON to Shapely geometry
    geom = shape(element["geometry"])
    
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

    g2.add((toronto[instancename + "ServiceCapacityUse"], iso21972.denominator, toronto[instancename + "ServiceCatchmentPopSize"]))
    g2.add((toronto[instancename + "ServiceCatchmentPopSize"], iso21972.hasNumericalValue, Literal(22139)))
    g2.add((toronto[instancename + "ServiceCatchmentPopSize"], iso21972.hasUnit, iso21972.population_cardinality_unit))
    
    g2.add((toronto[instancename + "Service"], res.hasCapacity, toronto[instancename + "ServiceCapacity"]))

    g2.add((toronto[instancename + "ServiceCapacity"], iso21972.hasValue, toronto[instancename + "ServiceCapacityMeasure"]))
    g2.add((toronto[instancename + "ServiceCapacityMeasure"], RDF.type, iso21972.Measure))
    g2.add((toronto[instancename + "ServiceCapacityMeasure"], iso21972.hasNumericalValue, Literal(0.001)))
    g2.add((toronto[instancename + "ServiceCapacityMeasure"], iso21972.hasUnit, hp.sites_per_person))

    # Call generate_triples function
    g += rdftools.generate_triples(element, amenityname)
    
    
# Export the RDF graph as a .ttl file
g.serialize(destination= amenityname + ".ttl")
g2.serialize(destination= amenityname + "Capacity.ttl")





