Hospital Documentation

Relevant Python Scripts:

- [Hospital.py](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/Hospital.py):
  generates the RDF data related to hospitals in Toronto.

  - Dataset links

    - hospital.geojson (data from OSM can be extracted using Overpass
      Turbo (<https://overpass-turbo.eu/>) by typing in
      “amenity=hospital in Toronto” in the wizard)

- [HospitalCapacity.py](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/HospitalCapacity.py):
  generates the RDF data for hospital capacity related information.

  - Dataset links

    - <https://www.cihi.ca/en/access-data-and-reports/indicator-library/download-indicator-data>

This is the ontological representation of Toronto’s hospital data from
OpenStreetMap. Hospitals are represented as instances of the
cdt:Hospital class while their services are represented as instances of
the tor:TorHospitalService class and limited data from the Canadian
Institute for Health Information is used for the capacity values.

This section summarizes how the hospital related datasets are mapped
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

<img src="/media/image.png" style="width:6.5in;height:5.38542in" />

<table>
<colgroup>
<col style="width: 16%" />
<col style="width: 30%" />
<col style="width: 22%" />
<col style="width: 30%" />
</colgroup>
<thead>
<tr>
<th colspan="4" style="text-align: left;"><strong>Data Provided By the
OSM Hospital Dataset (RDF generation done using
Hospital.py)</strong></th>
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
<td style="text-align: left;">Hospital</td>
<td style="text-align: left;">tor: {OSM ID}Hospital</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">cdt:Hospital</td>
</tr>
<tr>
<td style="text-align: left;">emergency</td>
<td style="text-align: left;">tor: {OSM
ID}HospitalEmergencyDepartment</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">org:OrganizationalUnit</td>
</tr>
<tr>
<td rowspan="4" style="text-align: left;">Indicates whether the hospital
provides emergency services</td>
<td style="text-align: left;">tor: {OSM ID}Hospital</td>
<td style="text-align: left;">org:hasUnit</td>
<td style="text-align: left;">tor: {OSM
ID}HospitalEmergencyDepartment</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}HospitalEmergencyService</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">hp:HospitalEmergencyService</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}Hospital</td>
<td style="text-align: left;">cdt:providesService</td>
<td style="text-align: left;">tor: {OSM ID}HospitalService</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM
ID}HospitalEmergencyDepartment</td>
<td style="text-align: left;">cdt:providesService</td>
<td style="text-align: left;">tor: {OSM ID}HospitalEmergencyService</td>
</tr>
<tr>
<td rowspan="6" style="text-align: left;">geometry</td>
<td style="text-align: left;">cdt: {OSM ID} Hospital</td>
<td style="text-align: left;">org:hasSite</td>
<td style="text-align: left;">tor: {OSM ID} HospitalSite</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}HospitalService</td>
<td style="text-align: left;">hpcdm:providedFromSite</td>
<td style="text-align: left;">tor: {OSM ID} HospitalSite</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}HospitalService</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">Tor:TorHospitalService</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID} HospitalSite</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">cdt:Site</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID} HospitalSite</td>
<td style="text-align: left;">loc:hasLocation</td>
<td style="text-align: left;">tor: {OSM ID} HospitalSiteLocation</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID} HospitalSiteLocation</td>
<td style="text-align: left;">geo:asWKT</td>
<td style="text-align: left;">“{geometry}” (the geometry here is
converted to WKT format)</td>
</tr>
<tr>
<td style="text-align: left;">id</td>
<td style="text-align: left;">tor: {OSM ID}Hospital</td>
<td style="text-align: left;">genprop:hasIdentifier</td>
<td style="text-align: left;">“{OSM ID}”</td>
</tr>
<tr>
<td style="text-align: left;">name</td>
<td style="text-align: left;">tor: {OSM ID}Hospital</td>
<td style="text-align: left;">genprop:hasName</td>
<td style="text-align: left;">“{name}”</td>
</tr>
<tr>
<td rowspan="6" style="text-align: left;">Address<br />
<br />
<em>Generally, the address information in OpenStreetMap is represented
using multiple properties such as addr:housenumber, addr:street, and
addr:postcode.</em></td>
<td style="text-align: left;">tor: {OSM ID}HospitalAddress</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">contact:Address</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}Hospital</td>
<td style="text-align: left;">org_city:orgAddress</td>
<td style="text-align: left;">tor: {OSM ID}HospitalAddress</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID} HospitalSite</td>
<td style="text-align: left;">org:siteAddress</td>
<td style="text-align: left;">tor: {OSM ID}HospitalAddress</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}HospitalAddress</td>
<td style="text-align: left;">contact:hasStreetNumber</td>
<td style="text-align: left;">“{addr:housenumber}”</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}HospitalAddress</td>
<td style="text-align: left;">contact:hasStreet (where appropriate, the
information in addr:street is separated and represented in more detail
using additional properties from the contact ontology e.g.,
contact:hasStreetType)</td>
<td style="text-align: left;">“{addr:street}”</td>
</tr>
<tr>
<td style="text-align: left;">tor: {OSM ID}HospitalAddress</td>
<td style="text-align: left;">contact:hasPostalCode</td>
<td style="text-align: left;">“{addr:postcode}”</td>
</tr>
<tr>
<td style="text-align: left;">operator</td>
<td style="text-align: left;">tor:{operator}</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">cdt:Organization</td>
</tr>
<tr>
<td style="text-align: left;">Name of the operator in charge of
operating the entity. The name is converted to CamelCase when it is used
as an IRI.</td>
<td style="text-align: left;">tor:{operator}</td>
<td style="text-align: left;">org:hasSubOrganization</td>
<td style="text-align: left;">tor: {OSM ID}Hospital</td>
</tr>
</tbody>
</table>

