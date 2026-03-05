# -*- coding: utf-8 -*-
"""
SolidWaste.py

Author: Anderson Wong

Date: February 13, 2026

Description: This is a Python program that generates RDF triples 
for solid waste collection using data from a GeoJSON file.
"""

# Import modules
import rdflib
import json
import shapely

from shapely.validation import make_valid
from rdflib import Graph, Literal, RDF, URIRef

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
# Create RDF graph
g = Graph()

# Initialize variables
filename = "SolidWaste.geojson"

# Get the data
data = json.loads(open(filename, encoding='utf8').read())

counter = 0

# Generate triples for each instance
for element in data["features"]:
    # Initialize variables
    objectid = str(counter)
    
    g.add((toronto["solidwaste_service" + objectid], RDF.type, toronto.TorSolidWasteService))
    g.add((toronto["solidwaste_service" + objectid], service.hasCatchmentArea, toronto["solidwaste_servicearea_" + str(element['properties']['AREA_ID'])]))
    
    g.add((toronto["solidwaste_servicearea_" + str(element['properties']['AREA_ID'])], RDF.type, loc.Location))
    g.add((toronto["solidwaste_servicearea_" + str(element['properties']['AREA_ID'])], genprop.hasIdentifier, Literal(element['properties']['AREA_ID'])))
    g.add((toronto["solidwaste_servicearea_" + str(element['properties']['AREA_ID'])], genprop.hasIdentifier, Literal(element['properties']['AREA_LONG_'])))
    g.add((toronto["solidwaste_servicearea_" + str(element['properties']['AREA_ID'])], genprop.hasName, Literal(element['properties']['AREA_NAME'])))
    g.add((toronto["solidwaste_servicearea_" + str(element['properties']['AREA_ID'])], geo.asWKT, Literal(shapely.to_wkt(make_valid(shapely.geometry.shape(element["geometry"])), rounding_precision=-1), datatype=geo.wktLiteral)))

    counter += 1
# Export the RDF graph as a .ttl file
g.serialize(destination="SolidWaste.ttl")
