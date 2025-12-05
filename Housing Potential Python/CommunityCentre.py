# -*- coding: utf-8 -*-
"""
Community Centre.py

Author: Anderson Wong

Date: December 1, 2025

Description: This is a Python program that generates RDF triples 
for community centres using data in a Microsoft Excel file.
    
"""

# Import modules
import rdflib
import json
import rdftools
import re
import geopandas
import shapely
import pandas
import ast

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

# Get the data
df = pandas.read_excel("Parks and Recreation Facilities - 4326 fake_capacity.xlsx")

g.add((cdt.CommunityCentreSite, rdfs.subClassOf, cdt.Site))

# Iterate through each row of the Excel table
for idx, row in df.iterrows():
    if row['TYPE'] == "Community Centre":
        objectid = str(row['_id'])
        siteid = str(row['ASSET_ID'])
        
        g.add((toronto["communitycentre_service" + objectid], RDF.type, hp.CommunityCentreService))
        g.add((toronto["communitycentre_service" + objectid], hp.providedFromSite, toronto["communitycentresite" + objectid]))
        
        g.add((toronto["communitycentresite" + objectid], RDF.type, cdt.CommunityCentreSite))
        g.add((toronto["communitycentresite" + objectid], genprop.hasName, Literal(row['ASSET_NAME'])))
        g.add((toronto["communitycentresite" + objectid], genprop.hasIdentifier, Literal(row['ASSET_ID'])))
        g.add((toronto["communitycentresite" + objectid], loc.hasLocation, toronto["communitycentresite" + objectid + "_location"]))
        
        g.add((toronto["communitycentresite" + objectid + "_location"], RDF.type, loc.Location))
        g.add((toronto["communitycentresite" + objectid + "_location"], geo.asWKT, Literal(shapely.to_wkt(shapely.geometry.shape(ast.literal_eval(row["geometry"]))), datatype=geo.wktLiteral)))
        
        g2.add((toronto["communitycentre_service" + objectid], res.hasCapacity, toronto["communitycentre_service" + objectid + "Capacity"]))
        g2.add((toronto["communitycentre_service" + objectid + "Capacity"], RDF.type, hp.CommunityCentreClientSpaces))
        
        g2.add((toronto["communitycentre_service" + objectid + "Capacity"], iso21972.hasValue, toronto["communitycentre_service" + objectid + "CapacityMeasure"]))
        g2.add((toronto["communitycentre_service" + objectid + "CapacityMeasure"], RDF.type, iso21972.Measure))
        g2.add((toronto["communitycentre_service" + objectid + "CapacityMeasure"], iso21972.hasNumericalValue, Literal(row['FAKE CAPACITY'])))
        g2.add((toronto["communitycentre_service" + objectid + "CapacityMeasure"], iso21972.hasUnit, iso21972.population_cardinality_unit))
    
        g2.add((toronto["communitycentre_service" + objectid], res.capacityInUse, toronto["communitycentre_service" + objectid + "CapacityUse"]))
        g2.add((toronto["communitycentre_service" + objectid + "CapacityUse"], RDF.type, hp.CommunityCentreClientSize))
        
        g2.add((toronto["communitycentre_service" + objectid + "CapacityUse"], iso21972.hasValue, toronto["communitycentre_service" + objectid + "CapacityUseMeasure"]))
        g2.add((toronto["communitycentre_service" + objectid + "CapacityUseMeasure"], RDF.type, iso21972.Measure))
        g2.add((toronto["communitycentre_service" + objectid + "CapacityUseMeasure"], iso21972.hasNumericalValue, Literal(13903)))
        g2.add((toronto["communitycentre_service" + objectid + "CapacityUseMeasure"], iso21972.hasUnit, iso21972.population_cardinality_unit))

# Export the RDF graph as a .ttl file
g.serialize(destination= "CommunityCentre.ttl")
g2.serialize(destination= "CommunityCentreCapacity.ttl")
