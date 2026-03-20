Supermarket Documentation

Relevant Python Scripts:

- [Supermarket.py](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/Supermarket.py):
  generates the RDF data related to supermarkets in Toronto and their
  capacities.

  - Dataset links

    - Supermarket.geojson (data from OSM can be extracted using Overpass
      Turbo (<https://overpass-turbo.eu/>) by typing in
      “shop=supermarket in Toronto” in the wizard)

    - SupermarketNumerator.csv (SPARQL query results exported as a csv
      file)

> PREFIX geo: \<http://www.opengis.net/ont/geosparql#\>

- PREFIX geof: \<http://www.opengis.net/def/function/geosparql/\>

- PREFIX uom: \<http://www.opengis.net/def/uom/OGC/1.0/\>

- PREFIX loc:
  \<https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/\>

- PREFIX i72: \<http://ontology.eil.utoronto.ca/ISO21972/iso21972#\>

- PREFIX hp: \<http://ontology.eil.utoronto.ca/HPCDM/\>

- PREFIX service:
  \<https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/CityService/\>

- SELECT ?s (COUNT(DISTINCT ?s2) AS ?nearbySchoolCount) {

- ?s a hp:SupermarketService;

- hp:providedFromSite ?site.

- ?site loc:hasLocation ?sloc.

- ?sloc geo:asWKT ?swkt.

- \#service-defined radius, in metres

- ?s hp:hasServiceRadius \[i72:hasValue \[i72:hasNumericalValue ?max_d;

- i72:hasUnit i72:metre\]\].

- \#other school services

- ?s2 a hp:SupermarketService;

- hp:providedFromSite \[loc:hasLocation ?s2loc\].

- ?s2loc geo:asWKT ?s2wkt.

- \#service radius

- \#BIND(geof:buffer(?swkt, ?max_d, uom:metre) AS ?service_area)

- 

- \#find other school sites within the servic area

- FILTER (?s != ?s2)

- FILTER(geof:distance(?swkt, ?s2wkt, uom:metre) \<= ?max_d)

- 

- \#?s2loc geo:sfwtihin ?service_area

- \#FILTER (geof:sfWithin(?s2wkt, ?service_area))

- } GROUP BY ?s

This is the ontological representation of Toronto’s supermarket data
from OpenStreetMap. Supermarkets are represented as instances of the
cdt:Supermarket class while their services are represented as instances
of the tor:TorSupermarketService class and synthetic data is used for
the capacity values.

This section summarizes how the supermarket related datasets are mapped
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

<img src="/media/image.png" style="width:6.5in;height:5.30208in" />

<table>
<colgroup>
<col style="width: 7%" />
<col style="width: 15%" />
<col style="width: 10%" />
<col style="width: 15%" />
<col style="width: 49%" />
</colgroup>
<thead>
<tr>
<th colspan="5" style="text-align: left;"><strong>Data Provided By the
OSM Supermarket Dataset (RDF generation done using
Supermarket.py)</strong></th>
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
<td rowspan="4" style="text-align: left;">Supermarket</td>
<td style="text-align: left;">tor: {OSM ID}Supermarket</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">cdt:Supermarket</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}SupermarketService</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">tor:TorSupermarketService</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}SupermarketService</td>
<td style="text-align: left;">service:hasCatchmentArea</td>
<td style="text-align: left;">tor: {OSM
ID}SupermarketServiceCatchmentLoc</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM
ID}SupermarketServiceCatchmentLoc</td>
<td style="text-align: left;">geo:asWKT</td>
<td style="text-align: left;">computed polygon 5000m boundary from
{geometry}</td>
<td style="text-align: left;">Note: this should be computable with
SPARQL (e.g. with geof:buffer) but may be more efficient directly in the
mapping</td>
</tr>
<tr>
<td rowspan="6" style="text-align: left;">geometry</td>
<td style="text-align: left;">tor: {OSM ID} Supermarket</td>
<td style="text-align: left;">org:hasSite</td>
<td style="text-align: left;">tor: {OSM ID} SupermarketSite</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM
ID}SupermarketServiceCatchmentLoc</td>
<td style="text-align: left;">hp:providedFromSite</td>
<td style="text-align: left;">tor: {OSM ID} SupermarketSite</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}SupermarketSite</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">cdt:Site</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}SupermarketSite</td>
<td style="text-align: left;">genprop:hasName</td>
<td style="text-align: left;">“{name}”</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}SupermarketSite</td>
<td style="text-align: left;">loc:hasLocation</td>
<td style="text-align: left;">tor: {OSM ID}SupermarketSiteLoc</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}SupermarketSiteLoc</td>
<td style="text-align: left;">geo:asWKT</td>
<td style="text-align: left;">“{geometry}” (the geometry here is
converted to WKT format)</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">id</td>
<td style="text-align: left;">tor: {OSM ID}Supermarket</td>
<td style="text-align: left;">genprop:hasIdentifier</td>
<td style="text-align: left;">“{OSM ID}”</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">name</td>
<td style="text-align: left;">tor: {OSM ID}Supermarket</td>
<td style="text-align: left;">genprop:hasName</td>
<td style="text-align: left;">“{name}”</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td rowspan="5" style="text-align: left;">Address<br />
<br />
<em>Generally, the address information in OpenStreetMap is represented
using multiple properties such as addr:housenumber, addr:street, and
addr:postcode.</em></td>
<td style="text-align: left;">tor: {OSM ID}SupermarketSiteLoc</td>
<td style="text-align: left;">org:siteAddress</td>
<td style="text-align: left;">tor: {OSM ID}SupermarketAddress</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}SupermarketAddress</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">contact:Address</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}SupermarketAddress</td>
<td style="text-align: left;">contact:hasStreetNumber</td>
<td style="text-align: left;">“{addr:housenumber}”</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}SupermarketAddress</td>
<td style="text-align: left;">contact:hasStreet (where appropriate, the
information in addr:street is separated and represented in more detail
using additional properties from the contact ontology e.g.,
contact:hasStreetType)</td>
<td style="text-align: left;">“{addr:street}”</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}SupermarketAddress</td>
<td style="text-align: left;">contact:hasPostalCode</td>
<td style="text-align: left;">“{addr:postcode}”</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td rowspan="4" style="text-align: left;">operator</td>
<td rowspan="2" style="text-align: left;">tor:{operator}</td>
<td rowspan="2" style="text-align: left;">rdf:type</td>
<td rowspan="2" style="text-align: left;">cdt:Organization</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;"></td>
</tr>
<tr>
<td rowspan="2" style="text-align: left;">tor:{operator}</td>
<td rowspan="2" style="text-align: left;">org:hasSubOrganization</td>
<td rowspan="2" style="text-align: left;">tor: {OSM ID}Supermarket</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;"></td>
</tr>
</tbody>
</table>

