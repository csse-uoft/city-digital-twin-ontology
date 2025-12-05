# -*- coding: utf-8 -*-
"""
SewerGravityMainCapacity.py

Author: Anderson Wong

Date: November 20, 2025

Description: This is a Python program that generates RDF triples 
for waste water services capacity using synthetic data from a CSV file.
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

df = pandas.read_csv("SewerGravityMainCapacity.csv")

# Iterate through each row of the Excel table
for idx, row in df.iterrows():
    objectid = str(row['_id'])
    
    g.add((toronto["wastewaterservicegravitymain" + objectid], res.hasCapacity, toronto["wastewaterservicegravitymain" + objectid + "Capacity"]))
    g.add((toronto["wastewaterservicegravitymain" + objectid + "Capacity"], iso21972.hasValue, toronto["wastewaterservicegravitymain" + objectid + "CapacityMeasure"]))
    
    g.add((toronto["wastewaterservicegravitymain" + objectid + "CapacityMeasure"], RDF.type, iso21972.Measure))
    g.add((toronto["wastewaterservicegravitymain" + objectid + "CapacityMeasure"], iso21972.hasNumericalValue,  Literal(row['Est Flow Capacity (m3/year)'])))
    g.add((toronto["wastewaterservicegravitymain" + objectid + "CapacityMeasure"], iso21972.hasUnit,  hp.cubic_metre_per_year))
    
    g.add((toronto["wastewaterservicegravitymain" + objectid], res.capacityInUse, toronto["wastewaterservicegravitymain" + objectid + "CapacityUse"]))
    g.add((toronto["wastewaterservicegravitymain" + objectid + "CapacityUse"], RDF.type, hp.WaterProcessingRate))
    g.add((toronto["wastewaterservicegravitymain" + objectid + "CapacityUse"], iso21972.hasValue, toronto["wastewaterservicegravitymain" + objectid + "CapacityUseMeasure"]))

    g.add((toronto["wastewaterservicegravitymain" + objectid + "CapacityUseMeasure"], RDF.type, iso21972.Measure))
    g.add((toronto["wastewaterservicegravitymain" + objectid + "CapacityUseMeasure"], iso21972.hasNumericalValue,  Literal(row['Synthetic (Randomized) utilization'])))
    g.add((toronto["wastewaterservicegravitymain" + objectid + "CapacityUseMeasure"], iso21972.hasUnit,  hp.cubic_metre_per_year))

    g.add((toronto["wastewaterservicegravitymain" + objectid], res.hasAvailableCapacity, toronto["wastewaterservicegravitymain" + objectid + "CapacityAvail"]))
    g.add((toronto["wastewaterservicegravitymain" + objectid + "CapacityAvail"], iso21972.hasValue, toronto["wastewaterservicegravitymain" + objectid + "CapacityAvailMeasure"]))

    g.add((toronto["wastewaterservicegravitymain" + objectid + "CapacityAvailMeasure"], RDF.type, iso21972.Measure))
    g.add((toronto["wastewaterservicegravitymain" + objectid + "CapacityAvailMeasure"], iso21972.hasNumericalValue,  Literal(row['Synthetic Available Capacity'])))
    g.add((toronto["wastewaterservicegravitymain" + objectid + "CapacityAvailMeasure"], iso21972.hasUnit,  hp.cubic_metre_per_year))

# Export the RDF graph as a .ttl file
g.serialize(destination="SewerGravityMainCapacity.ttl")






