# -*- coding: utf-8 -*-
"""
Childcare.py

Author: Anderson Wong

Date: November 27, 2025

Description: This is a Python program that generates RDF triples 
for child care data using Microsoft Excel data.
"""

# Import modules
import rdflib
import pandas
import shapely
import json

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
change = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Change/')

# Create RDF graph
g = Graph()
g2 = Graph()

# Get the data
df = pandas.read_excel("ChildCare.xlsx")

g.add((cdt.ChildcareServiceSite, rdfs.subClassOf, cdt.Site))

# Iterate through each row of the Excel table
for idx, row in df.iterrows():
    objectid = str(row["_id"])
    
    g.add((toronto["childcareservice_toronto" + objectid], RDF.type, hp.ChildcareService))
    g.add((toronto["childcareservice_toronto" + objectid], hp.providedFromSite, toronto["childcareservice_toronto" + objectid + "Site"]))
    
    g.add((toronto["childcareservice_toronto" + objectid + "Site"], RDF.type, cdt.ChildcareServiceSite))
    g.add((toronto["childcareservice_toronto" + objectid + "Site"], genprop.hasIdentifier, Literal(row["LOC_ID"])))
    g.add((toronto["childcareservice_toronto" + objectid + "Site"], genprop.hasName, Literal(row["LOC_NAME"])))
    
    g.add((toronto["childcareservice_toronto" + objectid + "Site"], loc.hasLocation, toronto["childcareservice_toronto" + objectid + "SiteLoc"]))
    g.add((toronto["childcareservice_toronto" + objectid + "SiteLoc"], geo.asWKT, Literal(shapely.to_wkt(shapely.geometry.shape(json.loads(row["geometry"]))), datatype=geo.wktLiteral)))
    
    g.add((toronto["childcareservice_toronto" + objectid], res.hasCapacity, toronto["childcareservice_toronto" + objectid + "Capacity"]))
    g.add((toronto["childcareservice_toronto" + objectid + "Capacity"], RDF.type, hp.ChildcareEnrollmentSpaces))
    g.add((toronto["childcareservice_toronto" + objectid + "Capacity"], iso21972.hasValue, toronto["childcareservice_toronto" + objectid + "CapacityMeasure"]))
    
    g.add((toronto["childcareservice_toronto" + objectid + "CapacityMeasure"], RDF.type, iso21972.Measure))
    g.add((toronto["childcareservice_toronto" + objectid + "CapacityMeasure"], iso21972.hasNumericalValue, Literal(row["TOTSPACE"])))
    g.add((toronto["childcareservice_toronto" + objectid + "CapacityMeasure"], iso21972.hasUnit, iso21972.population_cardinality_unit))

    g2.add((toronto["childcareservice_toronto" + objectid], res.capacityInUse, toronto["childcareservice_toronto" + objectid + "CapacityUse"]))
    g2.add((toronto["childcareservice_toronto" + objectid + "CapacityUse"], RDF.type, hp.ChildcareEnrollmentSize))
    g2.add((toronto["childcareservice_toronto" + objectid + "CapacityUse"], iso21972.hasValue, toronto["childcareservice_toronto" + objectid + "CapacityUseMeasure"]))
    
    g2.add((toronto["childcareservice_toronto" + objectid + "CapacityUseMeasure"], RDF.type, iso21972.Measure))
    g2.add((toronto["childcareservice_toronto" + objectid + "CapacityUseMeasure"], iso21972.hasNumericalValue, Literal(row["FAKE ENROLLMENT"])))
    g2.add((toronto["childcareservice_toronto" + objectid + "CapacityUseMeasure"], iso21972.hasUnit, iso21972.population_cardinality_unit))

# Export the RDF graph as a .ttl file    
g.serialize(destination="Childcare.ttl")
g2.serialize(destination="ChildcareSynthetic.ttl")