| **Data Provided By the Synthetic Supermarket Capacity Information (RDF generation done using Supermarket.py)** |  |  |  |
|:---|:---|:---|:---|
| **Subject** | **Property** | **Object** | **Notes** |
| tor: {OSM ID}SupermarketServiceCatchmentLoc | res:hasCapacity | tor: {OSM ID}SupermarketServiceCapacity | defined based on the recommendation of 1 store per 10000 residents |
| tor: {OSM ID}SupermarketServiceCapacity | rdf:type | hp:MinSupermarketsPopulationRatio |  |
| tor: {OSM ID}SupermarketServiceCapacity | i72:hasValue | tor: {OSM ID}SupermarketServiceCapacityMeasure |  |
| tor: {OSM ID}SupermarketServiceCapacityMeasure | i72:hasNumericalValue | 0.001 | defined based on the recommendation of 1 store per 10000 residents |
| tor: {OSM ID}SupermarketServiceCapacityMeasure | i72:hasUnit | hp:sites_per_person |  |
| tor: {OSM ID}SupermarketService | res:capacityInUse | tor: {OSM ID}SupermarketServiceCapacityUse | defined based on the recommendation of 1 store per 10000 residents |
| tor: {OSM ID}SupermarketServiceCapacityUse | rdf:type | hp:SupermarketsPopulationRatio |  |
| tor: {OSM ID}SupermarketServiceCapacityUse | i72:denominator | tor: {OSM ID}SupermarketServiceCatchmentPopSize | ratio may be computed by querying for supermarket count (the i72:numerator) and dividing with the i72:denominator |
| tor: {OSM ID}SupermarketServiceCatchmentPopSize | rdf:type | hp:ResidentPopulation |  |
| tor: {OSM ID}SupermarketServiceCatchmentPopSize | i72:hasValue | tor: {OSM ID}SupermarketServiceCatchmentPopSizeMeasure |  |
| tor: {OSM ID}SupermarketServiceCatchmentPopSizeMeasure | i72:hasNumericalValue | 22139 | very rough estimate (total toronto population \* catchment area size / toronto area size) |
| tor: {OSM ID}SupermarketServiceCatchmentPopSizeMeasure | i72:hasUnit | i72:population_cardinality_unit |  |
| tor: {OSM ID}SupermarketServiceCapacityUse | i72:numerator | tor:{OSM ID}CatchmentSupermarketCount | a count of the number of supermarkets in the catchment area |
| tor:{OSM ID}CatchmentSupermarketCount | rdf:type | i72:Population |  |
| tor:{OSM ID}CatchmentSupermarketCount | i72:hasValue | tor:{OSM ID}CatchmentSupermarketCountMeasure |  |
| tor:{OSM ID}CatchmentSupermarketCountMeasure | i72:hasNumericalValue | (TBD) |  |
| tor:{OSM ID}CatchmentSupermarketCountMeasure | i72:hasUnit | i72:population_cardinality_unit |  |
| tor: {OSM ID}SupermarketServiceCapacityUse | i72:hasValue | tor: {OSM ID}SupermarketServiceCapacityUseMeasure |  |
| tor: {OSM ID}SupermarketServiceCapacityUseMeasure | i72:hasNumericalValue | (TBD) |  |
| tor: {OSM ID}SupermarketServiceCapacityUseMeasure | i72:hasUnit | hp:sites_per_person |  |
| tor: {OSM ID}SupermarketService | res:hasAvailableCapacity | tor: {OSM ID}SupermarketServiceCapacityAvail |  |
| tor: {OSM ID}SupermarketServiceCapacityAvail | rdf:type | hp:SupermarketsPopulationRatio |  |
| tor: {OSM ID}SupermarketServiceCapacityAvail | i72:hasValue | tor: {OSM ID}SupermarketServiceCapacityAvailMeasure |  |
| tor: {OSM ID}SupermarketServiceCapacityAvailMeasure | i72:hasNumericalValue | {capacity - capacity use} |  |
| tor: {OSM ID}SupermarketServiceCapacityAvailMeasure | i72:hasUnit | hp:sites_per_person |  |

