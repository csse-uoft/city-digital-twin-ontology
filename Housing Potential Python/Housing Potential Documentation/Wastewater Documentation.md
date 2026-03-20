Wastewater Documentation

Relevant Python Scripts:

- [SewerPressurizedMain.py](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/SewerPressurizedMain.py):
  generates the RDF data related to sewer pressurized mains.

  - Dataset links

    - <https://open.toronto.ca/dataset/sewer-pressurized-mains/>

- [SewerPressurizedMainCapacity.py](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/SewerPressurizedMainCapacity.py):
  generates the RDF data for the sewer pressurized mains capacities
  using synthetic data.

  - Dataset links

    - Sewer Pressurized Main_Capacity.csv

- [SewerGravityMain.py](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/SewerGravityMain.py):
  generates the RDF data related to sewer gravity mains.

  - Dataset links

    - <https://open.toronto.ca/dataset/sewer-gravity-mains/>

- [SewerGravityMainCapacity.py](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/SewerGravityMainCapacity.py):
  generates the RDF data for the sewer gravity mains capacities using
  synthetic data.

  - Dataset links

    - Sewer Pressurized Gravity_Capacity.csv

This is the ontological representation of Toronto’s Wastewater data.
Sewer mains provide wastewater services as represented as instances of
the tor:TorWastewaterService class while synthetic data is used as the
capacity values.

This section summarizes how the wastewater related datasets are mapped
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

<img src="/media/image.png" style="width:6.5in;height:4.71875in" />

<img src="/media/image2.png" style="width:6.5in;height:4.71875in" />

| **Data Provided By Pressurized Main Dataset (RDF generation done using SewerPressurizedMain.py)** |  |  |  |  |
|:---|:---|:---|:---|:---|
| **Field Name** | **Subject** | **Property** | **Object** | **Notes** |
| \_id | tor:wastewaterservicepressurizedmain{\_id} | rdf:type | tor:TorWastewaterService | broken down into per-main service to capture flow rates |
|  | tor:wastewaterservicepressurizedmain{\_id} | hp:providedFromSite | tor:wastewaterservice_pressurizedmain{\_id}Site |  |
| Sewer Pressurized Asset Identification | tor:wastewaterservice_pressurizedmain{\_id}Site | genprop:hasIdentifier | "{Sewer Pressurized Asset Identification}" |  |
|  | tor:wastewaterservice_pressurizedmain{\_id}Site | loc:hasLocation | tor:wastewaterservice_pressurizedmain_loc{\_id} |  |
| geometry | tor:wastewaterservice_pressurizedmain_loc{\_id} | geo:asWKT | "{geometry}" |  |

| **Data Provided By Pressurized Main Capacity Dataset (RDF generation done using SewerPressurizedMainCapacity.py)** |  |  |  |
|:---|:---|:---|:---|
| **Field Name** | **Subject** | **Property** | **Object** |
| \_id | tor:wastewaterservicepressurizedmain{\_id} | res:hasCapacity | tor:wastewaterservicepressurizedmain{\_id}Capacity |
|  | tor:wastewaterservicepressurizedmain{\_id}Capacity | rdf:type | hp:MaxWaterProcessingRate |
|  | tor:wastewaterservicepressurizedmain{\_id}Capacity | i72:hasValue | tor:wastewaterservicepressurizedmain{\_id}CapacityMeasure |
| Synthetic Capacity (annual flow m3) | tor:wastewaterservicepressurizedmain{\_id}CapacityMeasure | i72:hasNumericalValue | "{Synthetic Capacity (annual flow m3)}" |
|  | tor:wastewaterservicepressurizedmain{\_id}CapacityMeasure | i72:hasUnit | hp:cubic_metre_per_year |
|  | tor:wastewaterservicepressurizedmain{\_id} | res:capacityInUse | tor:wastewaterservicepressurizedmain{\_id}CapacityUse |
|  | tor:wastewaterservicepressurizedmain{\_id}CapacityUse | rdf:type | hp:WaterProcessingRate |
|  | tor:wastewaterservicepressurizedmain{\_id}CapacityUse | i72:hasValue | tor:wastewaterservicepressurizedmain{\_id}CapacityUseMeasure |
| Randomized Annual Use (m3) | tor:wastewaterservicepressurizedmain{\_id}CapacityUseMeasure | i72:hasNumericalValue | "{Randomized Annual Use (m3)}" |
|  | tor:wastewaterservicepressurizedmain{\_id}CapacityUseMeasure | i72:hasUnit | hp:cubic_metre_per_year |
|  | tor:wastewaterservicepressurizedmain{\_id} | res:hasAvailableCapacity | tor:wastewaterservicepressurizedmain{\_id}CapacityAvail |
|  | tor:wastewaterservicepressurizedmain{\_id}Capacity | rdf:type | hp:AvailableWaterProcessingRate |
|  | tor:wastewaterservicepressurizedmain{\_id}CapacityAvail | i72:hasValue | tor:wastewaterservicepressurizedmain{\_id}CapacityAvailMeasure |
| Available Annual Flow | tor:wastewaterservicepressurizedmain{\_id}CapacityAvailMeasure | i72:hasNumericalValue | "{Available Annual Flow}" |
|  | tor:wastewaterservicepressurizedmain{\_id}CapacityAvailMeasure | i72:hasUnit | hp:cubic_metre_per_year |

