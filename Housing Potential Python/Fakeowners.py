# -*- coding: utf-8 -*-
"""
SyntheticOwnership.py

Author: Anderson Wong

Date: November 14, 2025

Description: This is a Python program that generates RDF triples 
for synthetic parcel ownership data.
"""

import pandas
import rdflib
import usaddress
import phonenumbers
import math

from shapely.geometry import Point
from geopy.geocoders import ArcGIS
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

geolocator = ArcGIS()

# Create RDF graph
g = Graph()

# Get the data
df1 = pandas.read_csv("Fakeowners1.csv")
df2 = pandas.read_csv("Fakeowners1.csv")

df = pandas.concat([df1, df2], ignore_index=True)

for idx, row in df.iterrows():
    parcelid = str(row['PARCELID'])
    ownername = row['Fake Owner'].replace(" ", "")
    
    g.add((toronto["Property" + parcelid], hp.ownership, toronto["Property" + parcelid + ownername]))
    g.add((toronto["Property" + parcelid], hp.ownership, toronto["Property" + parcelid + ownername]))
    g.add((toronto["Property" + parcelid + ownername], genprop.hasName, Literal(row['Fake Owner'])))

# Export the RDF graph as a .ttl file    
g.serialize(destination="Fakeowners.ttl")
