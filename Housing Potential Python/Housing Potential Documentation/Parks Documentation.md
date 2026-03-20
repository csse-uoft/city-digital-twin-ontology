Parks Documentation

Relevant Python Scripts:

- [Parks2.py](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/Parks2.py):
  generates the RDF data related to parks in Toronto.

  - Dataset links

    - parks.geojson (data from OSM can be extracted using Overpass Turbo
      (<https://overpass-turbo.eu/>) by typing in “leisure=park in
      Toronto” in the wizard)

This is the ontological representation of Toronto’s park data from
OpenStreetMap. Services provided by parks are represented as instances
of the tor:TorParkService class while the capacity data is synthetically
approximated using surface area data and an estimated catchment
population size.

This section summarizes how the park related datasets are mapped into
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

- i72: <http://ontology.eil.utoronto.ca/ISO21972/iso21972>\#

- cityunits:
  <https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/CityUnits/>

<img src="/media/image.png" style="width:6.5in;height:5.9375in" />

<table>
<colgroup>
<col style="width: 17%" />
<col style="width: 31%" />
<col style="width: 24%" />
<col style="width: 26%" />
</colgroup>
<thead>
<tr>
<th colspan="4" style="text-align: left;"><strong>Data Provided By the
OSM Park Dataset (RDF generation done using Parks.py)</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Field Name</strong></td>
<td style="text-align: left;"><strong>Subject</strong></td>
<td style="text-align: left;"><strong>Property</strong></td>
<td style="text-align: left;"><strong>Object</strong></td>
</tr>
<tr>
<td rowspan="3" style="text-align: left;">Park</td>
<td style="text-align: left;">tor: {OSM ID}ParkOrg</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">org:Organization</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}ParkService</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">tor:TorParkService</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}ParkOrg</td>
<td style="text-align: left;">cdt:providesService</td>
<td style="text-align: left;">tor: {OSM ID}ParkService</td>
</tr>
<tr>
<td rowspan="2" style="text-align: left;">Catchment area (manually
defined)</td>
<td style="text-align: left;">tor: {OSM ID}ParkService</td>
<td style="text-align: left;">service:hasCatchmentArea</td>
<td style="text-align: left;">tor: {OSM ID}Catchment</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}Catchment</td>
<td style="text-align: left;">geo:asWKT</td>
<td style="text-align: left;">800m radius from {geometry}</td>
</tr>
<tr>
<td rowspan="5" style="text-align: left;">geometry</td>
<td style="text-align: left;">tor: {OSM ID}ParkOrg</td>
<td style="text-align: left;">org:hasSite</td>
<td style="text-align: left;">tor: {OSM ID} ParkSite</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}ParkService</td>
<td style="text-align: left;">hp:providedFromSite</td>
<td style="text-align: left;">tor: {OSM ID} ParkSite</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID} ParkSite</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">cdt:Park</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID} ParkSite</td>
<td style="text-align: left;">loc:hasLocation</td>
<td style="text-align: left;">tor: {OSM ID} ParkSiteLoc</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID} ParkSiteLoc</td>
<td style="text-align: left;">geo:asWKT</td>
<td style="text-align: left;">“{geometry}” (the geometry here is
converted to WKT format)</td>
</tr>
<tr>
<td style="text-align: left;">id</td>
<td style="text-align: left;">tor: {OSM ID} ParkSite</td>
<td style="text-align: left;">genprop:hasIdentifier</td>
<td style="text-align: left;">“{OSM ID}”</td>
</tr>
<tr>
<td rowspan="2" style="text-align: left;">name</td>
<td style="text-align: left;">tor: {OSM ID} ParkSite</td>
<td style="text-align: left;">genprop:hasName</td>
<td style="text-align: left;">“{name}”</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID} ParkSite</td>
<td style="text-align: left;">org:siteAddress</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td rowspan="4" style="text-align: left;">Address<br />
<br />
<em>Generally, the address information in OpenStreetMap is represented
using multiple properties such as addr:housenumber, addr:street, and
addr:postcode.</em></td>
<td style="text-align: left;">tor: {OSM ID}ParkAddress</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">contact:Address</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}ParkAddress</td>
<td style="text-align: left;">contact:hasStreetNumber</td>
<td style="text-align: left;">“{addr:housenumber}”</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}ParkAddress</td>
<td style="text-align: left;">contact:hasStreet (where appropriate, the
information in addr:street is separated and represented in more detail
using additional properties from the contact ontology e.g.,
contact:hasStreetType)</td>
<td style="text-align: left;">“{addr:street}”</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}ParkAddress</td>
<td style="text-align: left;">contact:hasPostalCode</td>
<td style="text-align: left;">“{addr:postcode}”</td>
</tr>
<tr>
<td rowspan="2" style="text-align: left;"><p>Operator</p>
<p>Name of the operator in charge of operating the entity. The name is
converted to CamelCase when it is used as an IRI.</p></td>
<td style="text-align: left;">tor:{operator}Operator</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">cdt:Organization</td>
</tr>
<tr>
<td style="text-align: left;">tor:{operator}Operator</td>
<td style="text-align: left;">org:hasSubOrganization</td>
<td style="text-align: left;">tor: {OSM ID}ParkOrg</td>
</tr>
<tr>
<td rowspan="5" style="text-align: left;"><p>Surface Area</p>
<p>The surface area information of the feature is not directly provided
in the dataset but was calculated using the geospatial
geometries.</p></td>
<td style="text-align: left;">tor: {OSM ID}ParkArea</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">cityunits:Area</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID} ParkSite</td>
<td style="text-align: left;">cityunits:hasArea</td>
<td style="text-align: left;">tor: {OSM ID}ParkArea</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}ParkArea</td>
<td style="text-align: left;">i72:hasValue</td>
<td style="text-align: left;">tor: {OSM ID}ParkAreaMeasure</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}ParkAreaMeasure</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">i72:Measure</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}ParkAreaMeasure</td>
<td style="text-align: left;">21972:numerical_value</td>
<td style="text-align: left;">“{surface area}”</td>
</tr>
</tbody>
</table>

