# city-digital-twin-ontology
## Introduction
The City Digital Twin project at the University of Toronto’s Urban Data Research Centre aims to develop a digital twin of the City of Toronto. It builds on existing city data standards such as ISO/IEC 21972:2020, ISO/IEC 5087-1:2024, and ISO/IEC 5087-2:2024, and conforms to Linked Data requirements.  The goal of this project is to demonstrate standards-based semantic interoperability of city data. These standard ontologies enable the integration of data from multiple sources, opening up new possibilities for the development of data analysis and visualization tools.  Our City Digital Twin is represented as a knowledge graph containing a growing variety of city data (e.g. Canadian Census, Toronto Police Crime Data, City transportation infrastructure, parks, food stores, schools, …).  Our City Digital Twin also supports a dashboard that can generate data visualizations using the city data from the graph database.  

This GitHub repository contains documentation and code used to map and transform data for the City Digital Twin graph:
- The Diagrams folder contains ontology diagrams that outline the classes and properties used for representing information in the City Digital Twin
- The Documentation folder contains documentation for the City Digital Twin
- The OpenStreetMap folder contains code for mapping OpenStreetMap data onto the City Digital Twin ontologies
- The OpenStreetMap GeoJSON folder contains the raw data in GeoJSON format that was extracted from OpenStreetMap 
