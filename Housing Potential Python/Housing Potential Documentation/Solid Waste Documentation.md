Solid Waste Documentation

Relevant Python Scripts:

- [SolidWaste.py](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/SolidWaste.py):
  generates the RDF data related to solid waste collection.

  - Dataset links

    - <https://open.toronto.ca/dataset/solid-waste-daytime-curbside-collection-areas/>

  - Data is downloaded as a shapefile (.shp) from the Toronto Open Data
    Portal. This can be converted to a geoJSON file for easier parsing
    in Python

- [SolidWasteCapacity.py](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/SolidWasteCapacity.py):
  generates the RDF data for the solid waste collection capacities using
  synthetic data.

  - Dataset links

    - swms_synthetic_capacities.csv

This is the ontological representation of Toronto’s Solid Waste
Collection data. Solid waste collection services are represented as
instances of the tor:TorSolidWasteService class while synthetic data is
used for the capacity values.

This section summarizes how the solid waste related datasets are mapped
into the City Digital Twin ontology.

The following is a list of namespace prefixes<u> used in the mappings
and ontology definitions that follow</u>: 

- tor: http://ontology.eil.utoronto.ca/Toronto/Toronto#

- genprop:
  https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/

- loc:
  https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/

- geo: http://www.opengis.net/ont/geosparql#

- hp: http://ontology.eil.utoronto.ca/HPCDM/

- service:
  https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/CityService/

- org:
  https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Organization/

- contact:
  <https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Contact/>

- res:
  <https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Resource/>

- cdt: http://ontology.eil.utoronto.ca/CDT#

- i72: http://ontology.eil.utoronto.ca/ISO21972/iso21972#

<img src="/media/image.png" style="width:6.5in;height:4.5625in" />

| **Data Provided By Solid Waste Dataset (RDF generation done using SolidWaste.py)** |  |  |  |
|:---|:---|:---|:---|
| **Field Name** | **Subject** | **Property** | **Object** |
| FID | tor:solidwaste_service{FID} | rdf:type | tor:TorSolidWasteService |
| AREA_ID | tor:solidwaste_service{FID} | service:hasCatchmentArea | tor:solidwaste_servicearea\_{AREA_ID} |
|  | tor:solidwaste_servicearea\_{AREA_ID} | genprop:hasIdentifier | "AREA_ID" |
| AREA_LONG | tor:solidwaste_servicearea\_{AREA_ID} | genprop:hasIdentifier | "AREA_LONG" |
| Area | tor:solidwaste_servicearea\_{AREA_ID} | genprop:hasName | "Area" |
| geometry | tor:solidwaste_servicearea\_{AREA_ID} | geo:asWKT | "geometry" |

| **Data Provided By Synthetic Solid Waste Capacity Dataset (RDF generation done using SolidWasteCapacity.py)** |  |  |  |
|:---|:---|:---|:---|
| **Field Name** | **Subject** | **Property** | **Object** |
| FID | tor:solidwaste_service{FID} | res:hasCapacity | tor:solidwaste_service{FID}Capacity |
|  | tor:solidwaste_service{FID}Capacity | rdf:type | hp:MaxWasteProcessingRate |
|  | tor:solidwaste_service{FID}Capacity | i72:hasValue | tor:solidwaste_service{FID}CapacityMeasure |
| Randomized total capacity per area | tor:solidwaste_service{FID}CapacityMeasure | i72:hasNumericalValue | "{Randomized total capacity per area}" |
|  | tor:solidwaste_service{FID}CapacityMeasure | i72:hasUnit | hp:tonnes_per_year |
|  | tor:solidwaste_service{FID} | res:capacityInUse | tor:solidwaste_service{FID}CapacityUse |
|  | tor:solidwaste_service{FID}CapacityUse | rdf:type | hp:WasteProcessingRate |
|  | tor:solidwaste_service{FID}CapacityUse | i72:hasValue | tor:solidwaste_service{FID}CapacityUseMeasure |
| Estimated Capacity in use(tonnes / year) | tor:solidwaste_service{FID}CapacityUseMeasure | i72:hasNumericalValue | "{Estimated Capacity in use(tonnes / year)}" |
|  | tor:solidwaste_service{FID}CapacityUseMeasure | i72:hasUnit | hp:tonnes_per_year |
|  | tor:solidwaste_service{FID} | res:hasAvailableCapacity | tor:solidwaste_service{FID}CapacityAvail |
|  | tor:solidwaste_service{FID}CapacityAvail | rdf:type | hp:AvailableWasteProcessingRate |
|  | tor:solidwaste_service{FID}CapacityAvail | i72:hasValue | tor:solidwaste_service{FID}CapacityAvailMeasure |
| Available capacity | tor:solidwaste_service{FID}CapacityAvailMeasure | i72:hasNumericalValue | "{Available capacity}" |
|  | tor:solidwaste_service{FID}CapacityAvailMeasure | i72:hasUnit | hp:tonnes_per_year |

Implementation of Solid Waste Related Data in Mapping TTL

**Scripts:** SolidWaste.py

**URI strategy**

- **Solid Waste Collection Service:**

  - tor:solidwaste_service{FID}

- **Solid Waste Catchment Area**:

  - tor:solidwaste_servicearea\_{AREA_ID}

**Scripts:** SolidWasteCapacity.py

**URI strategy**

- **Solid Waste Capacity:**

  - tor:solidwaste_service{FID}Capacity

- **Solid Waste Capacity Use**:

  - tor:solidwaste_service{FID}CapacityUse

- **Solid Waste Capacity Available:**

  - tor:solidwaste_service{FID}CapacityAvail

**Inputs**

1.  **Solid Waste Collection Data (SolidWaste.py)**

    - Dataset links

      - <https://open.toronto.ca/dataset/solid-waste-daytime-curbside-collection-areas/>

    - Data is downloaded as a shapefile (.shp) from the Toronto Open
      Data Portal. This can be converted to a geoJSON file for easier
      parsing in Python

2.  **Solid Waste Capacity Data (SolidWasteCapacity.py )**

    - Dataset links

      - swms_synthetic_capacities.csv

**Outputs**

- SolidWaste.ttl (SolidWaste.py)  
  Contains: Solid waste information and the locations of their catchment
  areas.

- SolidWasteCapacity.ttl (SolidWasteCapacity.py)  
  Contains: Synthetic information about solid waste capacities

**Step-by-step process for SolidWaste.py**

**Step 1 - Initialize RDF graphs and namespaces**  
One RDF graph is created:

- g contains all triples found in the output ttl file

**Step 2 – Import geoJSON dataset using json Python package**  
Data from the geoJSON dataset is contained in the “data” variable.

**Step 3 - RDF triples are created using each feature in the geoJSON
data**  
The data is iterated feature by feature and RDF triples are generated
according to the mapping specifications outlined in the tables found
earlier in this document. Values for the triples are extracted from the
corresponding property in the data.

**Step 4 - Serialize TTL**  
The graph is written to SolidWaste.ttl.

**Step-by-step process for SolidWasteCapacity.py**

**Step 1 - Initialize RDF graphs and namespaces**  
One RDF graph is created:

- g contains all triples found in the output ttl file

**Step 2 – Import CSV dataset using the pandas Python package**  
The imported csv data is stored in the “df” dataframe.

**Step 3 – RDF triples are created using each row of data in the
imported CSV data**  
The data is iterated row by row and RDF triples are generated according
to the mapping specifications outlined in the tables found earlier in
this document. Values for the triples are extracted from the
corresponding column in the data.

**Step 4 - Serialize TTL**  
The graphs are written to SolidWasteCapacity.ttl.