| **Synthetic Park Capacity Data (RDF generation done using Parks.py)** |  |  |
|:---|:---|:---|
| **Subject** | **Property** | **Object** |
| tor: {OSM ID}ParkService | res:capacityInUse | tor: {OSM ID}ParkServiceCapacityUse |
| tor: {OSM ID}ParkServiceCapacityUse | rdf:type | hp:RecreationAreaPopulationRatio |
| tor: {OSM ID}ParkServiceCapacityUse | i72:hasValue | tor: {OSM ID}ParkServiceCapacityUseMeasure |
| tor: {OSM ID}ParkServiceCapacityUseMeasure | i72:hasNumericalValue | {surface area} / 8855 |
| tor: {OSM ID}ParkServiceCapacityUseMeasure | i72:hasUnit | hp:square_metre_per_person |
| tor: {OSM ID}ParkService | res:hasCapacity | tor: {OSM ID}ParkServiceCapacity |
| tor: {OSM ID}ParkServiceCapacity | rdf:type | hp:MinRecreationAreaPopulationRatio |
| tor: {OSM ID}ParkServiceCapacity | i72:hasValue | tor: {OSM ID}ParkServiceCapacityMeasure |
| tor: {OSM ID}ParkServiceCapacityMeasure | i72:hasNumericalValue | 20 |
| tor: {OSM ID}ParkServiceCapacityMeasure | i72:hasUnit | hp:square_metre_per_person |
| tor: {OSM ID}ParkService | res:hasAvailableCapacity | tor: {OSM ID}ParkServiceCapacityAvail |
| tor: {OSM ID}ParkServiceCapacityAvail | rdf:type | hp:AvailableRecreationAreaPopulationRatio |
| tor: {OSM ID}ParkServiceCapacityAvail | i72:hasValue | tor: {OSM ID}ParkServiceCapacityAvailMeasure |
| tor: {OSM ID}ParkServiceCapacityAvailMeasure | i72:hasNumericalValue | {capacity - capacity use} |
| tor: {OSM ID}ParkServiceCapacityAvailMeasure | i72:hasUnit | hp:square_metre_per_person |

Implementation of Parks Related Data in Mapping TTL

**Scripts:** Parks2.py

**URI strategy**

- **Park (Organization):**

  - tor: {OSM ID}ParkOrg

- **Park Site:**

  - tor: {OSM ID} ParkSite

- **Park Site Location:**

  - tor: {OSM ID} ParkSiteLoc

- **Park Service:**

  - tor: {OSM ID}ParkService

- **Park Capacity:**

  - tor: {OSM ID}ParkServiceCapacity

- **Park Capacity Use:**

  - tor: {OSM ID}ParkServiceCapacityUse

- **Park Capacity Available:**

  - tor: {OSM ID}ParkServiceCapacityAvail

**Inputs**

1.  **OSM Toronto Park Data (Parks2.py)**

    - Dataset links

      - parks.geojson (data from OSM can be extracted using Overpass
        Turbo (<https://overpass-turbo.eu/>) by typing in “leisure=park
        in Toronto” in the wizard)

    - Data can be downloaded and used as a .geojson file

**Outputs**

- Parks.ttl (Parks2.py)  
  Contains: OSM park data for Toronto and their locations.

- ParksCapacity.ttl (ParksCapacity.py)  
  Contains: Synthetic information about park capacities

**Step-by-step process for Parks2.py**

**Step 1 - Initialize RDF graphs and namespaces**  
Two RDF graphs are created:

- g contains all triples for the Parks.ttl output file

- g2 contains all triples for the ParksCapacity.ttl output file

**Step 2 – Import geoJSON dataset using the json Python package**  
The data from the park dataset is contained in the “amenity” variable.

**Step 3 - RDF triples are created using each feature in the data**  
The data in stored in the amenity variable is iterated feature by
feature and RDF triples are generated according to the mapping
specifications outlined in the tables found earlier in this document.
Values for the triples are extracted from the corresponding property in
the data.

**Note:** For the catchment area calculation, the geometry of the park
is temporarily converted to EPSG:32617 format as this standard uses
metres as the unit of measure which is needed in order to calculate the
800m buffered area for the catchment area. The buffered area is then
converted back to EPSG:4326 (WGS84) to be consistent with the other
geospatial data in the City Digital Twin.

**Step 4 - Serialize TTL**  
The graph g is written to Parks.ttl and g2 is written to
ParksCapacity.ttl.
