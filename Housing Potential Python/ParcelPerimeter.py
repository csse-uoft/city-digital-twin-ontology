# -*- coding: utf-8 -*-
"""
ParcelPerimeter.py

Author: Anderson Wong

Date: December 5, 2025

Description: This is a Python program that generates RDF triples 
for parcel perimeters using data from a GeoJSON file.
"""

# Import modules
import rdflib
import geopandas

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

# Create RDF graph
g = Graph()

# Get the data and remove unused columns
perimeter = geopandas.read_file("PropertyBoundaries_4326_with_perimeter.geojson")
perimeter = perimeter.drop(columns=["fid", "F_id","FEATURE_TYPE", "DATE_EFFECTIVE", "DATE_EXPIRY", "STATEDAREA", "ADDRESS_NUMBER", "LINEAR_NAME_FULL", "TRANS_ID_CREATE", "TRANS_ID_EXPIRE"])

# Generate triples for each row
for idx, row in perimeter.iterrows():
    # Initialize variables
    parcelid = str(row['PARCELID'])
    
    g.add((toronto["Property" + parcelid], hp.hasPerimeter, toronto["PropertyPerimeter" + parcelid]))
    g.add((toronto["PropertyPerimeter" + parcelid], iso21972.hasValue, toronto["PropertyPerimeterMeasure" + parcelid]))
    g.add((toronto["PropertyPerimeterMeasure" + parcelid], iso21972.hasNumericalValue, Literal(row['Perimeter'])))
    g.add((toronto["PropertyPerimeterMeasure" + parcelid], iso21972.hasUnit, iso21972.metre))

# Export the RDF graph as a .ttl file
g.serialize(destination="ParcelPerimeter.ttl")