Implementation of Supermarket Related Data in Mapping TTL

**Scripts:** Supermarket.py

**URI strategy**

- **Supermarket:**

  - tor: {OSM ID}Supermarket

- **Supermarket Site:**

  - tor: {OSM ID} SupermarketSite

- **Supermarket Site Location:**

  - tor: {OSM ID}SupermarketSiteLoc

- **Supermarket Capacity:**

  - tor: {OSM ID}SupermarketServiceCapacity

- **Supermarket Capacity Use:**

  - tor: {OSM ID}SupermarketServiceCapacityUse

- **Supermarket Capacity Available:**

  - tor: {OSM ID}SupermarketServiceCapacityAvail

**Inputs**

1.  **OSM Toronto Supermarket Data (Supermarket.py)**

    - Dataset links

      - <https://services8.arcgis.com/SnGTjuDV2RIxBTxw/ArcGIS/rest/services/PRD_FeederLayers/FeatureServer>

    - Data from OSM can be extracted as a geoJSON using Overpass Turbo
      (<https://overpass-turbo.eu/>) by typing in “shop=supermarket in
      Toronto” in the wizard

2.  **Synthetic Supermarket Capacity Data (Supermarket.py)**

    - Data from SPARQL query

      - SupermarketNumerator.csv

    - SPARQL query results exported as a csv file

**Outputs**

- Supermarket.ttl (Supermarket.py)  
  Contains: OSM supermarket data for Toronto and their locations.

- SupermarketCapacity.ttl (Supermarket.py)  
  Contains: Synthetic information about supermarket capacities

**Step-by-step process for Supermarket.py**

**Step 1 - Initialize RDF graphs and namespaces**  
Two RDF graphs are created:

- g contains OSM supermarket data for Toronto and their locations.

- g2 contains synthetic information about supermarket capacities

**Step 2 – Import geoJSON dataset using the json Python package**  
The data from the supermarket dataset is contained in the “amenity”
variable.

**Step 3 – Import CSV dataset using the pandas Python package**  
The data from the SPARQL query is contained in the “df” dataframe.

**Step 4 - RDF triples are created using each row in the dataframe**  
The data in the df dataframe is iterated row by row and RDF triples are
generated according to the mapping specifications outlined in the tables
found earlier in this document. Values for the triples are extracted
from the corresponding column in the data.

**Step 5 - RDF triples are created using each feature in the data**  
The data in stored in the amenity variable is iterated feature by
feature and RDF triples are generated according to the mapping
specifications outlined in the tables found earlier in this document.
Values for the triples are extracted from the corresponding property in
the data.

**Note:** In cases where there is no data in step 4, the value of
CatchmentSupermarketCount is assumed to be 1 and capacity information is
generated accordingly.

**Step 6- Serialize TTL**  
The graph g is written to Supermarket.ttl and g2 is written to
SupermarketCapacity.ttl.
