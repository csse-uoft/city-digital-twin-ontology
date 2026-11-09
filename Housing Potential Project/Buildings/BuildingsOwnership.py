# -*- coding: utf-8 -*-
"""
BuildingsOwnership.py

Author: Anderson Wong

Date: November 18, 2025

Description: This is a Python program that generates RDF triples 
for land ownership using data from a GeoJSON file.

Note: element['properties']['Tier'] should be replaced with 
element['properties']['myp_tier'] for the GTHA Lower Tier dataset
"""

# Import modules
import rdflib
import json
import shapely

from shapely.validation import make_valid
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
org_city = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Organization/')


def camelcase(s: str) -> str:
    # Replace separators with spaces
    s = s.replace("_", " ").replace("-", " ")
    # Capitalize each word
    parts = s.title().split()
    # Lowercase the first word, join the rest
    return parts[0].lower() + "".join(parts[1:])

# Create RDF graph
g = Graph()

# Initialize variables
# Values for different datasets: gthaUpperTier, gthaLowerTier, provincialLands
dataset = "gthaUpperTier"
# Values for different datasets: GTHAUpperTier, GTHALowerTier, ProvincialLands
filename = "GTHAUpperTier"

# Get the data
data = json.loads(open(filename + ".geojson", encoding='utf8').read())

# Generate triples for each instance
for element in data["features"]:
    # Initialize variables
    objectid = str(element['properties']['OBJECTID_1'])
    tier = camelcase(str(element['properties']['Tier']))
    
    g.add((toronto[dataset + "Property" + objectid], RDF.type, hp.Parcel))
    g.add((toronto[dataset + "Property" + objectid], hp.ownership, hp[tier + "Org"]))
    
    if (hp[tier + "Org"], RDF.type, org_city.GovernmentOrganization) not in g:
        g.add((hp[tier + "Org"], RDF.type, org_city.GovernmentOrganization))
        
    g.add((toronto[dataset + "Property" + objectid + "Loc"], RDF.type, loc.Location))  
    g.add((toronto[dataset + "Property" + objectid], loc.hasLocation, toronto[dataset + "Property" + objectid + "Loc"]))
    g.add((toronto[dataset + "Property" + objectid + "Loc"], geo.asWKT, Literal(shapely.to_wkt(make_valid(shapely.geometry.shape(element["geometry"])), rounding_precision=-1), datatype=geo.wktLiteral)))

# Export the RDF graph as a .ttl file
g.serialize(destination= filename + ".ttl")
    






