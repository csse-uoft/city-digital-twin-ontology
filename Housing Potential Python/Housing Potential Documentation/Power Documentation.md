Power Documentation

Relevant Python Scripts:

- [FeederCapacity.py](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/FeederCapacity.py):
  generates the RDF data related to Toronto Hydro power feeders and
  their capacities.

  - Dataset links

    - <https://services8.arcgis.com/SnGTjuDV2RIxBTxw/ArcGIS/rest/services/PRD_FeederLayers/FeatureServer>

    - feeder_total_fake.csv (synthetic total capacities)

This is the ontological representation of Toronto’s power feeders data
from Toronto Hydro. Hydro feeder services are represented as instances
of the tor:TorElectricService class while synthetic data is used for the
total capacity values.

This section summarizes how the power related datasets are mapped into
the City Digital Twin ontology.

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

<img src="/media/image.png" style="width:6.5in;height:4.64583in" />

| **Data Provided By Toronto Hydro Feeder Dataset (RDF generation done using FeederCapacity.py)** |  |  |  |  |
|:---|:---|:---|:---|:---|
| **Field Name** | **Subject** | **Property** | **Object** | **Notes** |
| Network_id | tor:hydro_feeder_service{Network_id} | rdf:type | tor:TorElectricService | maps hydro feeder to a power (sub)service |
|  | tor:hydro_feeder_service{Network_id} | genprop:hasIdentifier | "{Network_id}" |  |
|  | tor:hydro_feeder_service{Network_id} | hp:providedFromSite | tor:hydro_feeder_service_site{Network_id} |  |
|  | tor:hydro_feeder_service_site{Network_id} | rdf:type | cdt:Site |  |
|  | tor:hydro_feeder_service_site{Network_id} | genprop:hasName | "Feeder Station {Network_id}" |  |
|  | tor:hydro_feeder_service{Network_id} | service:hasAvailableCapacity | tor:hydro_feeder_service{Network_id}CapacityAvail |  |
|  | tor:hydro_feeder_service{Network_id}CapacityAvail | rdf:type | hp:AvailableElectricalCapacity |  |
|  | tor:hydro_feeder_service{Network_id}CapacityAvail | i72:hasValue | tor:hydro_feeder_service{Network_id}CapacityAvailMeasure |  |
| Feeder_Capacity | tor:hydro_feeder_service{Network_id}CapacityAvailMeasure | i72:hasNumericalValue | {Feeder_Capacity} | \<-parse value to take maximum, as an estimate |
|  | tor:hydro_feeder_service{Network_id}CapacityAvailMeasure | i72:hasUnit | hp:kilovolt_ampere |  |
| SHAPE | tor:hydro_feeder_service{Network_id} | service:hasCatchmentArea | tor:hydro_feeder_service{Network_id}Area{OBJECTID} |  |
|  | tor:hydro_feeder_service{Network_id}Area{OBJECTID} | geo:asWKT | {SHAPE} |  |

| **Data Provided By Synthetic Total Feeder Capacity Dataset (RDF generation done using FeederCapacity.py)** |  |  |  |
|:---|:---|:---|:---|
| **Field Name** | **Subject** | **Property** | **Object** |
| Network_id | tor:hydro_feeder_service{Network_id} | service:hasCapacity | tor:hydro_feeder_service{Network_id}Capacity |
|  | tor:hydro_feeder_service{Network_id}Capacity | rdf:type | hp:ElectricalLoadCapacity |
| Fake Max Avail Capacity (kVA) | tor:hydro_feeder_service{Network_id}Capacity | i72:hasValue | tor:hydro_feeder_service{Network_id}CapacityMeasure |
|  | tor:hydro_feeder_service{Network_id}CapacityMeasure | i72:hasNumericalValue | {Fake Max Avail Capacity (kVA)} |
|  | tor:hydro_feeder_service{Network_id}CapacityMeasure | i72:hasUnit | hp:kilovolt_ampere |

Implementation of Power Related Data in Mapping TTL

**Scripts:** FeederCapacity.py

**URI strategy**

- **Feeder Service:**

  - tor:hydro_feeder_service{Network_id}

- **Feeder Catchment Area**:

  - tor:hydro_feeder_service{Network_id}Area{OBJECTID}

- **Feeder Capacity:**

  - tor:hydro_feeder_service{Network_id}Capacity

- **Feeder Capacity Available:**

  - tor:hydro_feeder_service{Network_id}CapacityAvail

**Inputs**

1.  **Toronto Hydro Feeder Data (FeederCapacity.py)**

    - Dataset links

      - <https://services8.arcgis.com/SnGTjuDV2RIxBTxw/ArcGIS/rest/services/PRD_FeederLayers/FeatureServer>

    - Data is downloaded as a shapefile (.shp) from the Toronto Open
      Data Portal. This can be converted to a geoJSON file for easier
      parsing in Python

2.  **Feeder Capacity Data (FeederCapacity.py )**

    - Dataset links

      - feeder_total_fake.csv (synthetic total capacities)

**Outputs**

- FeederCapacity.ttl (FeederCapacity.py)  
  Contains: Toronto Hydro feeder information, their available
  capacities, and the locations of their catchment areas.

- FeederTotal.ttl (FeederCapacity.py)  
  Contains: Synthetic information about feeder total capacities

**Step-by-step process for Feeder.py**

**Step 1 - Initialize RDF graphs and namespaces**  
Two RDF graphs are created:

- g contains Toronto Hydro feeder information, their available
  capacities, and the locations of their catchment areas.

- g2 contains synthetic information about feeder total capacities

**Step 2 – Import CSV dataset using the pandas Python package**  
Initially, the data from the Toronto Hydro dataset is contained in the
“df” dataframe and the synthetic data is contained in the “df2”
dataframe. The two dataframes are then merged as one dataframe called
“df” which will be used for parsing.

**Step 3 - RDF triples are created using each row in the dataframe**  
The data is iterated row by row and RDF triples are generated according
to the mapping specifications outlined in the tables found earlier in
this document. Values for the triples are extracted from the
corresponding column in the data.

**Note:** The value of the available capacity uses the maximum value
from the Toronto Hydro dataset, as the values are shown as ranges
instead of singular values in the dataset.

**Note 2:** The geospatial data in the Toronto Hydro dataset uses the
EPSG:3857 standard for its coordinates. These coordinates are converted
to EPSG:4326 (WGS84) before being written as an RDF triple in order to
maintain consistency with the other geospatial data in the City Digital
Twin.

**Step 4 - Serialize TTL**  
The graph g is written to FeederCapacity.ttl and g2 is written to
FeederTotal.ttl.
