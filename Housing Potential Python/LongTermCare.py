# -*- coding: utf-8 -*-
"""
LongTermCare.py

Author: Anderson Wong

Date: November 25, 2025

Description: This is a Python program that generates RDF triples 
for long term care services using synthetic data from a SHP file.
"""

# Import modules
import rdflib
import geopandas
import pandas
import shapely
import os

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
g2 = Graph()

df = geopandas.read_file(os.path.join(os.getcwd(), "LongTermCare", "city_operated_long_term_care_wgs84", "city_op_long_term_care_wgs84.shp"))
df2 = pandas.read_excel("long_term_care_locations_wgs84_withfakeoccupancy.xlsx")

df = df.merge(df2, on="ID")

g.add((cdt.SeniorCareServiceSite, rdfs.subClassOf, cdt.Site))


# Iterate through each row of the CSV table
for idx, row in df.iterrows():
    objectid = str(idx)
    
    g.add((toronto["seniorcare_service" + objectid], RDF.type, hp.SeniorCareService))
    g.add((toronto["seniorcare_service" + objectid], hp.providedFromSite, toronto["seniorcare_service_site" + objectid]))
    
    g.add((toronto["seniorcare_service_site" + objectid], RDF.type, cdt.SeniorCareServiceSite))
    g.add((toronto["seniorcare_service_site" + objectid], genprop.hasIdentifier, Literal(row['ID'])))
    g.add((toronto["seniorcare_service_site" + objectid], genprop.hasName, Literal(row['NAME_x'])))
    
    g.add((toronto["seniorcare_service" + objectid], res.hasCapacity, toronto["seniorcare_service" + objectid + "Capacity"]))

    g.add((toronto["seniorcare_service" + objectid + "Capacity"], RDF.type, hp.NumberOfLongTermCareBeds))
    g.add((toronto["seniorcare_service" + objectid + "Capacity"], iso21972.hasValue, toronto["seniorcare_service" + objectid + "CapacityMeasure"]))

    g.add((toronto["seniorcare_service" + objectid + "CapacityMeasure"], RDF.type, iso21972.Measure))
    g.add((toronto["seniorcare_service" + objectid + "CapacityMeasure"], iso21972.hasNumericalValue, Literal(row['BEDS_x'])))
    g.add((toronto["seniorcare_service" + objectid + "CapacityMeasure"], iso21972.hasUnit, iso21972.population_cardinality_unit))

    g.add((toronto["seniorcare_service_site" + objectid], loc.hasLocation, toronto["seniorcare_service_site_location" + objectid]))
    g.add((toronto["seniorcare_service_site_location" + objectid], RDF.type, loc.Location))
    g.add((toronto["seniorcare_service_site_location" + objectid], geo.asWKT, Literal(shapely.to_wkt(shapely.geometry.shape(row["geometry"])), datatype=geo.wktLiteral)))
    
    g2.add((toronto["seniorcare_service" + objectid], res.capacityInUse, toronto["seniorcare_service" + objectid + "CapacityUse"]))
    g2.add((toronto["seniorcare_service" + objectid + "CapacityUse"], iso21972.hasValue, toronto["seniorcare_service" + objectid + "CapacityUseMeasure"]))

    g2.add((toronto["seniorcare_service" + objectid + "CapacityUseMeasure"], RDF.type, iso21972.Measure))
    g2.add((toronto["seniorcare_service" + objectid + "CapacityUseMeasure"], iso21972.hasNumericalValue, Literal(round(row['Fake occupancy']))))
    g2.add((toronto["seniorcare_service" + objectid + "CapacityUseMeasure"], iso21972.hasUnit, iso21972.population_cardinality_unit))
    
# Export the RDF graph as a .ttl file
g.serialize(destination="LongTermCare.ttl")
g2.serialize(destination="LongTermCareCapacity.ttl")






