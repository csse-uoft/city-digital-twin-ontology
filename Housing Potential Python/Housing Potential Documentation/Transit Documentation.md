Transit Documentation

Relevant Python Scripts:

- [**TransitStop.py**](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/TransitStop.py):
  generates the RDF data related to TTC transit stops using the TTC GTFS
  data from the Toronto Open Data Portal.

  - Dataset links

    - <https://open.toronto.ca/dataset/ttc-routes-and-schedules/>

- [**TransitRoute.py**](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/TransitRoute.py):
  generates the RDF data for the transit capacities (e.g., ridership
  data) using the TTC GTFS data from the Toronto Open Data Portal as
  well as synthetic data.

  - Dataset links

    - <https://open.toronto.ca/dataset/ttc-ridership-all-day-weekday-for-surface-routes/>

This is the ontological representation of Toronto’s TTC transit data.
Transit stops are represented as instances of the cdt:TransitStop class
while ridership data is represented as capacity in use and supplemented
with synthetic data in order to calculate the capacity and available
capacity information.

This section summarizes how the transit related datasets are mapped into
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

<img src="/media/image.png" style="width:5.40625in;height:6.5in" />

| **Data Provided By The TTC GTFS Datasets (RDF generation done using TransitStop.py)** |  |  |  |  |
|:---|:---|:---|:---|:---|
| **Field Name** | **Subject** | **Property** | **Object** | **Notes** |
| stop_id | tor:{stop_id}TransitStop | rdf:type | cdt:TransitStop |  |
| stop_lat, stop_lon | tor:{stop_id}TransitStop | loc:hasLocation | tor:{stop_id}TransitStop_loc |  |
|  | tor:{stop_id}TransitStop_loc | geo:asWKT | "POINT({stop_lat} {stop_lon})" |  |
| stop_name | cdt:{stop_id}TransitStop | genprop:hasName | "{stop_name}" |  |
| stop_id | cdt:{stop_id}TransitStop | genprop:hasIdentifier | "{stop_id}” |  |
| Operator | tor:ttc | org:hasSite | cdt:{stop_id}TransitStop |  |
|  | tor:ttc | genprop:hasName | "Toronto Transit Commission" |  |
| route_id | tor:ttc | cdt:providesService | tor:{route_id}RouteService | derived for each stop by identifying the trips (via stop_times) and associated routes |
|  | tor:{route_id}RouteService | hp:providedFromSite | Site stop_id |  |

<table>
<colgroup>
<col style="width: 15%" />
<col style="width: 19%" />
<col style="width: 9%" />
<col style="width: 19%" />
<col style="width: 35%" />
</colgroup>
<thead>
<tr>
<th colspan="5" style="text-align: left;"><strong>Data Provided By The
TTC Ridership Data (RDF generation done using
TransitRoute.py)</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Field Name</strong></td>
<td style="text-align: left;"><strong>Subject</strong></td>
<td style="text-align: left;"><strong>Property</strong></td>
<td style="text-align: left;"><strong>Object</strong></td>
<td style="text-align: left;"><strong>Notes</strong></td>
</tr>
<tr>
<td rowspan="2" style="text-align: left;">route_id (via TTC stops)</td>
<td style="text-align: left;">tor:{route_id}RouteService</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">tor:TorPublicTransitService</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">tor:{route_id}RouteService</td>
<td style="text-align: left;">genprop:hasIdentifier</td>
<td style="text-align: left;">"{route_short_name}"</td>
<td style="text-align: left;">Integrated with GTFS via matching
"route_short_name" to "Route #"</td>
</tr>
<tr>
<td rowspan="2" style="text-align: left;">route_short_name (via TTC
stops routes.txt),<br />
Route # (via ridership)</td>
<td style="text-align: left;">tor:{route_id}RouteService</td>
<td style="text-align: left;">res:capacityInUse</td>
<td style="text-align: left;">tor:{route_id}RouteServiceCapacityUse</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">tor:{route_id}RouteServiceCapacityUse</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">hp:PassengerThroughputRate</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td rowspan="3" style="text-align: left;">All-Day Ridership (via
ridership)</td>
<td style="text-align: left;">tor:{route_id}RouteServiceCapacityUse</td>
<td style="text-align: left;">i72:hasValue</td>
<td
style="text-align: left;">tor:{route_id}RouteServiceCapacityUseMeausre</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td
style="text-align: left;">tor:{route_id}RouteServiceCapacityUseMeausre</td>
<td style="text-align: left;">i72:hasNumericalValue</td>
<td style="text-align: left;">"{All Day Ridership}"</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td
style="text-align: left;">tor:{route_id}RouteServiceCapacityUseMeausre</td>
<td style="text-align: left;">i72:hasUnit</td>
<td style="text-align: left;">hp:person_per_day</td>
<td style="text-align: left;"></td>
</tr>
</tbody>
</table>

