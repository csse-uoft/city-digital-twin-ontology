# -*- coding: utf-8 -*-
"""
FeederCapacity.py

Author: Anderson Wong

Date: November 25, 2025

Description: This is a Python program that generates RDF triples 
for hydro power services using data from a CSV file.
"""

# Import modules
import rdflib
import pandas
import re
import json

from shapely.geometry import Polygon
from shapely.ops import transform
from pyproj import Transformer
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
service = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/CityService/')


def extract_max_value(text):
    # Remove commas for easier parsing
    clean_text = text.replace(",", "")
    
    # Case 1: Range like "0–499 kVA"
    range_match = re.match(r"(\d+)\D+(\d+)", clean_text)
    if range_match:
        return int(range_match.group(2))  # take the upper bound
    
    # Case 2: Plus like "2000+ kVA"
    plus_match = re.match(r"(\d+)\+", clean_text)
    if plus_match:
        return int(plus_match.group(1))  # take the number before '+'
    
    # Fallback: just extract the largest number
    numbers = re.findall(r"\d+", clean_text)
    return max(map(int, numbers)) if numbers else None

def rings_to_wkt(rings):
    """
    Convert an Esri JSON polygon string from EPSG:3857 to EPSG:4326 and return WKT.
    """
    # Replace single quotes with double quotes
    rings = rings.replace("'", '"')
    
    # Step 1: Parse the JSON string
    geom_dict = json.loads(rings)
    rings = geom_dict.get("rings", [])
    if not rings:
        raise ValueError("No rings found in Esri JSON")

    # Step 2: Build Shapely polygon
    exterior = rings[0]
    holes = rings[1:] if len(rings) > 1 else None
    polygon = Polygon(shell=exterior, holes=holes)

    # Step 3: Define transformer (EPSG:3857 → EPSG:4326)
    transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

    # Step 4: Transform coordinates
    polygon_4326 = transform(transformer.transform, polygon)
    
    # Step 5: Return WKT
    return polygon_4326.wkt

# Create RDF graph
g = Graph()
g2 = Graph()

df = pandas.read_csv("FeederCapacity.csv")
df2 = pandas.read_csv("FeederTotal.csv", encoding="iso-8859-1")

df = df.merge(df2, on="Network_id")

# Iterate through each row of the Excel table
for idx, row in df.iterrows():
    objectid = str(row['Network_id'])
    
    g.add((toronto["hydro_feeder_service" + objectid], RDF.type, hp.ElectricService))
    g.add((toronto["hydro_feeder_service" + objectid], genprop.hasIdentifier, Literal(row['Network_id'])))
    g.add((toronto["hydro_feeder_service" + objectid], service.hasCatchmentArea, toronto["hydro_feeder_service" + objectid + "Area" + str(row['OBJECTID_x'])]))
    
    g.add((toronto["hydro_feeder_service" + objectid + "Area" + str(row['OBJECTID_x'])], RDF.type, loc.Location))
    g.add((toronto["hydro_feeder_service" + objectid + "Area" + str(row['OBJECTID_x'])], geo.asWKT, Literal(rings_to_wkt(row["SHAPE"]))))
    
    g.add((toronto["hydro_feeder_service" + objectid], res.hasAvailableCapacity, toronto["hydro_feeder_service" + objectid + "CapacityAvail"]))
    g.add((toronto["hydro_feeder_service" + objectid + "CapacityAvail"], iso21972.hasValue, toronto["hydro_feeder_service" + objectid + "CapacityAvailMeasure"]))

    g.add((toronto["hydro_feeder_service" + objectid + "CapacityAvailMeasure"], RDF.type, iso21972.Measure))
    g.add((toronto["hydro_feeder_service" + objectid + "CapacityAvailMeasure"], iso21972.hasNumericalValue,  Literal(extract_max_value(row['Feeder_Capacity_x']))))
    g.add((toronto["hydro_feeder_service" + objectid + "CapacityAvailMeasure"], iso21972.hasUnit,  hp.kilovolt_ampere))
    
    g2.add((toronto["hydro_feeder_service" + objectid], res.hasCapacity, toronto["hydro_feeder_service" + objectid + "Capacity"]))
    g2.add((toronto["hydro_feeder_service" + objectid + "Capacity"], iso21972.hasValue, toronto["hydro_feeder_service" + objectid + "CapacityMeasure"]))
    
    g2.add((toronto["hydro_feeder_service" + objectid + "CapacityMeasure"], RDF.type, iso21972.Measure))
    g2.add((toronto["hydro_feeder_service" + objectid + "CapacityMeasure"], iso21972.hasNumericalValue,  Literal(row['Fake Max Avail Capacity (kVA)'])))
    g2.add((toronto["hydro_feeder_service" + objectid + "CapacityMeasure"], iso21972.hasUnit,  hp.kilovolt_ampere))


# Export the RDF graph as a .ttl file
g.serialize(destination="FeederCapacity.ttl")
g2.serialize(destination="FeederTotal.ttl")





