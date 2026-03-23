Water

This is the ontological representation of Toronto’s water distribution
service, including both the physical distribution infrastructure and
ward-level service metrics (consumption and capacity). The overall
service is represented as an instance of the **WaterService** class
(tor:waterservice). Water distribution pipes are represented as
site-like entities linked from the service via **providedFromSite**,
where each pipe can have a unique identifier (via **hasIdentifier**) and
a geospatial location (via **hasLocation**) expressed as WKT geometry
(via **asWKT**).

To model how water service performance varies across the city, the water
service is decomposed into ward-level sub-services (for a given year),
linked using **hasSubService**. Each ward sub-service is associated with
a ward catchment area using **hasCatchmentArea**, where the catchment’s
geometry is defined using the ward’s existing location in the knowledge
graph. Consumption, total capacity, and available capacity are
represented as quantitative rate objects (as instances of
**WaterDistributionRate**) with values captured through ISO measurement
structure (**hasValue**, **hasNumericalValue**, **hasUnit**) in m³/year.

This section summarizes how the Watermains dataset (geometry and
assets), water billing by ward (annual consumption), synthetic capacity
by ward (total and available capacity), and ward locations (catchment
geometry) are mapped into the City Digital Twin ontology.

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


![Figure 1](https://github.com/csse-uoft/city-digital-twin-ontology/blob/8805fc77c472c008d82c617f019b663efd477a6e/Housing%20Potential%20Python/Housing%20Potential%20Diagrams/Figure%201%20Diagram%20of%20bylaw%20reference%20mapping%20result.png)

Figure 1: Diagram of Water Pattern.

| **Data Provided by Watermains Dataset** |                                                |                       |                                                |                                                       |
|-----------------------------------------|------------------------------------------------|-----------------------|------------------------------------------------|-------------------------------------------------------|
| **Field Name**                          | **Subject**                                    | **Property**          | **Object**                                     | **Notes**                                             |
| \_id                                    | tor:waterservice                               | rdf:type              | tor:TorWaterService                            | Unique row identifier for Open Data database          |
|                                         | tor:waterservice                               | hp:providedFromSite   | tor:waterservice\_ distributionpipes{\_id}     |                                                       |
| Watermain Asset Identification          | tor:waterservice\_ distributionpipes{\_id}     | genprop:hasIdentifier | "{Watermain Asset Identification}"             | Identification number assigned by the City of Toronto |
|                                         | tor:waterservice\_ distributionpipes{\_id}     | loc:hasLocation       | tor:waterservice\_ distributionpipes_loc{\_id} |                                                       |
| geometry                                | tor:waterservice\_ distributionpipes_loc{\_id} | geo:asWKT             | "{geo}"                                        | Geometry.                                             |

: Mapping Watermains Data to City Digital Twins

| **Data Provided by Ward Locations Dataset** |                                                      |                 |            |                                                                                                                                        |
|---------------------------------------------|------------------------------------------------------|-----------------|------------|----------------------------------------------------------------------------------------------------------------------------------------|
| **Field Name**                              | **Subject**                                          | **Property**    | **Object** | **Notes**                                                                                                                              |
| loc                                         | tor:water_distributionservice \_ward_catchment{Ward} | loc:hasLocation | {loc}      | parse the tor:{ward} value for {s} to generate the ward number needed for {Ward} in tor:water_distributionservice_ward_catchment{Ward} |

: Mapping Water Capacity Data to City Digital Twins

Table 2: Mapping Ward Locations Data to City Digital Twins

Toronto [Watermain
locations](https://data.urbandatacentre.ca/catalogue/watermains)
interpreted as service sites (sites of the distribution service). While
no catchment areas are specified, nor is service defined for individual
water connections, it is possible to use the service site locations to
approximate service accessibility (based on some reasonable proximity,
e.g., 30 m)

[Watermains](https://open.toronto.ca/dataset/watermains/), specifically,
"distribution" dataset; note that there is other data that could be
useful for extensions to this work; emailed OpenData contact for
interpretation of "Watermain Type" field in case this could/should be
used for filtering

<table>
<colgroup>
<col style="width: 14%" />
<col style="width: 28%" />
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 17%" />
</colgroup>
<thead>
<tr class="header">
<th colspan="5"><strong>Data Provided by Water Billing
Dataset</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><strong>Field Name</strong> </td>
<td><strong>Subject</strong> </td>
<td><strong>Property</strong> </td>
<td><strong>Object</strong> </td>
<td><strong>Notes</strong> </td>
</tr>
<tr class="even">
<td rowspan="3">Ward</td>
<td>tor:waterservice</td>
<td>hp:hasSubService</td>
<td>tor:water_distribution service_ward{Ward}_{Year}</td>
<td rowspan="3"><p>2-digit electoral ward number</p>
<p>Services are activites, so a "sub-service" is simply a subactivity of
the service</p></td>
</tr>
<tr class="odd">
<td>tor:water_distribution service_ward{Ward}_{Year}</td>
<td>rdf:type</td>
<td>tor:TorWaterService</td>
</tr>
<tr class="even">
<td>tor:water_distribution service_ward{Ward}_{Year}</td>
<td>service:hasCatchmentArea</td>
<td>tor:water_distribution service_ward_ catchment{Ward}</td>
</tr>
<tr class="odd">
<td rowspan="5">Year</td>
<td>tor:water_distribution service_ward{Ward}_{Year}</td>
<td>change:existsAt</td>
<td>tor:interval_{year}</td>
<td rowspan="5">Year in yyyy format</td>
</tr>
<tr class="even">
<td>tor:interval_{year}</td>
<td>time:hasBeginning</td>
<td>tor:instant_{year}_start</td>
</tr>
<tr class="odd">
<td>tor:interval_{year}</td>
<td>time:hasEnd</td>
<td>tor:instant_{year}_end</td>
</tr>
<tr class="even">
<td>tor:instant_{year}_start</td>
<td>time:inXSDDateTimeStamp</td>
<td>{year}-01-01T00:00:00-05:00</td>
</tr>
<tr class="odd">
<td>tor:instant_{year}_end</td>
<td>time:inXSDDateTimeStamp</td>
<td>{year}-12-31T23:59:59-05:00</td>
</tr>
<tr class="even">
<td rowspan="5">Total consumption (m3)</td>
<td>tor:water_distributionservice_ ward {Ward}_{Year}</td>
<td>res:capacityInUse</td>
<td><p>tor:water_distribution</p>
<p>service_ward {Ward}_{Year}_capacityuse</p></td>
<td rowspan="5">Total annual usage</td>
</tr>
<tr class="odd">
<td>tor:water_distributionservice_ ward {Ward}_{Year}_capacityuse</td>
<td>rdf:type</td>
<td>hp:WaterDistributionRate</td>
</tr>
<tr class="even">
<td>tor:water_distributionservice_ ward {Ward}_{Year}_capacityuse</td>
<td>i72:hasValue</td>
<td><p>tor:water_distribution service_ward{Ward}_</p>
<p>{Year}_capacityuse_ measure</p></td>
</tr>
<tr class="odd">
<td>tor:water_distributionservice_
ward{Ward}_{Year}_capacityuse_measure</td>
<td>i72:hasNumerical Value</td>
<td>"Total consumption (m3)"</td>
</tr>
<tr class="even">
<td>tor:water_distributionservice_
ward{Ward}_{Year}_capacityuse_measure</td>
<td>i72:hasUnit</td>
<td>hp:cubic_meter_per_ year</td>
</tr>
</tbody>
</table>

Table 3: Mapping Water Billing (by ward) Data to City Digital Twins

Toronto [Water billing by
ward](https://data.urbandatacentre.ca/catalogue/city-toronto-water-billing-by-ward)
provides a measure of capacity use

In this case, wards are simply used as a means of aggregating water
usage.  
We can interpret this data as providing usage for sub-services of the
city-wide water distribution service, where the water distribution is
broken down by ward  
This data gives us an annual consumption rate though in theory the
numbers should be available e.g. per day per region.

<table>
<colgroup>
<col style="width: 9%" />
<col style="width: 32%" />
<col style="width: 22%" />
<col style="width: 24%" />
<col style="width: 10%" />
</colgroup>
<thead>
<tr class="header">
<th colspan="5"><strong>Data Provided by Water Capacity
Dataset</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><strong>Field Name</strong></td>
<td><strong>Subject</strong></td>
<td><strong>Property</strong></td>
<td><strong>Object</strong></td>
<td><strong>Notes</strong></td>
</tr>
<tr class="even">
<td rowspan="5">Synthetic Capacity</td>
<td><p>tor:water_distribution</p>
<p>service_ward{Ward}_{Year}</p></td>
<td>res:hasCapacity</td>
<td><p>tor:water_distribution</p>
<p>service_ward{Ward}_{Year}_Capacity</p></td>
<td rowspan="5">use measured in m3/year</td>
</tr>
<tr class="odd">
<td><p>tor:water_distribution</p>
<p>service_ward{Ward}_{Year}_Capacity</p></td>
<td>rdf:type</td>
<td>hp:WaterDistributionRate</td>
</tr>
<tr class="even">
<td><p>tor:water_distribution</p>
<p>service_ward{Ward}_{Year}_Capacity</p></td>
<td>i72:hasValue</td>
<td><p>tor:water_distribution</p>
<p>service_ward{Ward}_{Year}_CapacityMeasure</p></td>
</tr>
<tr class="odd">
<td><p>tor:water_distribution</p>
<p>service_ward{Ward}_{Year}_Capacity</p>
<p>Measure</p></td>
<td>i72:hasNumericalValue</td>
<td>"{Synthetic Capacity}"</td>
</tr>
<tr class="even">
<td><p>tor:water_distribution</p>
<p>service_ward{Ward}_{Year}_Capacity</p>
<p>Measure</p></td>
<td>i72:hasUnit</td>
<td>hp:cubic_metre_per_year</td>
</tr>
<tr class="odd">
<td rowspan="5">Synthetic Available Capacity</td>
<td><p>tor:water_distribution</p>
<p>service_ward{Ward}_{Year}</p></td>
<td>res:hasAvailableCapacity</td>
<td><p>tor:water_distribution</p>
<p>service_ward{Ward}_{Year}_AvailCapacity</p></td>
<td rowspan="5">use measured in m3/year</td>
</tr>
<tr class="even">
<td><p>tor:water_distribution</p>
<p>service_ward{Ward}_{Year}_Avail</p>
<p>Capacity</p></td>
<td>rdf:type</td>
<td>hp:AvailableWaterDistributionRate</td>
</tr>
<tr class="odd">
<td><p>tor:water_distribution</p>
<p>service_ward{Ward}_{Year}_Avail</p>
<p>Capacity</p></td>
<td>i72:hasValue</td>
<td><p>tor:water_distribution</p>
<p>service_ward{Ward}_{Year}</p>
<p>_AvailCapacityMeasure</p></td>
</tr>
<tr class="even">
<td>tor:water_distributionservice_ward
{Ward}_{Year}_AvailCapacityMeasure</td>
<td>i72:hasNumericalValue</td>
<td>"{Synthetic Available Capacity}"</td>
</tr>
<tr class="odd">
<td>tor:water_distributionservice_ward
{Ward}_{Year}_AvailCapacityMeasure</td>
<td>i72:hasUnit</td>
<td>hp:cubic_metre_per_year</td>
</tr>
</tbody>
</table>

Implementation of Water Data in Mapping TTL

**Script:**
[Water&Water_Capacity.py](https://github.com/csse-uoft/city-digital-twin-ontology/tree/main/Housing%20Potential%20Python)

**URI strategy**

The script generates deterministic URIs under the tor: namespace so that
pipes and ward-year services can be referenced consistently:

- **City-wide service:** tor:waterservice

- **Distribution pipe (per asset row):**
  tor:waterservice_distributionpipes{\_id}

- **Pipe location node:** tor:waterservice_distributionpipes_loc{\_id}

- **Ward-year distribution sub-service:**
  tor:water_distributionservice_ward{Ward}\_{Year}

- **Ward catchment area:**
  tor:water_distributionservice_ward_catchment{Ward}

- **Annual time interval/instants:**

  - tor:interval\_{Year}

  - tor:instant\_{Year}\_start, tor:instant\_{Year}\_end

- **Consumption (capacity-in-use) rate + measure:**

  - tor:water_distributionservice_ward{Ward}\_{Year}\_capacityuse

  - tor:water_distributionservice_ward{Ward}\_{Year}\_capacityuse_measure

- **Total capacity + measure:**

  - tor:water_distributionservice_ward{Ward}\_{Year}\_Capacity

  - tor:water_distributionservice_ward{Ward}\_{Year}\_CapacityMeasure

- **Available capacity + measure:**

  - tor:water_distributionservice_ward{Ward}\_{Year}\_AvailCapacity

  - tor:water_distributionservice_ward{Ward}\_{Year}\_AvailCapacityMeasure

**Inputs**

1.  **Watermain geometry + identifiers**

    - Distribution Watermain - 4326.csv

    - Required fields used:

      - \_id (for URI construction)

      - Watermain Asset Identification (identifier literal)

      - geometry (GeoJSON string converted to WKT)

2.  **Ward-year consumption (water billing)**

    - Water_Consumption_YYYY.xls/xlsx files (script is written to
      iterate across many years)

    - Required columns (names vary by file, script matches flexibly):

      - City ward

      - Year

      - Total consumption

3.  **Ward-year synthetic capacity**

    - Water_Consumption_Capacity_2020(Water_Consumption_2020).csv

    - Required columns:

      - city ward, year

      - Synthetic Capacity

      - Synthetic Available Capacity

4.  **Ward locations (for catchment geometry)**

    - The script queries the existing City Digital Twin knowledge graph
      (GraphDB SPARQL endpoint) to retrieve Ward instances and their
      hasLocation nodes (and geo:asWKT), so catchment areas inherit the
      ward geometry for Toronto.

**Outputs**

- water.ttl  
  Contains: water service, distribution pipes + their geometries,
  ward-year sub-services, catchment-area links, annual time intervals,
  and ward-year consumption (capacity in use).

- water_capacity.ttl  
  Contains: ward-year total capacity and available capacity measures.

**Step-by-step process**

**Step 1 - Initialize RDF graphs and namespaces**  
Two RDF graphs are created:

- g for the core water service + pipes + ward-year consumption

- capacity_g for ward-year (total/available) capacity values  
  Namespaces are bound (e.g., tor:, hp:, loc:, geo:, res:, i72:,
  service:, change:, time:).

**Step 2 - Create the top-level WaterService instance**  
tor:waterservice is created and typed as tor:TorWaterService.

**Step 3 - Create catchment areas by linking to existing Ward
geometries**  
The script runs a SPARQL query to retrieve each toronto:Ward and its
iso50871:hasLocation. For each ward:

- A catchment URI (tor:water_distributionservice_ward_catchment{Ward})
  is created.

- The catchment is linked to the ward’s location node via
  loc:hasLocation.

- The ward location’s geo:asWKT is also pulled and asserted in the
  output graph so the geometry is present for downstream use.

**Step 4 - Map distribution pipes (watermains) with geometry**  
For each row in Distribution Watermain - 4326.csv:

- A pipe node tor:waterservice_distributionpipes{\_id} is created.

- The pipe is linked from the service using hp:providedFromSite.

- The asset identifier is stored using genprop:hasIdentifier.

- A location node is created and linked using loc:hasLocation.

- The GeoJSON LineString / MultiLineString is converted into a WKT
  LINESTRING(...) and stored via geo:asWKT on the location node.

**Step 5 - Map ward-year consumption as capacity-in-use with time
interval**  
For each year file in the consumption list:

- The script detects the ward/year/total consumption columns (even if
  they include newlines/spaces).

- For each valid ward-year row:

  - Create the ward-year distribution service
    tor:water_distributionservice_ward{Ward}\_{Year}.

  - Link it from tor:waterservice using hp:hasSubService.

  - Link it to the ward catchment using service:hasCatchmentArea.

  - Add a temporal interval for the year using change:existAt pointing
    to tor:interval\_{Year}, with beginning/end instants (Jan 1 to Dec
    31 timestamps).

  - Represent consumption as a hp:WaterDistributionRate linked by
    res:capacityInUse, with ISO 21972 measurement structure:

    - i72:hasValue → measure node

    - i72:hasNumericalValue → consumption number

    - i72:hasUnit → hp:cubic_metre_per_year

**Step 6 - Map synthetic total and available capacity**  
For each ward-year row in the capacity CSV:

- The script creates two rate nodes:

  - total capacity linked via res:hasCapacity

  - available capacity linked via res:hasAvailableCapacity

- Each is typed as hp:WaterDistributionRate and recorded with:

  - i72:hasValue → measure node

  - i72:hasNumericalValue → parsed numeric value (commas removed)

  - i72:hasUnit → hp:cubic_metre_per_year

**Step 7 - Serialize TTL**  
The graphs are written to:

- water.ttl

- water_capacity.ttl

**Notes / assumptions**

- Catchment geometries depend on the SPARQL endpoint being reachable; if
  the ward location lookup fails, catchment areas may be missing
  geometry/location triples.

- Pipe geometry conversion assumes the geometry column is valid GeoJSON
  for LineString or MultiLineString.

- All ward-year rates are stored in **m³/year**
  (hp:cubic_metre_per_year).

- Annual interval timestamps are generated in an explicit -05:00 offset
  in the script.
