# -*- coding: utf-8 -*-
"""
Hospital.py

Author: Anderson Wong

Date: December 4, 2025

Description: This is a Python program that generates RDF triples 
for hospitals using OpenStreetMap data in a geojson file.
    
"""

# Import modules
import rdflib
import pandas

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
contact = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Contact/')
org_city = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Organization/')
org = rdflib.Namespace('http://www.w3.org/ns/org#')
res = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Resource/')
iso21972 = rdflib.Namespace('http://ontology.eil.utoronto.ca/ISO21972/iso21972#')
hp = rdflib.Namespace('http://ontology.eil.utoronto.ca/HPCDM/')

# Create RDF graph
g = Graph()

# Get the data
df = pandas.read_excel("HospitalCapacity.xlsx")

# Iterate through each row of the Excel table
for idx, row in df.iterrows():
    if row["Place or organization"] == "North York General Hospital (Ont.)":
        instancename = "684426043Hospital"
        
    elif row["Place or organization"] == "Michael Garron Hospital Corporation (Ont.)":
        instancename = "447744987Hospital"

    elif row["Place or organization"] == "Hospital for Sick Children (Ont.)":
        instancename = "712078929Hospital"
        
    else:
        continue
    
    g.add((toronto[instancename + "Service"], res.capacityInUse, toronto[instancename + "CapacityUse"]))
    g.add((toronto[instancename + "CapacityUse"], iso21972.hasValue, toronto[instancename + "CapacityUseMeasure"]))

    g.add((toronto[instancename + "CapacityUseMeasure"], RDF.type, iso21972.Measure))
    g.add((toronto[instancename + "CapacityUseMeasure"], iso21972.hasNumericalValue, Literal(row['Metric value'])))
    g.add((toronto[instancename + "CapacityUseMeasure"], iso21972.hasUnit, hp.avg_inpatients_daily_per_bed))

    g.add((toronto[instancename + "Service"], res.hasCapacity, toronto[instancename + "Capacity"]))
    g.add((toronto[instancename + "Capacity"], iso21972.hasValue, toronto[instancename + "CapacityMeasure"]))

    g.add((toronto[instancename + "CapacityMeasure"], RDF.type, iso21972.Measure))
    g.add((toronto[instancename + "CapacityMeasure"], iso21972.hasNumericalValue, Literal(1)))
    g.add((toronto[instancename + "CapacityMeasure"], iso21972.hasUnit, hp.avg_inpatients_daily_per_bed))
    
# Export the RDF graph as a .ttl file    
g.serialize(destination="HospitalCapacity.ttl")





