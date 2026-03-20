Long Term Care Documentation

Relevant Python Scripts:

- [LongTermCare.py:](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/LongTermCare.py)
  generates the RDF data related to long term care locations in Toronto
  and their capacities.

  - Dataset links

    - <https://open.toronto.ca/dataset/long-term-care-locations-city-operated/>

    - long_term_care_locations_wgs84_withfakeoccupancy.xlsx (synthetic
      capacity data)

This is the ontological representation of Toronto’s long term care
location data from the Toronto Open Data Portal. Services provided by
long term care locations are represented as instances of the
tor:TorLongTermCareService class while the capacity data is derived from
a synthetic dataset.

This section summarizes how the long term care related datasets are
mapped into the City Digital Twin ontology.

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

| **Data Provided By the Long Term Care Dataset (RDF generation done using LongTermCare.py)** |  |  |  |  |
|:---|:---|:---|:---|:---|
| **Field Name** | **Subject** | **Property** | **Object** | **Notes** |
| FID | tor:seniorcare_service{FID} | rdf:type | tor:TorLongTermCareService |  |
|  | tor:seniorcare_service{FID} | hp:providedFromSite | tor:seniorcare_service_site{FID} |  |
| ID | tor:seniorcare_service_site{FID} | genprop:hasIdentifier | "{ID}" |  |
| NAME |  | genprop:hasName | "{NAME}" |  |
| BEDS | tor:seniorcare_service{FID} | res:hasCapacity | tor:seniorcare_service{FID}Capacity |  |
|  | tor:seniorcare_service{FID}Capacity | rdf:type | hp:NumberOfLongTermCareBeds |  |
|  | tor:seniorcare_service{FID}Capacity | i72:hasValue | tor:seniorcare_service{FID}CapacityMeasure |  |
|  | tor:seniorcare_service{FID}CapacityMeasure | i72:hasNumericalValue | "{BEDS}" |  |
|  | tor:seniorcare_service{FID}CapacityMeasure | i72:hasUnit | i72:population_cardinality_unit |  |
| geometry | tor:seniorcare_service_site{FID} | loc:hasLocation | tor:seniorcare_service_site_location{FID} |  |
|  | tor:seniorcare_service_site_location{FID} | geo:asWKT | "{geometry}" |  |
| none (synthetic) | tor:seniorcare_service{FID} | res:capacityInUse | tor:seniorcare_service{FID}CapacityUse |  |
|  | tor:seniorcare_service{FID}CapacityUse | rdf:type | hp:NumberOfLongTermCareResidents |  |
|  | tor:seniorcare_service{FID}CapacityUse | i72:hasValue | tor:seniorcare_service{FID}CapacityUseMeasure |  |
| Fake occupancy | tor:seniorcare_service{FID}CapacityUseMeasure | i72:hasNumericalValue | {Fake occupancy} | total number of beds, scaled by 95-100% |
|  | tor:seniorcare_service{FID}CapacityUseMeasure | i72:hasUnit | i72:population_cardinality_unit |  |
|  | tor:seniorcare_service{FID} | res:hasAvailableCapacity | tor:seniorcare_service{FID}CapacityAvail |  |
|  | tor:seniorcare_service{FID}CapacityAvail | rdf:type | hp:NumberOfLongTermCareBedsAvailable |  |
|  | tor:seniorcare_service{FID}CapacityAvail | i72:hasValue | tor:seniorcare_service{FID}CapacityAvailMeasure |  |
|  | tor:seniorcare_service{FID}CapacityAvailMeasure | i72:hasNumericalValue | {capacity - capacity use} |  |
|  | tor:seniorcare_service{FID}CapacityAvailMeasure | i72:hasUnit | i72:population_cardinality_unit |  |

Implementation of Long Term Care Related Data in Mapping TTL

**Scripts:** LongTermCare.py

**URI strategy**

- **Long Term Care Site:**

  - tor:seniorcare_service_site{FID}

- **Long Term Care Site Location:**

  - tor:seniorcare_service_site_location{FID}

- **Long Term Care Service:**

  - tor:seniorcare_service{FID}

- **Long Term Care Capacity:**

  - tor:seniorcare_service{FID}Capacity

- **Long Term Care Capacity Use:**

  - tor:seniorcare_service{FID}CapacityUse

- **Long Term Care Capacity Available:**

  - tor:seniorcare_service{FID}CapacityAvail

**Inputs**

1.  **Long Term Care Data (LongTermCare.py)**

    - Dataset links

      - <https://open.toronto.ca/dataset/long-term-care-locations-city-operated/>

    - Data can be downloaded and used as a .shp file

2.  **Long Term Care Synthetic Capacity Data (LongTermCare.py)**

    - Dataset links

      - long_term_care_locations_wgs84_withfakeoccupancy.xlsx (synthetic
        capacity data)

**Outputs**

- LongTermCare.ttl (LongTermCare.py)  
  Contains: Long term care data for Toronto and their locations.

- LongTermCareCapacity.ttl (LongTermCare.py)  
  Contains: Synthetic information about long term care capacities

**Step-by-step process for LongTermCare.py**

**Step 1 - Initialize RDF graphs and namespaces**  
Two RDF graphs are created:

- g contains all triples for the LongTermCare.ttl output file

- g2 contains all triples for the LongTermCareCapacity.ttl output file

**Step 2 – Import data from the shapefile using the geopandas Python
package**  
The data from the long term care dataset is contained in the “df”
dataframe.

**Step 3 – Import data from the xlsx file using the pandas Python
package**  
The data from the long term care dataset is contained in the “df2”
dataframe.

**Step 4 – Merge both dataframes**  
Both dataframes from step 2 and 3 are merged to create a dataframe “df”
containing data from both datasets.

**Step 5 - RDF triples are created using each feature in the data**  
The data in stored in the df dataframe is iterated row by row and RDF
triples are generated according to the mapping specifications outlined
in the tables found earlier in this document. Values for the triples are
extracted from the corresponding column in the data.

**Step 6 - Serialize TTL**  
The graph g is written to LongTermCare.ttl and g2 is written to
LongTermCareCapacity.ttl.