| **Data Provided By the CIHI Dataset (RDF generation done using HospitalCapacity.py)** |  |  |  |  |
|:---|:---|:---|:---|:---|
| **Field Name** | **Subject** | **Property** | **Object** | **Notes** |
|  | tor: {OSM ID}HospitalService | res:capacityInUse | tor: {OSM ID}HospitalCapacityUse | Manually aligned to existing hospital IRIs |
|  | tor: {OSM ID}HospitalCapacityUse | rdf:type | hp:HospitalBedPopulationRatio |  |
|  | tor: {OSM ID}HospitalCapacityUse | i72:hasValue | tor: {OSM ID}HospitalCapacityUseMeasure |  |
| Metric value | tor: {OSM ID}HospitalCapacityUseMeasure | i72:hasNumericalValue | "{Metric value}" |  |
|  | tor: {OSM ID}HospitalCapacityUseMeasure | i72:hasUnit | hp:avg_inpatients_daily_per_bed |  |
|  | tor: {OSM ID}HospitalService | res:hasCapacity | tor: {OSM ID}HospitalCapacity |  |
|  | tor: {OSM ID}HospitalCapacity | rdf:type | hp:MinHospitalBedPopulationRatio |  |
|  | tor: {OSM ID}HospitalCapacity | i72:hasValue | tor: {OSM ID}HospitalCapacityMeasure |  |
|  | tor: {OSM ID}HospitalCapacityMeasure | i72:hasNumericalValue | 1 | set maximum |
|  | tor: {OSM ID}HospitalCapacityMeasure | i72:hasUnit | hp:avg_inpatients_daily_per_bed |  |
|  | tor: {OSM ID}HospitalService | res:hasAvailableCapacity | tor: {OSM ID}HospitalCapacityAvail |  |
|  | tor: {OSM ID}HospitalCapacityAvail | rdf:type | hp: AvailableHospitalBedPopulationRatio |  |
|  | tor: {OSM ID}HospitalCapacityAvail | i72:hasValue | tor: {OSM ID}HospitalCapacityAvailMeasure |  |
|  | tor: {OSM ID}HospitalCapacityAvailMeasure | i72:hasNumericalValue | {1 – Metric value} |  |
|  | tor: {OSM ID}HospitalCapacityAvailMeasure | i72:hasUnit | hp:avg_inpatients_daily_per_bed |  |

Implementation of Hospital Related Data in Mapping TTL

**Scripts:** Hospital.py

**URI strategy**

- **Hospital:**

  - tor: {OSM ID}Hospital

- **Hospital Site:**

  - tor: {OSM ID} HospitalSite

- **Hospital Site Location:**

  - tor: {OSM ID}HospitalSiteLoc

- **Hospital Service:**

  - tor: {OSM ID}HospitalService

**Scripts:** HospitalCapacity.py

**URI strategy**

- **Hospital Capacity:**

  - tor: {OSM ID}HospitalServiceCapacity

- **Hospital Capacity Use:**

  - tor: {OSM ID}HospitalServiceCapacityUse

- **Hospital Capacity Available:**

  - tor: {OSM ID}HospitalServiceCapacityAvail

**Inputs**

1.  **OSM Toronto Hospital Data (Hospital.py)**

    - Dataset links

      - hospital.geojson (data from OSM can be extracted using Overpass
        Turbo (<https://overpass-turbo.eu/>) by typing in
        “amenity=hospital in Toronto” in the wizard)

    - Data can be downloaded and used as a .geojson file

2.  **CIHI Hospital Capacity Data (HospitalCapacity.py)**

    - Dataset links

      - <https://www.cihi.ca/en/access-data-and-reports/indicator-library/download-indicator-data>

    - Data is downloaded and used as an .xlsx file

**Outputs**

- Hospital.ttl (Hospital.py)  
  Contains: OSM hospital data for Toronto and their locations.

- HospitalCapacity.ttl (HospitalCapacity.py)  
  Contains: CIHI information about hospital capacities

**Step-by-step process for Hospital.py**

**Step 1 - Initialize RDF graphs and namespaces**  
One RDF graph is created:

- g contains all triples for the Hospital.ttl output file

**Step 2 – Import geoJSON dataset using the json Python package**  
The data from the hospital dataset is contained in the “amenity”
variable.

**Step 3 - RDF triples are created using each feature in the data**  
The data in stored in the amenity variable is iterated feature by
feature and RDF triples are generated according to the mapping
specifications outlined in the tables found earlier in this document.
Values for the triples are extracted from the corresponding property in
the data.

**Step 4 - Serialize TTL**  
The graph g is written to Hospital.ttl.

**Step-by-step process for HospitalCapacity.py**

**Step 1 - Initialize RDF graphs and namespaces**  
One RDF graph is created:

- g contains all triples for the HospitalCapacity.ttl output file

**Step 2 – Import xlsx dataset using the pandas Python package**  
The data from the hospital capacity dataset is contained in the “df”
dataframe.

**Step 3 - RDF triples are created using each feature in the data**  
The data in stored in the df dataframe is iterated row by row and RDF
triples are generated according to the mapping specifications outlined
in the tables found earlier in this document. Values for the triples are
extracted from the corresponding column in the data.

**Note:** The hospital capacity data is very limited and most hospitals
in Hospital.ttl don’t have capacity information.

**Step 4 - Serialize TTL**  
The graph g is written to HospitalCapacity.ttl.
