Public Schools Documentation

Relevant Python Scripts:

- [PublicSchools.py](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/PublicSchools.py):
  generates the RDF data related to public schools in Toronto.

  - Dataset links

    - <https://data.ontario.ca/en/dataset/ontario-public-school-contact-information>

- [PublicSchoolsCapacity.py](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/PublicSchoolsCapacity.py):
  generates the RDF data for public school capacities.

  - Dataset links

    - <https://data.ontario.ca/en/dataset/ontario-public-schools-enrolment>
      (used as capacity use data)

    - enrolment_by_school_2324_en_fakeadded.xlsx (synthetic capacity
      data)

This is the ontological representation of Toronto’s public school data
from the Ontario Data Catalogue. Services provided by public schools are
represented as instances of the tor:TorSchoolService class while the
capacity data is derived from the public school enrollment dataset and
the synthetic capacity dataset used to supplement it.

This section summarizes how the school related datasets are mapped into
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

<img src="/media/image.png" style="width:6.5in;height:5.38542in" />

<table>
<colgroup>
<col style="width: 18%" />
<col style="width: 16%" />
<col style="width: 20%" />
<col style="width: 44%" />
</colgroup>
<thead>
<tr>
<th colspan="4" style="text-align: left;"><strong>Data Provided By the
Public School Dataset (RDF generation done using
PublicSchools.py)</strong></th>
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
<td rowspan="5" style="text-align: left;">School Number</td>
<td style="text-align: left;">tor:{School Number}School</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">cdt:ElementarySchool or
cdt:SecondarySchool, as indicated by the "School Level" column</td>
</tr>
<tr>
<td style="text-align: left;">tor:{School Number}School</td>
<td style="text-align: left;">cdt:providesService</td>
<td style="text-align: left;">tor:{School Number}SchoolService</td>
</tr>
<tr>
<td style="text-align: left;">tor:{School Number}SchoolService</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">tor:TorSchoolService</td>
</tr>
<tr>
<td style="text-align: left;">tor:{School Number}School</td>
<td style="text-align: left;">genprop:hasIdentifier</td>
<td style="text-align: left;">"{School Number}"</td>
</tr>
<tr>
<td style="text-align: left;">tor:{School Number}School</td>
<td style="text-align: left;">genprop:hasName</td>
<td style="text-align: left;">"{School Name}"</td>
</tr>
<tr>
<td rowspan="4" style="text-align: left;">Board Number</td>
<td style="text-align: left;">tor:{Board Number}SchoolBoard</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">cdt:Organization</td>
</tr>
<tr>
<td style="text-align: left;">tor:{Board Number}SchoolBoard</td>
<td style="text-align: left;">org:hasSubOrganization</td>
<td style="text-align: left;">tor:{School Number}School</td>
</tr>
<tr>
<td style="text-align: left;">tor:{Board Number}SchoolBoard</td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">tor:{Board Number}SchoolBoard</td>
<td style="text-align: left;">genprop:hasIdentifier</td>
<td style="text-align: left;">"{Board Number}"</td>
</tr>
<tr>
<td rowspan="2" style="text-align: left;">Board Name</td>
<td style="text-align: left;">tor:{Board Number}SchoolBoard</td>
<td style="text-align: left;">genprop:hasName</td>
<td style="text-align: left;">"{Board Name}"</td>
</tr>
<tr>
<td style="text-align: left;">tor:{School Number}SchoolService</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">hpcdm:ElementarySchoolService or<br />
hpcdm:SecondarySchoolService as appropriate (based on the "School Level"
column)</td>
</tr>
<tr>
<td rowspan="5" style="text-align: left;"><em>calculated value</em></td>
<td style="text-align: left;">tor:{School Number}School</td>
<td style="text-align: left;">org:hasSite</td>
<td style="text-align: left;">tor:{School Number}SchoolSite</td>
</tr>
<tr>
<td style="text-align: left;">tor:{School Number}SchoolService</td>
<td style="text-align: left;">hp:providedFromSite</td>
<td style="text-align: left;">tor:{School Number}SchoolSite</td>
</tr>
<tr>
<td style="text-align: left;">tor:{School Number}SchoolSite</td>
<td style="text-align: left;">loc:hasLocation</td>
<td style="text-align: left;">tor:{School Number}SchoolSiteLocation</td>
</tr>
<tr>
<td style="text-align: left;">tor:{School Number}SchoolSiteLocation</td>
<td style="text-align: left;">geo:asWKT</td>
<td style="text-align: left;">{calculated coordinates based on
address}</td>
</tr>
<tr>
<td style="text-align: left;">tor:{School Number}SchoolSite</td>
<td style="text-align: left;">org:siteAddress</td>
<td style="text-align: left;">tor:{School Number}SchoolAddress</td>
</tr>
<tr>
<td rowspan="3" style="text-align: left;">Street</td>
<td style="text-align: left;">tor:{School Number}SchoolAddress</td>
<td style="text-align: left;">rdf:type</td>
<td style="text-align: left;">contact:Address</td>
</tr>
<tr>
<td style="text-align: left;">tor:{School Number}SchoolAddress</td>
<td style="text-align: left;">contact:hasStreetNumber</td>
<td style="text-align: left;">Needs to be extracted from {Street}</td>
</tr>
<tr>
<td style="text-align: left;">tor:{School Number}SchoolAddress</td>
<td style="text-align: left;">contact:hasStreet (where appropriate, the
information in addr:street is separated and represented in more detail
using additional properties from the contact ontology e.g.,
contact:hasStreetType)</td>
<td style="text-align: left;">Needs to be extracted from {Street}</td>
</tr>
<tr>
<td style="text-align: left;">Postal Code</td>
<td style="text-align: left;">tor:{School Number}SchoolAddress</td>
<td style="text-align: left;">contact:hasPostalCode</td>
<td style="text-align: left;">"{Postal Code}"</td>
</tr>
</tbody>
</table>

