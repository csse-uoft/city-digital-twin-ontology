# -*- coding: utf-8 -*-
"""
ZoningSynthetic.py

Author: Anderson Wong

Date: December 3, 2025

Description: This is a Python program that generates RDF triples 
for synthetic zoning using data from a CSV file.
"""

# Import modules
import rdflib
import rdftools
import pandas

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
oz = rdflib.Namespace('http://www.theworldavatar.com/ontology/ontozoning/OntoZoning.owl#')

# Create RDF graph
g = Graph()

# Load the data
df = pandas.read_csv("zoning_landuse.csv")

# Generate triples for each row
for idx, row in df.iterrows():
    objectid = str(row["Zone Symbol"])
    alloweduse = rdftools.toUpperCamelCase(str(row["Allowed Use"]))
    
    g.add((toronto["zone_" + objectid], RDF.type, hp.ZoningType))
    g.add((toronto["zone_" + objectid], genprop.hasName, Literal(str(row["Zone Category"]))))
    g.add((toronto["zone_" + objectid], oz.allowsUse, toronto[alloweduse]))
    g.add((toronto[alloweduse], genprop.hasName, Literal(str(row["Allowed Use"]))))

# Export the RDF graph as a .ttl file
g.serialize(destination="ZoningSynthetic.ttl")
