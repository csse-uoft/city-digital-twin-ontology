# -*- coding: utf-8 -*-
"""
TransitSynthetic.py

Author: Anderson Wong

Date: November 18, 2025

Description: This is a Python program that generates RDF triples 
for synthetic transit capacity data.
    
"""
import os
import pandas as pd
import rdflib

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
hp = rdflib.Namespace('http://ontology.eil.utoronto.ca/HPCDM/')
iso21972 = rdflib.Namespace('http://ontology.eil.utoronto.ca/ISO21972/iso21972#')
res = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Resource/')

# Load files
synthetic = pd.read_csv("TTCSynthetic.csv")

# Create RDF graph
g = Graph()

# Generate triples for each route
for _, row in synthetic.iterrows():
    routeid = str(row['route_id'])
    
    g.add((toronto[routeid + "RouteService"], res.hasCapacity, toronto[routeid + "RouteServiceCapacityTotal"]))   
    
    g.add((toronto[routeid + "RouteServiceCapacityTotal"], iso21972.hasValue, toronto[routeid + "RouteServiceCapacityTotalMeasure"]))  
    g.add((toronto[routeid + "RouteServiceCapacityTotal"], RDF.type, hp.PassengerThroughputRate))   

    g.add((toronto[routeid + "RouteServiceCapacityTotalMeasure"], RDF.type, iso21972.Measure))   
    g.add((toronto[routeid + "RouteServiceCapacityTotalMeasure"], iso21972.hasNumericalValue, Literal(row['daily_passenger_throughput'])))   
    g.add((toronto[routeid + "RouteServiceCapacityTotalMeasure"], iso21972.hasUnit, hp.person_per_day))   

# Export the RDF graph as a .ttl file
g.serialize(destination="TransitSynthetic.ttl")