| **Data Provided By the Public School Enrollment Dataset and Synthetic Capacities Dataset (RDF generation done using PublicSchoolsCapacity.py)** |  |  |  |  |
|:---|:---|:---|:---|:---|
| **Field Name** | **Subject** | **Property** | **Object** | **Notes** |
| School Number | tor:{School Number}SchoolService | res:capacityInUse | tor:{School Number}SchoolServiceCapacityUse | Integration with school contact/location data |
|  | tor:{School Number}SchoolServiceCapacityUse | rdf:type | hp:SchoolEnrollmentSize |  |
|  | tor:{School Number}SchoolServiceCapacityUse | i72:hasValue | tor:{School Number}SchoolServiceCapacityUseMeasure |  |
| Enrolment | tor:{School Number}SchoolServiceCapacityUseMeasure | i72:hasNumericalValue | "{Enrolment}" |  |
|  | tor:{School Number}SchoolServiceCapacityUseMeasure | i72:hasUnit | i72:population_cardinality_unit |  |
| {time interval} | tor:{School Number}SchoolServiceCapacityUseMeasure | change:existsAt | tor:{time interval camelcase}Interval | Extracted from metadata: September 1, 2023 - August 31, 2024 |
|  | tor:{time interval camelcase}Interval | time:hasBeginning | tor:{time interval camelcase}BeginningTimeInstant |  |
|  | tor:{time interval camelcase}BeginningTimeInstant | time:inXSDDateTimeStamp | {start of time interval converted to xsd datetime stamp} |  |
|  | tor:{time interval camelcase}Interval | time:hasEnd | tor:{time interval camelcase}EndTimeInstant |  |
|  | tor:{time interval camelcase}EndTimeInstant | time:inXSDDateTimeStamp | {end of time interval converted to xsd datetime stamp} |  |
| Fake Capacity | tor:{School Number}SchoolService | res:hasCapacity | tor:{School Number}SchoolServiceCapacity |  |
|  | tor:{School Number}SchoolServiceCapacity | rdf:type | hp:SchoolEnrollmentSpaces |  |
|  | tor:{School Number}SchoolServiceCapacity | i72:hasValue | tor:{School Number}SchoolServiceCapacityMeasure |  |
|  | tor:{School Number}SchoolServiceCapacityMeasure | i72:hasNumericalValue | {Fake Capacity} |  |
|  | tor:{School Number}SchoolServiceCapacityMeasure | i72:haUnit | i72:population_cardinality_unit |  |
|  | tor:{School Number}SchoolService | res:hasAvailableCapacity | tor:{School Number}SchoolServiceCapacityAvail |  |
|  | tor:{School Number}SchoolServiceCapacityAvail | rdf:type | hp:SchoolAvailableEnrollmentSpaces |  |
|  | tor:{School Number}SchoolServiceCapacityAvail | i72:hasValue | tor:{School Number}SchoolServiceCapacityAvailMeasure |  |
|  | tor:{School Number}SchoolServiceCapacityAvailMeasure | i72:hasNumericalValue | {capacity - capacity use} |  |
|  | tor:{School Number}SchoolServiceCapacityAvailMeasure | i72:haUnit | i72:population_cardinality_unit |  |

