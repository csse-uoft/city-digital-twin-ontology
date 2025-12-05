# -*- coding: utf-8 -*-
"""
SolidWasteCapacity.py

Author: Anderson Wong

Date: November 20, 2025

Description: This is a Python program that generates RDF triples 
for solid waste services capacity using synthetic data from a CSV file.
"""

# Import modules
import rdflib
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
org_city = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Organization/')
res = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Resource/')

# Create RDF graph
g = Graph()

df = pandas.read_csv("SolidWasteCapacity.csv")

# Iterate through each row of the CSV table
for idx, row in df.iterrows():
    objectid = str(idx)
    
    g.add((toronto["solidwaste_service" + objectid], res.hasCapacity, toronto["solidwaste_service" + objectid + "Capacity"]))
    g.add((toronto["solidwaste_service" + objectid + "Capacity"], iso21972.hasValue, toronto["solidwaste_service" + objectid + "CapacityMeasure"]))
    
    g.add((toronto["solidwaste_service" + objectid + "CapacityMeasure"], RDF.type, iso21972.Measure))
    g.add((toronto["solidwaste_service" + objectid + "CapacityMeasure"], iso21972.hasNumericalValue,  Literal(row['Randomized total capacity per area'])))
    g.add((toronto["solidwaste_service" + objectid + "CapacityMeasure"], iso21972.hasUnit,  hp.tonnes_per_year))
    
    g.add((toronto["solidwaste_service" + objectid], res.capacityInUse, toronto["solidwaste_service" + objectid + "CapacityUse"]))
    g.add((toronto["solidwaste_service" + objectid + "CapacityUse"], RDF.type, hp.WasteProcessingRate))
    g.add((toronto["solidwaste_service" + objectid + "CapacityUse"], iso21972.hasValue, toronto["solidwaste_service" + objectid + "CapacityUseMeasure"]))

    g.add((toronto["solidwaste_service" + objectid + "CapacityUseMeasure"], RDF.type, iso21972.Measure))
    g.add((toronto["solidwaste_service" + objectid + "CapacityUseMeasure"], iso21972.hasNumericalValue,  Literal(row['Estimated Capacity in use(tonnes / year)'])))
    g.add((toronto["solidwaste_service" + objectid + "CapacityUseMeasure"], iso21972.hasUnit,  hp.tonnes_per_year))

    g.add((toronto["solidwaste_service" + objectid], res.hasAvailableCapacity, toronto["solidwaste_service" + objectid + "CapacityAvail"]))
    g.add((toronto["solidwaste_service" + objectid + "CapacityAvail"], iso21972.hasValue, toronto["solidwaste_service" + objectid + "CapacityAvailMeasure"]))

    g.add((toronto["solidwaste_service" + objectid + "CapacityAvailMeasure"], RDF.type, iso21972.Measure))
    g.add((toronto["solidwaste_service" + objectid + "CapacityAvailMeasure"], iso21972.hasNumericalValue,  Literal(row['Available capacity'])))
    g.add((toronto["solidwaste_service" + objectid + "CapacityAvailMeasure"], iso21972.hasUnit,  hp.tonnes_per_year))

# Export the RDF graph as a .ttl file
g.serialize(destination="SolidWasteCapacity.ttl")