| **Data Provided By Gravity Main Dataset (RDF generation done using SewerGravityMain.py)** |  |  |  |
|:---|:---|:---|:---|
| **Field Name** | **Subject** | **Property** | **Object** |
| \_id | tor:wastewaterservicegravitymain{\_id} | rdf:type | tor:TorWastewaterService |
|  | tor:wastewaterservicegravitymain{\_id} | hp:providedFromSite | tor:wastewaterservice_gravitymain{\_id}Site |
| Sewer Gravity Asset Identification | tor:wastewaterservice_gravitymain{\_id}Site | genprop:hasIdentifier | "{Sewer Gravity Asset Identification}" |
|  | tor:wastewaterservice_gravitymain{\_id}Site | loc:hasLocation | tor:wastewaterservice_gravitymain_loc{\_id} |
| geometry | tor:wastewaterservice_gravitymain_loc{\_id} | geo:asWKT | "{geometry}" |

| **Data Provided By Gravity Main Capacity Dataset (RDF generation done using SewerGravityMainCapacity.py)** |  |  |  |
|:---|:---|:---|:---|
| **Field Name** | **Subject** | **Property** | **Object** |
| \_id | tor:wastewaterservicegravitymain{\_id} | res:hasCapacity | tor:wastewaterservicegravitymain{\_id}Capacity |
|  | tor:wastewaterservicegravitymain{\_id}Capacity | rdf:type | hp:MaxWaterProcessingRate |
|  | tor:wastewaterservicegravitymain{\_id}Capacity | i72:hasValue | tor:wastewaterservicegravitymain{\_id}CapacityMeasure |
| Est Flow Capacity (m3/year) | tor:wastewaterservicegravitymain{\_id}CapacityMeasure | i72:hasNumericalValue | "{Est Flow Capacity (m3/year)}" |
|  | tor:wastewaterservicegravitymain{\_id}CapacityMeasure | i72:hasUnit | hp:cubic_metre_per_year |
|  | tor:wastewaterservicegravitymain{\_id} | res:capacityInUse | tor:wastewaterservicegravitymain{\_id}CapacityUse |
|  | tor:wastewaterservicegravitymain{\_id}CapacityUse | rdf:type | hp:WaterProcessingRate |
|  | tor:wastewaterservicegravitymain{\_id}CapacityUse | i72:hasValue | tor:wastewaterservicegravitymain{\_id}CapacityUseMeasure |
| Synthetic (Randomized) utilization | tor:wastewaterservicegravitymain{\_id}CapacityUseMeasure | i72:hasNumericalValue | "{Synthetic (Randomized) utilization}" |
|  | tor:wastewaterservicegravitymain{\_id}CapacityUseMeasure | i72:hasUnit | hp:cubic_metre_per_year |
|  | tor:wastewaterservicegravitymain{\_id} | res:hasAvailableCapacity | tor:wastewaterservicegravitymain{\_id}CapacityAvail |
|  | tor:wastewaterservicegravitymain{\_id}CapacityAvail | rdf:type | hp:AvailableWaterProcessingRate |
|  | tor:wastewaterservicegravitymain{\_id}CapacityAvail | i72:hasValue | tor:wastewaterservicegravitymain{\_id}CapacityAvailMeasure |
| Synthetic Available Capacity | tor:wastewaterservicegravitymain{\_id}CapacityAvailMeasure | i72:hasNumericalValue | "{Synthetic Available Capacity}" |
|  | tor:wastewaterservicegravitymain{\_id}CapacityAvailMeasure | i72:hasUnit | hp:cubic_metre_per_year |