Implementation of Public School Related Data in Mapping TTL

**Scripts:** PublicSchools.py

**URI strategy**

- **School:**

  - tor:{School Number}School

- **School Site:**

  - tor:{School Number}SchoolSite

- **School Site Location:**

  - tor:{School Number}SchoolSiteLocation

- **School Service:**

  - tor:{School Number}SchoolService

**Scripts:** PublicSchoolsCapacity.py

**URI strategy**

- **School Capacity:**

  - tor:{School Number}SchoolServiceCapacity

- **School Capacity Use:**

  - tor:{School Number}SchoolServiceCapacityUse

- **School Capacity Available:**

  - tor:{School Number}SchoolServiceCapacityAvail

**Inputs**

1.  **Public School Data (PublicSchools.py)**

    - Dataset links

      - <https://data.ontario.ca/en/dataset/ontario-public-school-contact-information>

    - Data can be downloaded and used as a .xlsx file

2.  **Public School Capacity Data (PublicSchoolsCapacity.py)**

    - Dataset links

      - enrolment_by_school_2324_en_fakeadded.xlsx

    - This dataset additionally contains the enrollment data from the
      Ontario Data Catalogue so that dataset does not need to be
      imported separately.

**Outputs**

- PublicSchools.ttl (PublicSchools.py)  
  Contains: Public school data for Toronto and their locations.

- PublicSchoolsCapacity.ttl (PublicSchoolsCapacity.py)  
  Contains: Information about public school capacities using enrollment
  data and synthetic data.

**Step-by-step process for PublicSchools.py**

**Step 1 - Initialize RDF graphs and namespaces**  
One RDF graph is created:

- g contains all triples for the PublicSchools.ttl output file

**Step 2 – Import data from the xlsx file using the pandas Python
package**  
The data from the public schools dataset is contained in the “df”
dataframe.

**Step 3 - RDF triples are created using each feature in the data**  
The data in stored in the df dataframe is iterated row by row and RDF
triples are generated according to the mapping specifications outlined
in the tables found earlier in this document. Values for the triples are
extracted from the corresponding column in the data.

**Note:** Address parsing is required for extracting the address
components from the raw data. The script utilizes ArcGIS’ geocoder that
is available for use in Python using the geopy package (from
geopy.geocoders import ArcGIS).

**Step 4 - Serialize TTL**  
The graph g is written to PublicSchools.ttl.

**Step-by-step process for PublicSchoolsCapacity.py**

**Step 1 - Initialize RDF graphs and namespaces**  
One RDF graph is created:

- g contains all triples for the PublicSchoolsCapacity.ttl output file

**Step 2 – Import data from the xlsx file using the pandas Python
package**  
The data from the public schools enrollment/capacity dataset is
contained in the “df” dataframe.

**Step 3 - RDF triples are created using each feature in the data**  
The data in stored in the df dataframe is iterated row by row and RDF
triples are generated according to the mapping specifications outlined
in the tables found earlier in this document. Values for the triples are
extracted from the corresponding column in the data.

**Step 4 - Serialize TTL**  
The graph g is written to PublicSchoolsCapacity.ttl.
