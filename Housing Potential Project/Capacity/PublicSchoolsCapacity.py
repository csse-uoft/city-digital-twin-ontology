# -*- coding: utf-8 -*-
"""
PublicSchoolsCapacity.py

Author: Anderson Wong

Date: February 13, 2026

Description: This is a Python program that generates RDF triples 
for public school capacity using Microsoft Excel data.
"""

# Import modules
import rdflib
import pandas
import re

from rdflib import Graph, Literal, RDF, XSD

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
df = pandas.read_excel("PublicSchoolsEnrolment.xlsx")

# Iterate through each row of the Excel table
for idx, row in df.iterrows():
    if str(row["Board Number"]) in ("B67059", "B66052"):
        
        objectid = str(int(row["School Number"]))
        
        capacityusevalue = round(float(re.sub(r"[^\d.]", "", str(row["Enrolment"]))))
        capacityvalue = round(capacityusevalue / row["Random Capacity Factor=87.6 * (1 + (RAND() - 0.5) * 0.10)"])
        capacityavailvalue = round(capacityvalue - capacityusevalue)
        
        g.add((toronto[objectid + "SchoolService"], res.capacityInUse, toronto[objectid + "SchoolServiceCapacityUse"]))
        g.add((toronto[objectid + "SchoolServiceCapacityUse"], RDF.type, hp.SchoolEnrollmentSize))
        g.add((toronto[objectid + "SchoolServiceCapacityUse"], iso21972.hasValue, toronto[objectid + "SchoolServiceCapacityUseMeasure"]))
        
        g.add((toronto[objectid + "SchoolServiceCapacityUseMeasure"], RDF.type, iso21972.Measure))
        g.add((toronto[objectid + "SchoolServiceCapacityUseMeasure"], iso21972.hasNumericalValue, Literal(capacityusevalue)))
        g.add((toronto[objectid + "SchoolServiceCapacityUseMeasure"], iso21972.hasUnit, iso21972.population_cardinality_unit))
        
        g.add((toronto[objectid + "SchoolService"], change.existsAt, toronto["September12023August312024Interval"]))
        g.add((toronto["September12023August312024Interval"], RDF.type, time.Interval))
        g.add((toronto["September12023August312024Interval"], time.hasBeginning, toronto["September12023August312024BeginningTimeInstant"]))
        g.add((toronto["September12023August312024BeginningTimeInstant"], RDF.type, time.Instant))
        g.add((toronto["September12023August312024BeginningTimeInstant"], time.inXSDDateTimeStamp, Literal("2023-09-01T00:00:00-04:00", datatype=XSD.dateTimeStamp)))
        g.add((toronto["September12023August312024Interval"], time.hasBeginning, toronto["September12023August312024EndTimeInstant"]))
        g.add((toronto["September12023August312024EndTimeInstant"], RDF.type, time.Instant))
        g.add((toronto["September12023August312024EndTimeInstant"], time.inXSDDateTimeStamp, Literal("2024-08-31T00:00:00-04:00", datatype=XSD.dateTimeStamp)))
        
        g2.add((toronto[objectid + "SchoolService"], res.hasCapacity, toronto[objectid + "SchoolServiceCapacity"]))
        g2.add((toronto[objectid + "SchoolServiceCapacity"], RDF.type, hp.SchoolEnrollmentSpaces))
        g2.add((toronto[objectid + "SchoolServiceCapacity"], iso21972.hasValue, toronto[objectid + "SchoolServiceCapacityMeasure"]))
        
        g2.add((toronto[objectid + "SchoolServiceCapacityMeasure"], RDF.type, iso21972.Measure))
        g2.add((toronto[objectid + "SchoolServiceCapacityMeasure"], iso21972.hasNumericalValue, Literal(capacityvalue)))
        g2.add((toronto[objectid + "SchoolServiceCapacityMeasure"], iso21972.hasUnit, iso21972.population_cardinality_unit))
        
        g2.add((toronto[objectid + "SchoolService"], res.hasAvailableCapacity , toronto[objectid + "SchoolServiceCapacityAvail"]))
        g2.add((toronto[objectid + "SchoolServiceCapacityAvail"], RDF.type, hp.SchoolAvailableEnrollmentSpaces))
        g2.add((toronto[objectid + "SchoolServiceCapacityAvail"], iso21972.hasValue, toronto[objectid + "SchoolServiceCapacityAvailMeasure"]))
        
        g2.add((toronto[objectid + "SchoolServiceCapacityAvailMeasure"], RDF.type, iso21972.Measure))
        g2.add((toronto[objectid + "SchoolServiceCapacityAvailMeasure"], iso21972.hasNumericalValue, Literal(capacityavailvalue)))
        g2.add((toronto[objectid + "SchoolServiceCapacityAvailMeasure"], iso21972.hasUnit, iso21972.population_cardinality_unit))

# Export the RDF graph as a .ttl file    
g.serialize(destination="PublicSchoolsEnrollment.ttl")
g2.serialize(destination="PublicSchoolsCapacity.ttl")