Implementation of Wastewater Related Data in Mapping TTL

**Scripts:** SewerPressurizedMain.py

**URI strategy**

- **Pressurized Main:**

  - tor:wastewaterservicepressurizedmain{\_id}

- **Pressurized Main Location**:

  - tor:wastewaterservice_pressurizedmain_loc{\_id}

- **Pressurized Main Site:**

  - tor:wastewaterservice_pressurizedmain{\_id}Site

**Scripts:** SewerPressurizedMainCapacity.py

**URI strategy**

- **Pressurized Main Capacity:**

  - tor:wastewaterservicepressurizedmain{\_id}Capacity

- **Pressurized Main Capacity Use**:

  - tor:wastewaterservicepressurizedmain{\_id}CapacityUse

- **Pressurized Main Capacity Available:**

  - tor:wastewaterservicepressurizedmain{\_id}CapacityAvail

**Scripts:** SewerGravityMain.py

- **Gravity Main:**

  - tor:wastewaterservicegravitymain{\_id}

- **Gravity Main Location:**

  - tor:wastewaterservice_gravitymain_loc{\_id}

- **Gravity Main Site:**

  - tor:wastewaterservice_gravitymain{\_id}Site

**Scripts:** SewerGravityMainCapacity.py

**URI strategy**

- **Gravity Main Capacity:**

  - tor:wastewaterservicegravitymain{\_id}Capacity

- **Gravity Main Capacity Use**:

  - tor:wastewaterservicegravitymain{\_id}CapacityUse

- **Gravity Main Capacity Available:**

  - tor:wastewaterservicegravitymain{\_id}CapacityAvail

**Inputs**

1.  **Sewer Pressurized Main Data (SewerPressurizedMain.py )**

    - Dataset links

      - <https://open.toronto.ca/dataset/sewer-pressurized-mains/>

    - Data from the Toronto Open Data Portal can be downloaded as a
      geoJSON file and is directly accessible using the Python script.

2.  **Sewer Pressurized Main Capacity Data
    (SewerPressurizedMainCapacity.py )**

    - Dataset links

      - Sewer Pressurized Main_Capacity.csv

3.  **Sewer Gravity Main Data (SewerGravityMain.py )**

    - Dataset links

      - <https://open.toronto.ca/dataset/sewer-gravity-mains/>

    - Data from the Toronto Open Data Portal can be downloaded as a
      geoJSON file and is directly accessible using the Python script.

4.  **Sewer Gravity Main Capacity Data (SewerGravityMainCapacity.py )**

    - Dataset links

      - Sewer Pressurized Gravity_Capacity.csv

**Outputs**

- SewerPressurizedMain.ttl (SewerPressurizedMain.py)  
  Contains: Sewer pressurized main information and their locations

- SewerPressurizedMainCapacity.ttl (SewerPressurizedMainCapacity.py)  
  Contains: Synthetic information about sewer pressurized main
  capacities

- SewerGravityMain.ttl (SewerGravityMain.py)  
  Contains: Sewer gravity main information and their locations

- SewerGravityMainCapacity.ttl (SewerGravityMainCapacity.py)  
  Contains: Synthetic information about sewer gravity main capacities

**Step-by-step process for SewerPressurizedMain.py**

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
The graph is written to SewerPressurizedMain.ttl.

**Step-by-step process for SewerPressurizedMainCapacity.py**

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
The graphs are written to SewerPressurizedMainCapacity.ttl.

**Step-by-step process for SewerGravityMain.py**

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
The graph is written to SewerGravityMain.ttl.

**Step-by-step process for SewerGravityMainCapacity.py**

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
The graphs are written to SewerGravityMainCapacity.ttl.
