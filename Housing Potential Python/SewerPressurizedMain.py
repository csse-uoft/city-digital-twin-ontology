# -*- coding: utf-8 -*-
"""
SewerPressurizedMain.py

Author: Anderson Wong

Date: November 18, 2025

Description: This is a Python program that generates RDF triples 
for waste water services using data from a GeoJSON file.
"""

# Import modules
import rdflib
import json
import shapely

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

# Create RDF graph
g = Graph()

# Initialize variables
filename = "SewerPressurizedMain.geojson"

# Get the data
data = json.loads(open(filename, encoding='utf8').read())

g.add((cdt.PressurizedMainSite, rdfs.subClassOf, cdt.Site))


# Generate triples for each instance
for element in data["features"]:
    # Initialize variables
    objectid = str(element['properties']['_id'])
    
    g.add((toronto["wastewaterservicepressurizedmain" + objectid], RDF.type, hp.WasteWaterService))
    g.add((toronto["wastewaterservicepressurizedmain" + objectid], hp.providedFromSite, toronto["wastewaterservice_pressurizedmain" + objectid + "Site"]))
    
    g.add((toronto["wastewaterservice_pressurizedmain" + objectid + "Site"], RDF.type, cdt.PressurizedMainSite))
    g.add((toronto["wastewaterservice_pressurizedmain" + objectid + "Site"], genprop.hasIdentifier, Literal(element['properties']['Sewer Pressurized Asset Identification'])))
        
    g.add((toronto["wastewaterservice_pressurizedmain_loc" + objectid], RDF.type, loc.Location))  
    g.add((toronto["wastewaterservice_pressurizedmain" + objectid + "Site"], loc.hasLocation, toronto["wastewaterservice_pressurizedmain_loc" + objectid]))
    g.add((toronto["wastewaterservice_pressurizedmain_loc" + objectid], geo.asWKT, Literal(shapely.to_wkt(shapely.geometry.shape(element["geometry"])), datatype=geo.wktLiteral)))

# Export the RDF graph as a .ttl file
g.serialize(destination="SewerPressurizedMain.ttl")
    






