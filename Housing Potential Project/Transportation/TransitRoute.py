# -*- coding: utf-8 -*-
"""
TransitRoute.py

Author: Anderson Wong

Date: February 17, 2025

Description: This is a Python program that generates RDF triples 
for transit routes from GTFS data.
    
"""
import os
import pandas as pd
import rdflib

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
org = rdflib.Namespace('http://www.w3.org/ns/org#')
hp = rdflib.Namespace('http://ontology.eil.utoronto.ca/HPCDM/')
iso21972 = rdflib.Namespace('http://ontology.eil.utoronto.ca/ISO21972/iso21972#')
res = rdflib.Namespace('https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Resource/')

# Load files
routes = pd.read_csv(os.path.join(os.getcwd(), "TTC", "routes.txt"))
trips = pd.read_csv((os.path.join(os.getcwd(), "TTC", "trips.txt")))
stop_times = pd.read_csv((os.path.join(os.getcwd(), "TTC", "stop_times.txt")))
capacity = pd.read_excel("TTCCapacity.xlsx")

# Create RDF graph
g = Graph()

# Create empty dictionary
d = {}

# Merge trips with stop_times to connect route_id -> trip_id -> stop_id
trips_stop_times = pd.merge(trips[['trip_id', 'route_id']], 
                            stop_times[['trip_id', 'stop_id']], 
                            on='trip_id')

# Group by route_id and collect unique stop_ids
route_stops = trips_stop_times.groupby('route_id')['stop_id'].unique().reset_index()

# Merge Pandas dataframes into route_stops
route_stops = pd.merge(route_stops, routes[['route_id', 'route_long_name', 'route_short_name']], on='route_id')
route_stops = pd.merge(route_stops, capacity[['route_short_name', 'Ridership']], on='route_short_name')

# Convert numpy arrays to lists for readability
route_stops['stop_id'] = route_stops['stop_id'].apply(list)

# Generate triples for each route
for _, row in route_stops.iterrows():
    routeid = str(row['route_id'])
    
    g.add((toronto[routeid + "RouteService"], RDF.type, toronto.TorPublicTransitService))   
    g.add((toronto.ttc, cdt.providesService, toronto[routeid + "RouteService"])) 
    g.add((toronto[routeid + "RouteService"], genprop.hasName, Literal(row['route_long_name'])))   
    g.add((toronto[routeid + "RouteService"], genprop.hasIdentifier, Literal(row['route_short_name'])))
    
    g.add((toronto[routeid + "RouteService"], res.capacityInUse, toronto[routeid + "RouteServiceCapacityUse"]))
    g.add((toronto[routeid + "RouteServiceCapacityUse"], RDF.type, hp.PassengerThroughputRate))
    
    g.add((toronto[routeid + "RouteServiceCapacityUse"], iso21972.hasValue, toronto[routeid + "RouteServiceCapacityUseMeasure"]))
    g.add((toronto[routeid + "RouteServiceCapacityUseMeasure"], RDF.type, iso21972.Measure))
    try:
        g.add((toronto[routeid + "RouteServiceCapacityUseMeasure"], iso21972.hasNumericalValue, Literal(int(row['Ridership']))))
        d[routeid] = int(row['Ridership'])
    except:
        g.add((toronto[routeid + "RouteServiceCapacityUseMeasure"], iso21972.hasNumericalValue, Literal(0)))
        d[routeid] = 0
    g.add((toronto[routeid + "RouteServiceCapacityUseMeasure"], iso21972.hasUnit, hp.person_per_day))
    
    # Generate triples for each stop
    for stop in row['stop_id']:
        g.add((toronto[routeid + "RouteService"], hp.providedFromSite, toronto[str(stop) + "TransitStop"]))   

# Load files for synthetic data
synthetic = pd.read_csv("TTCSynthetic.csv")

# Create RDF graph
g2 = Graph()

# Generate triples for each route
for row in synthetic.itertuples():
    routeid = str(row.route_id)
    
    try:
        g2.add((toronto[routeid + "RouteServiceCapacityAvailMeasure"], iso21972.hasNumericalValue, Literal(int(row.daily_passenger_throughput) - d[str(routeid)])))   
    
        g2.add((toronto[routeid + "RouteService"], res.hasCapacity, toronto[routeid + "RouteServiceCapacityTotal"]))   
        
        g2.add((toronto[routeid + "RouteServiceCapacityTotal"], iso21972.hasValue, toronto[routeid + "RouteServiceCapacityTotalMeasure"]))  
        g2.add((toronto[routeid + "RouteServiceCapacityTotal"], RDF.type, hp.MinPassengerThroughputRate))   
    
        g2.add((toronto[routeid + "RouteServiceCapacityTotalMeasure"], RDF.type, iso21972.Measure))   
        g2.add((toronto[routeid + "RouteServiceCapacityTotalMeasure"], iso21972.hasNumericalValue, Literal(row.daily_passenger_throughput)))   
        g2.add((toronto[routeid + "RouteServiceCapacityTotalMeasure"], iso21972.hasUnit, hp.person_per_day))   
    
        g2.add((toronto[routeid + "RouteService"], res.hasAvailableCapacity, toronto[routeid + "RouteServiceCapacityAvail"]))   
        
        g2.add((toronto[routeid + "RouteServiceCapacityAvail"], iso21972.hasValue, toronto[routeid + "RouteServiceCapacityAvailMeasure"]))  
        g2.add((toronto[routeid + "RouteServiceCapacityAvail"], RDF.type, hp.AvailablePassengerThroughputRate))   
    
        g2.add((toronto[routeid + "RouteServiceCapacityAvailMeasure"], RDF.type, iso21972.Measure))   
        g2.add((toronto[routeid + "RouteServiceCapacityAvailMeasure"], iso21972.hasUnit, hp.person_per_day))   
    except:
        print (routeid)
        
# Export the RDF graph as a .ttl file
g2.serialize(destination="TransitSynthetic.ttl")

# Export the RDF graph as a .ttl file
g.serialize(destination="TransitRoute.ttl")