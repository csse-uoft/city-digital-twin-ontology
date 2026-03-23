# Fire

This is the ontological representation of Toronto’s fire emergency service, including both fire station service sites and run-area catchment geometries. Fire services are represented as instances of a fire service class (e.g., tor:fire_service{RUN_AREA}), and each service is linked to a catchment area representing the fire run area using service:hasCatchmentArea. Catchment areas are represented as spatial regions with geospatial geometry stored as WKT using geo:asWKT. Fire stations are represented as service sites linked from the fire service via hp:providedFromSite, where each station can have a name (genprop:hasName), an address (org:siteAddress with street components), and a point location (loc:hasLocation) expressed as WKT geometry (geo:asWKT).

To model service performance and capacity, the mapping represents fire service capacity and usage using quantitative rate objects with ISO measurement structure (i72:hasValue, i72:hasNumericalValue, i72:hasUnit). Capacity and capacity-in-use are asserted using res:hasCapacity and res:capacityInUse, and available capacity can be asserted directly using res:hasAvailableCapacity to preserve the classification of the available capacity type (e.g., available firefighters-per-population).

This section summarizes how the [Toronto Fire Services run areas dataset](https://open.toronto.ca/dataset/toronto-fire-services-run-areas/) (catchment geometries), [the fire station locations dataset](https://open.toronto.ca/dataset/fire-station-locations/) (service sites and addresses), and the synthetic firefighter-per-person dataset (service usage and derived available capacity) are mapped into the City Digital Twin ontology.

The following is a list of namespace prefixes<u> used in the mappings and ontology definitions that follow</u>: 

- tor: http://ontology.eil.utoronto.ca/Toronto/Toronto#

- genprop: https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/

- loc: https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/

- geo: http://www.opengis.net/ont/geosparql#

- hp: http://ontology.eil.utoronto.ca/HPCDM/

- service: https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/CityService/

- change: https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Change/

- time: http://www.w3.org/2006/time#

- res: https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Resource/

- i72: http://ontology.eil.utoronto.ca/ISO21972/iso21972#
  

![Figure 1](https://github.com/csse-uoft/city-digital-twin-ontology/blob/e7ddff502e8b82190e12781280852868372c9853/Housing%20Potential%20Python/Housing%20Potential%20Diagrams/Figure%201%20Diagram%20of%20Fire%20Pattern..png)

**Figure 1**: Diagram of Fire Pattern.


| **Data Provided by Fire Services Run Areas Dataset** |                               |                          |                               |                                                                                                                                                                         |
|------------------------------------------------------|-------------------------------|--------------------------|-------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Field Name**                                       | **Subject**                   | **Property**             | **Object**                    | **Notes**                                                                                                                                                               |
| RUN_AREA                                             | tor:fire_service{RUN_AREA}    | rdf:type                 | tor:TorFireEmergencyService   | This corresponds to the fire station id and integrates with the fire station dataset; this station will be the primary responder (but others could respond as required) |
|                                                      | tor:fire_service{RUN_AREA}    | service:hasCatchmentArea | tor:fire_catchment\_{AREA_ID} |                                                                                                                                                                         |
| AREA_ID                                              | tor:fire_catchment\_{AREA_ID} | genprop:has Identifier   | "{AREA_ID}"                   | Note - there are other attributes for the area (not required)                                                                                                           |
| geometry                                             | tor:fire_catchment\_{AREA_ID} | geo:asWKT                | {geometry}                    | Geometry.                                                                                                                                                               |

**Table 1**: Mapping Fire Services Run Areas Data to City Digital Twins


| **Data Provided by Fire Facility Locations Dataset** |                                              |                         |                                              |                                                    |
|------------------------------------------------------|----------------------------------------------|-------------------------|----------------------------------------------|----------------------------------------------------|
| **Field Name**                                       | **Subject**                                  | **Property**            | **Object**                                   | **Notes**                                          |
| STATION                                              | tor:fire_service{STATION}                    | hp:providedFrom Site    | tor:fire_station\_{STATION}                  | Identifier/name for the station                    |
|                                                      | tor:fire_station\_{STATION}                  | genprop:hasName         | Fire Station {STATION}                       |                                                    |
|                                                      | tor:fire_service{STATION}                    | rdf:type                | hp:FireEmergencyService                      |                                                    |
| ADDRESS_POINT_ID                                     | tor:fire_station\_{STATION}                  | org:siteAddress         | tor:fire_station_address\_{ADDRESS_POINT_ID} | N/A                                                |
|                                                      | tor:fire_station_address\_{ADDRESS_POINT_ID} | rdf:type                | contact:Address                              |                                                    |
| ADDRESS_NUMBER                                       | tor:fire_station_address\_{ADDRESS_POINT_ID} | contact:hasStreetNumber | {ADDRESS_NUMBER}                             | Street address of the station                      |
| LINEAR_NAME_FULL                                     | tor:fire_station_address\_{ADDRESS_POINT_ID} | contact:hasStreetName   | {LINEAR_NAME}                                | Note: may need to split name with type             |
| geometry                                             | tor:fire_station\_{STATION}                  | loc:hasLocation         | tor:fire_station_loc\_{ADDRESS_POINT_ID}     | Point location of the station                      |
|                                                      | tor:fire_station_loc\_{ADDRESS_POINT_ID}     | geo:asWKT               | {geometry}                                   | \<- defined via service level numbers (per capita) |
|                                                      | tor:fire_services                            | rdf:type                | org:Organization                             |                                                    |
|                                                      |                                              | cdt:providesService     | tor:emergency_service                        |                                                    |
|                                                      | tor:fire_service{STATION}                    | res:hasCapacity         | tor:fire_service{STATION}Capacity            |                                                    |
|                                                      | tor:fire_service{STATION}Capacity            | rdf:type                | hp:MinFirefighterPerPopulation               |                                                    |
|                                                      | tor:fire_service{STATION}Capacity            | i72:hasValue            | tor:fire_service{STATION}CapacityMeasure     |                                                    |
|                                                      | tor:fire_service{STATION}CapacityMeasure     | i72:hasNumericalValue   | 0.001                                        |                                                    |
|                                                      | tor:fire_service{STATION}CapacityMeasure     | i72:hasUnit             | i72:population_ratio_unit                    |                                                    |

**Table 2**: Mapping Fire Facility Locations Data to City Digital Twins


| **Data Provided by Synthetic firefighter population counts Dataset** |                                                |                          |                                                |                                                                       |
|----------------------------------------------------------------------|------------------------------------------------|--------------------------|------------------------------------------------|-----------------------------------------------------------------------|
| **Field Name**                                                       | **Subject**                                    | **Property**             | **Object**                                     | **Notes**                                                             |
| RUN_AREA                                                             | tor:fire_service{RUN_AREA}                     | res:capacityInUse        | tor:fire_service{RUN_AREA}CapacityUse          | \<- to generate (approximation of staffing count to population ratio) |
|                                                                      | tor:fire_service{RUN_AREA}CapacityUse          | rdf:type                 | hp:FirefighterPerPopulation                    |                                                                       |
|                                                                      | tor:fire_service{RUN_AREA}CapacityUse          | i72:hasValue             | tor:fire_service{RUN_AREA}CapacityUseMeasure   |                                                                       |
| Firefighters per person in run area                                  | tor:fire_service{RUN_AREA}CapacityUseMeasure   | i72:hasNumericalValue    | {Firefighters per person in run area}          |                                                                       |
|                                                                      | tor:fire_service{RUN_AREA}CapacityUseMeasure   | i72:hasUnit              | i72:population_ratio_unit                      |                                                                       |
|                                                                      | tor:fire_service{RUN_AREA}                     | res:hasAvailableCapacity | tor:fire_service{RUN_AREA}AvailCapacity        |                                                                       |
|                                                                      | tor:fire_service{RUN_AREA}AvailCapacity        | rdf:type                 | hp:AvailableFirefightersPerPopulation          |                                                                       |
|                                                                      | tor:fire_service{RUN_AREA}AvailCapacity        | i72:hasValue             | tor:fire_service{RUN_AREA}AvailCapacityMeasure |                                                                       |
|                                                                      | tor:fire_service{RUN_AREA}AvailCapacityMeasure | i72:hasNumericalValue    | 0.001 - {Firefighters per person in run area}  |                                                                       |
|                                                                      | tor:fire_service{RUN_AREA}AvailCapacityMeasure | i72:hasUnit              | i72:population_ratio_unit                      |                                                                       |

**Table 3**: Mapping Synthetic firefighter population counts Data to City Digital Twins


- Capacity information:

  - No count of firefighters per station (catchment area)

  - Toronto-wide: est.84% of 3191 = 2680 full time firefighters

    - This could be captured as a “capacity in use” metric of the actual ratio, however it is not worthwhile encoding this as it is too general to be useful for the use cases

- There is the potential to link each catchment area to a specific fire station (corresponding to a sub-service of tor:emergency_service), however this is not

# Implementation of Fire Data in Mapping TTL

**Script:** [Fire.py](https://github.com/csse-uoft/city-digital-twin-ontology/tree/main/Housing%20Potential%20Python)

**URI strategy**

The script generates deterministic URIs under the tor: namespace so that run areas, stations, and capacity measures can be referenced consistently:

- **Fire service (run area):** tor:fire_service{RUN_AREA}

- **Run area catchment polygon:** tor:fire_catchment\_{AREA_ID}

- **Fire station site:** tor:fire_station\_{STATION}

- **Station address node:** tor:fire_station_address\_{ADDRESS_POINT_ID}

- **Station location node:** tor:fire_station_loc\_{ADDRESS_POINT_ID}

- **Station capacity rate and measure:**

  - tor:fire_service{STATION}Capacity

  - tor:fire_service{STATION}CapacityMeasure

- **Run area capacity-in-use rate and measure:**

  - tor:fire_service{RUN_AREA}CapacityUse

  - tor:fire_service{RUN_AREA}CapacityUseMeasure

- **Run area available capacity rate and measure:**

  - tor:fire_service{RUN_AREA}AvailCapacity

  - tor:fire_service{RUN_AREA}AvailCapacityMeasure

**Inputs**

1.  **Run areas (catchment geometry)**

    - toronto-fire-services-run-areas - 4326.csv

    - Required fields used:

      - RUN_AREA (for service URI construction)

      - AREA_ID (for catchment URI + identifier)

      - geometry (GeoJSON / coordinates converted to WKT)

2.  **Fire station locations (service sites + addresses)**

    - fire-station-locations - 4326.csv

    - Required fields used:

      - STATION (for station URI construction)

      - ADDRESS_POINT_ID (for address/location URIs)

      - ADDRESS_NUMBER (street number)

      - LINEAR_NAME_FULL (street name; code also checks a fallback column name)

      - geometry (GeoJSON / coordinates converted to WKT)

3.  **Synthetic usage data (capacity-in-use)**

    - synthetic firefighter and population counts(in).csv

    - Required fields used:

      - RUN_AREA

      - Firefighters per person in run area

**Outputs**

- **fire.ttl**  
  Contains: run area fire services, catchment polygons (with WKT), fire station sites (names, addresses, point geometries), and station-level capacity assertions.

- **fire_synthetic.ttl**  
  Contains: run-area capacity-in-use assertions and explicit available-capacity assertions derived from the synthetic dataset.

**Step-by-step process**

**Step 1 - Initialize RDF graph and namespaces**  
A graph is created and namespaces are bound (e.g., tor, hp, genprop, geo, service, org, contact, loc, cdt, res, i72).

**Step 2 - Normalize geometries and convert to WKT**  
Helper functions infer geometry types (when missing) and convert stored geometry values into WKT using shapely, so geometries can be asserted via geo:asWKT.

**Step 3 - Map run areas as fire services with catchment polygons**  
For each row in toronto-fire-services-run-areas - 4326.csv:

- Create tor:fire_service{RUN_AREA} and assert it as a fire emergency service class.

- Link the service to a catchment resource tor:fire_catchment\_{AREA_ID} using service:hasCatchmentArea.

- Add an identifier to the catchment (genprop:hasIdentifier).

- Convert the run area polygon geometry to WKT and assert it with geo:asWKT.

**Step 4 - Map fire stations as service sites**  
Before iterating stations, the script also asserts a few “global” triples to connect an organization to the emergency service.  
For each row in fire-station-locations - 4326.csv:

- Create a station site tor:fire_station\_{STATION} and add a name (genprop:hasName).

- Link the station as a site using hp:providedFromSite.

- Create an address node tor:fire_station_address\_{ADDRESS_POINT_ID} and attach street number/name when present.

- Create a location node tor:fire_station_loc\_{ADDRESS_POINT_ID} and assert point WKT geometry using geo:asWKT.

**Step 5 - Assert service capacity**  
For each station, the script asserts a capacity node:

- tor:fire_service{STATION} res:hasCapacity tor:fire_service{STATION}Capacity

- The capacity node is typed as hp:MinFirefighterPerPopulation.

- The measure node stores:

  - i72:hasNumericalValue (constant 0.001)

  - i72:hasUnit i72:population_ratio_unit

**Step 6 - Map synthetic usage and explicitly assert available capacity**  
From synthetic firefighter and population counts(in).csv, for each RUN_AREA:

- Assert res:capacityInUse with a node typed hp:FirefighterPerPopulation and a measure storing the usage value.

- Assert res:hasAvailableCapacity with a node typed hp:AvailableFirefightersPerPopulation.

- Compute available capacity as (0.001 - capacityInUse) and store it as the measure’s numerical value (using the same unit).

**Step 7 - Serialize TTL outputs**

> Serialize the run area + station graph to fire.ttl.

- Serialize the synthetic usage graph to fire_synthetic.ttl.

**Notes / assumptions**

- Geometry values may be stored without an explicit GeoJSON "type" field; the script attempts to infer the geometry type from coordinates before conversion to WKT.

- The station capacity is currently asserted on tor:fire_service{STATION}, while capacity-in-use and available capacity are asserted on tor:fire_service{RUN_AREA}. If you need available capacity to strictly represent (hasCapacity − capacityInUse) on the *same* service instance, these assertions should be aligned to the same service URI (e.g., all at the run-area service).

- The value 0.001 is a configured constant in the script; it should be replaced if/when validated capacity definitions are available.