| **Data Provided By The Synthetic Dataset (RDF generation done using TransitRoute.py)** |  |  |  |  |
|:---|:---|:---|:---|:---|
| **Field Name** | **Subject** | **Property** | **Object** | **Notes** |
| route_id | tor:{route_id}RouteService | res:hasCapacity | tor:{route_id}RouteServiceCapacityTotal |  |
|  | tor:{route_id}RouteServiceCapacityTotal | rdf:type | hp:MinPassengerThroughputRate |  |
| daily_passenger_throughput | tor:{route_id}RouteServiceCapacityTotal | i72:hasValue | tor:{route_id}RouteServiceCapacityTotalMeasure |  |
|  | tor:{route_id}RouteServiceCapacityTotalMeasure | i72:hasNumericalValue | "{daily_passenger_throughput}" |  |
|  | tor:{route_id}RouteServiceCapacityTotalMeasure | i72:hasUnit | hp:person_per_day |  |
|  | tor:{route_id}RouteService | res:hasAvailableCapacity | tor:{route_id}RouteServiceCapacityAvail | available capacities not defined in synthetic data (can be retrieved via difference between total and in-use capacities) |
|  | tor:{route_id}RouteServiceCapacityAvail | rdf:type | hp:AvailablePassengerThroughputRate |  |
|  | tor:{route_id}RouteServiceCapacityAvail | i72:hasValue | tor:{route_id}RouteServiceCapacityAvailMeasure |  |
|  | tor:{route_id}RouteServiceCapacityAvailMeasure | i72:hasNumericalValue | {capacity – capacity use} |  |
|  | tor:{route_id}RouteServiceCapacityAvailMeasure | i72:hasUnit | hp:person_per_day |  |

Implementation of Transit Related Data in Mapping TTL

**Scripts:** TransitStop.py

**URI strategy**

- **Transit Stop:**

  - tor:{stop_id}TransitStop

- **Transit Stop Location**:

  - tor:{stop_id}TransitStop_loc

- **Transit Route Service:**

  - tor:{route_id}RouteService

**Scripts:** TransitRoute.py

- **Transit Route Service:**

  - tor:{route_id}RouteService

- **Transit Capacity Use (Ridership):**

  - tor:{route_id}RouteServiceCapacityUse

- **Transit Capacity Total:**

  - tor:{route_id}RouteServiceCapacityTotal

- **Transit Capacity Available:**

  - tor:{route_id}RouteServiceCapacityAvail

**Inputs**

1.  **TTC GTFS Data (TransitStop.py)**

    - Dataset links

      - <https://open.toronto.ca/dataset/ttc-routes-and-schedules/>

    - GTFS Data on the Toronto Open Data Portal is downloaded as a zip
      file which needs to be extracted before use with the Python
      script. Data within the GTFS zip file is stored as CSV files.

2.  **TTC Route Ridership Data + Synthetic Data (TransitRoute.py)**

    - Dataset links

      - <https://open.toronto.ca/dataset/ttc-ridership-all-day-weekday-for-surface-routes/>

      - TTC_est_throughput_report.csv

    - Ridership data is downloaded as an XLSX file and can be directly
      accessed using the Python script.

**Outputs**

- TransitRoute.ttl (TransitRoute.py)  
  Contains: Transit ridership information based on transit route (i.e.,
  capacity use information)

- TransitSynthetic.ttl (TransitRoute.py)  
  Contains: Synthetic information about total and available transit
  capacities

- TransitStop.ttl (TransitStop.py)  
  Contains: Contains information and location of TTC transit stops

**Step-by-step process for TransitRoute.py**

**Step 1 - Initialize RDF graphs and namespaces**  
Two RDF graphs are created:

- g contains the TTC ridership information (i.e., capacity use)

- g2 contains the synthetic information (i.e., total capacity and
  available capacity)

**Step 2 – Import csv datasets using pandas Python package**  
Route data is contained in the “routes” Pandas dataframe, trip data is
contained in the “trips” dataframe, stop time data is contained in the
“stop_times” dataframe then, unnecessary columns are dropped before the
dataframes are merged into one dataframe called “route_stops” for
row-by-row parsing.

**Note:** All 3 datasets are needed in order to connect route_id with
the trip_id, and then the stop_id in the TTC GTFS data.

**Note 2:** The datasets found in the GTFS data are stored as .txt files
but they are formatted as CSV files.

**Step 3 – Merge route_stops dataframe with TTC ridership data**

The TTC ridership XLSX dataset is imported using the pandas Python
package and is then merged with the route_stops dataframe. The ridership
information will be used as the capacity use values later in the script.

**Step 4 - RDF triples are created using each row of data in the
route_stops dataframe**  
The route_stops dataframe is iterated row by row and RDF triples are
generated according to the mapping specifications outlined in the tables
found earlier in this document. Values for the triples are extracted
from the corresponding column in the dataframe.

**Note:** The ridership values for each route are also recorded in a
Python dictionary called “d” as they are needed later for the
calculation of the available capacity data. Routes that have invalid
ridership values in the dataset (e.g., “TBD”) are treated as having a
ridership value of 0.

**Step 5 – Generate RDF triples for synthetic data**  
Repeat steps 2 and 4 for the synthetic transit data. Synthetic data is
also imported using pandas and stored in the “synthetic” dataframe.
Triples are generated by iterating row by row through the synthetic
dataframe.

**Note:** Available capacities are calculated by subtracting the TTC
ridership values from the synthetic total capacity data.

**Step 6 - Serialize TTL**  
The graphs are written to TransitRoute.ttl (for capacity use data) and
TransitSynthetic.ttl (for total and available capacity data).

**Step-by-step process for TransitStop.py**

**Step 1 - Initialize RDF graphs and namespaces**  
One RDF graph is created:

- g contains all triples found in the output ttl file

**Step 2 – Import CSV dataset using csv Python package**  
The imported csv data is stored in the “data” variable.

**Step 3 – RDF triples are created using each row of data in the
imported CSV data**  
The data is iterated row by row and RDF triples are generated according
to the mapping specifications outlined in the tables found earlier in
this document. Values for the triples are extracted from the
corresponding column in the data.

**Step 4 - Serialize TTL**  
The graphs are written to TransitStop.ttl.
