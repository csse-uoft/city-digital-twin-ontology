# -*- coding: utf-8 -*-
"""
TransitStop.py

Author: Anderson Wong

Date: February 17, 2025

Description: This is a Python program that generates RDF triples 
for transit stops from GTFS data.
    
"""

# Import modules
import rdflib
import csv
import os

from rdflib import Graph, Literal, RDF

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
org = rdflib.Namespace('http://www.w3.org/ns/org#')

with open(os.path.join(os.getcwd(), "TTC", "stops.txt"), newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    data = list(reader)

# Create RDF graph
g = Graph()

# Initialize variables
amenityname = "TransitStop"

g.add((cdt.TransitStop, rdfs.label, Literal("TransitStop")))
g.add((cdt.TransitStop, rdfs.comment, Literal("The individual locations where vehicles pick up or drop off passengers.")))
g.add((cdt.TransitStop, rdfs.subClassOf, cdt.Site))

g.add((toronto.ttc, genprop.hasName, Literal("Toronto Transit Commission")))   


# Generate triples for CompleteCommunityAmneity superclass and displayColor
g.add((cdt.TransitStop, cdt.displayColor, Literal("#f70202")))

# Generate triples for displayProperties
g.add((cdt.TransitStop, cdt.displayProperties, genprop.hasName))
g.add((cdt.TransitStop, cdt.displayProperties, genprop.hasIdentifier))
g.add((cdt.TransitStop, cdt.displayProperties, cdt.wheelchairAccess))

for row in data:
    # Initialize variables
    instancename = row[0] + "TransitStop"
    
    # Generate triples for transit stop instance
    g.add((toronto[instancename], RDF.type, cdt.TransitStop))
    g.add((toronto[instancename], loc.hasLocation, toronto[instancename + "Location"]))
    g.add((toronto[instancename], gci.forCity, toronto.toronto))   
    g.add((toronto[instancename], genprop.hasIdentifier, Literal(row[0])))
    g.add((toronto[instancename], genprop.hasName, Literal(row[2])))
    
    g.add((toronto.ttc, org.hasSite, toronto[instancename]))   
    try:
        wheelchairaccess = str(row[11])
        if wheelchairaccess == "1":
            g.add((toronto[instancename], cdt.wheelchairAccess, Literal("Yes")))
        elif wheelchairaccess == "2":
            g.add((toronto[instancename], cdt.wheelchairAccess, Literal("No")))
    except:
        pass
    
    # Generate triple for location instance
    g.add((toronto[instancename + "Location"], RDF.type, loc.Location))
    
    # Generate triple for asWKT property
    longitude = row[5]
    latitude = row[4]
    g.add((toronto[instancename + "Location"], geo.asWKT, Literal(f"POINT ({longitude} {latitude})", datatype=geo.wktLiteral)))

# Export the RDF graph as a .ttl file
g.serialize(destination="TransitStop.ttl")