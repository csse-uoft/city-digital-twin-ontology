# Ontario Road Network

[The Ontario Road Network (ORN) dataset](https://geohub.lio.gov.on.ca/datasets/mnrf::ontario-road-network-orn-road-net-element/about) represents the provincial road infrastructure and is segmented at real-world intersections or junctions. The primary dataset consists of a shapefile (ORN_ROAD_NET_ELEMENT.shp) that describes road geometries and includes fields such as OGF_ID (a unique identifier for each road element), FROM_JCT, and TO_JCT, which indicate the junctions that bound each segment, and more. These junction references establish a topological connection between road elements. Supplementary CSV files (e.g., ORN_ROAD_CLASS.csv, ORN_SPEED_LIMIT.csv) enrich the dataset with additional attributes, including road names, speed limits, lane counts, and more. The following is an example of data in the shp file for a road element:

FROM_JCT:1500091661 TO_JCT:1500045335

LENGTH:254.258 ACCURACY:3.0

NID:9bed6561cdbd438590abec7bf592d722 DIRECTION:Both

EXIT_NUM:18 ELEM_TYPE:ROAD ELEMENT

TOLL_ROAD:Yes ACQTECH:VECTOR DATA

CREDATE:20020401000000 REVDATE:None

GEO_UPDATE_DT:None EFF_DATE:20090123155815

The above example defines, a road element identified by OGF_ID = 1509876543, that runs from junction 1501234567 to junction 1507654321, with a total length of 254.258 meters, with a positional accuracy of 3.0 meters, and a unique national identifier of 9bed6561cdbd438590abec7bf592d722. It is a toll road that was created using vector data, it has traffic flowing in both directions, an exit number of 18, a creation date of April 1<sup>st</sup> 2002, a revision and geometry update date that is unknown, and a record creation date of January 23<sup>rd</sup> 2009 (15 hours, 58 minutes, and 15 seconds). More information about these attributes is provided below.

Each road network corresponds to an instance of the RoadLink class in the ISO/IEC 5087-3 ontology. Each RoadLink begins and ends at a TransportNode, which corresponds to a Junction in the ontology

Thus, in mapping the road network data to the City Digital Twin:

- **ORN road net elements** → transnet:RoadLink (subclass of TravelledWayLink)

- **ORN junctions** → transnet:Junction (subclass of TransportNode)

- A group of RoadLinks sharing the same street name → transnet:Road

The data was also filtered around only Toronto roads using the Toronto Bound Filter:

lat_min: 43.5810, lat_max: 43.8555, lon_min: -79.6393, lon_max: -79.1152

The following is a list of namespace prefixes used in the mappings and ontology definitions that follow:

- geo: <http://www.opengis.net/ont/geosparql>\#

- transnet: <https://standards.iso.org/isoiec/5087/3/ed1/en/ontology/TransportaionNetwork/>

- transinfras: <https://standards.iso.org/isoiec/5087/2/ed1/en/ontology/TransportationInfrastructure/>

- loc: <https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/>

- partwhole: <https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Mereology/>

- cityunits: <https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/CityUnits/>

- cdt: <http://ontology.eil.utoronto.ca/CDT>\#

- rdfs: <http://www.w3.org/2000/01/rdf-schema>\#

- i72: <http://ontology.eil.utoronto.ca/5087/2/iso21972/>

- genprop: <https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/>

- rdf: [http://www.w3.org/1999/02/22-rdf-syntax-ns#](http://www.w3.org/1999/02/22-rdf-syntax-ns)

- contact: <https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Contact/>

- code: <https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Code/>

- infras: <https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Infrastructure/>

- road: <https://standards.iso.org/iso-iec/5087/-3/ed-1/en/ontology/RoadNetwork>

- org_city: <https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Organization/>

- xsd: [http://www.w3.org/2001/XMLSchema#](http://www.w3.org/2001/XMLSchema)

- hp: http://ontology.eil.utoronto.ca/HPCDM#

- res: <https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Resource/>

- orn: http://ontology.eil.toronto.ca/Ontario/OMNR/ORNELEM#
- 

![Figure 1](https://github.com/csse-uoft/city-digital-twin-ontology/blob/ce2d59b4f229e20b29a5b11c56fb5b8b562dbefd/Housing%20Potential%20Python/Housing%20Potential%20Diagrams/Figure%201%20Diagram%20of%20the%20Transportation%20Network%20Pattern.png)

*<u>Figure 1: Diagram of the Transportation Network Pattern</u>*

## Junction

Junctions are an instance of a subclass/specialization of transnet:Junction and are a subclass of TransportNode. These entities connect travellers from one TravelledWayLink to another, serving a connection between one or more RoadLinks. They are uniquely identified using ORN-provided IDs. Geospatial coordinates are linked using geo:Geometry pointing to a geo:asWKT. Each Junction participates in one or more ingress and egress relationships with RoadLinks, ensuring accurate topological representation of the network.

Information regarding the junctions in the dataset specified in the ORN_JUNCTIONS.csv file.

**Note:** All the CSV files had a data tag ORN_ROAD_NET_ELEMENT_ID, an Integer representing a system-generated identifier unique at the application level. This identifier corresponds to the OGF_ID in the shapefile, enabling consistent linkage between data in the CSV files and in the shapefile.

**The following properties are for associated with instances of the cdt:Junction class, which is a subclass of the Junction class in the TransportationNetwork ontology.**

**ORN_Junction.csv:** A unique national identifier assigned to a road net element, junction and selected event data such as Toll Point, Blocked Passage and Structure which are required to support the National Road Network (NRN).

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr class="header">
<th colspan="5">Data Provided by ORN_JUNCTION.csv</th>
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
<td rowspan="2">JUNCTION_ID</td>
<td>orn:Junction_ {JUNCTION_ID}</td>
<td>genprop:hasIdentifier</td>
<td>{JUNCTION_ID}</td>
<td rowspan="2">System-generated identifier, unique at the application level.</td>
</tr>
<tr class="odd">
<td>orn:Junction_ {JUNCTION_ID}</td>
<td>rdf:type</td>
<td>cdt:Junction</td>
</tr>
<tr class="even">
<td>LATITUDE_DECIMAL_DEGREES</td>
<td rowspan="2">orn:Junction_ {JUNCTION_ID}</td>
<td rowspan="2">loc:hasLocation</td>
<td rowspan="2">loc:junction_loc_{JUNCTION_ID}</td>
<td rowspan="4"><p>The latitude in decimal degrees.</p>
<p>The longitude in negative decimal degrees.</p>
<p>For each Junction individual, a new geo:Geometry individual is created and linked via</p>
<p>loc:hasLocation.</p>
<p>This geometry is defined with the geo:asWKT property using the LATITUDE_DECIMAL_DEGREES and LONGITUDE_DECIMAL_DEGREES with the POINT (lon lat) format.</p></td>
</tr>
<tr class="odd">
<td rowspan="3">LONGITUDE_DECIMAL_DEGREES</td>
</tr>
<tr class="even">
<td>loc:junction_loc_{JUNCTION_ID}</td>
<td>rdf:type</td>
<td>loc:Location</td>
</tr>
<tr class="odd">
<td>loc:junction_loc_{JUNCTION_ID}</td>
<td>geo:asWKT</td>
<td>POINT ({LONGITUDE_ DECIMAL_ DEGREES } { LATITUDE_ DECIMAL_ DEGREES })</td>
</tr>
<tr class="even">
<td rowspan="4">JUNCTION_TYPE</td>
<td>orn:Junction_{JUNCTION_ID}</td>
<td>cdt:hasJunctionType</td>
<td>orn:junction_ type_{JUNCTION_ID}</td>
<td rowspan="4"><p>The classification of a junction is based on the valency of the junction. The number of road elements or ferry connections joining at a junction is termed the valency of a junction.</p>
<p></td>
</tr>
<tr class="odd">
<td>orn:junction_ type_{JUNCTION_ID}</td>
<td>rdf:type</td>
<td>cdt:JunctionType</td>
</tr>
<tr class="even">
<td>orn:junction_ type_{JUNCTION_ID}</td>
<td>code:Code</td>
<td>code:junction Type_Code_ {JUNCTION_ID}</td>
</tr>
<tr class="odd">
<td>code:junction Type_Code_ {JUNCTION_ID}</td>
<td>genprop:hasName</td>
<td>{JUNCTION_ TYPE}</td>
</tr>
<tr class="even">
<td>EXIT_NUMBER</td>
<td>orn:Junction_{JUNCTION_ID}</td>
<td>cdt:exitNumber</td>
<td>{EXIT_NUMBER}</td>
<td>The number of an exit on or off a freeway, expressway or highway, assigned by an administrating body and is represented by a valid number or character</td>
</tr>
<tr class="odd">
<td>NATIONAL_UUID</td>
<td>orn:Junction_{JUNCTION_ID}</td>
<td>cdt:nationUUID</td>
<td>{NATIONAL_ UUID}</td>
<td>A unique national identifier assigned to a road net element, junction and selected event data such as Toll Point, Blocked Passage and Structure which are required to support the National Road Network (NRN).</td>
</tr>
<tr class="even">
<td>EFFECTIVE_ DATETIME</td>
<td>orn:Junction_{JUNCTION_ID}</td>
<td>cdt:effectiveDate</td>
<td>{EFFECTIVE_ DATETIME}</td>
<td>Date/time the record was created or last modified in the source database.</td>
</tr>
</tbody>
</table>

*<u>Table 1: Mapping ORN_JUNCTION.csv to City Digital Twin</u>*

**NOTE:** The TO_JCT and FROM_JCT; are both junction IDs that are within the ORN_JUNCTION.csv files. So, using the ID, we can find the URI for the junction that has already been created. When the junction entities are found, then we use the properties above on the corresponding RoadLinks.

| Data Provided by ORN_ROAD_NET_ELEMENT.shp: |                             |                  |                        |                                                                |
|--------------------------------------------|-----------------------------|------------------|------------------------|----------------------------------------------------------------|
| **Field Name**                             | **Subject**                 | **Property**     | **Object**             | **Notes**                                                      |
| TO_JCT                                     | orn:Junction\_{JUNCTION_ID} | transnet:ingress | orn:roadLink\_{OGF_ID} | The end junction for a road element or ferry connection.       |
| FROM_JCT                                   | orn:Junction\_{JUNCTION_ID} | transnet:egress  | orn:roadLink\_{OGF_ID} | The beginning junction for a road element or ferry connection. |

*<u>Table 2: Mapping ORN_ROAD_NET_ELEMENT.shp Junction data to City Digital Twin</u>*

## Road

A Road is modeled as a transinfras:Road, a subclass of TravelledWay, and is defined as a continuous sequence of RoadLinks that share a common entity (e.g., Highway 401, Dundas Street). A single RoadLink may be part of multiple Roads to accommodate overlapping entities. Each Road is linked to a unique designator (road name or number), and its extent is defined by the collective geometry of its constituent RoadLinks.

**ORN_OFFICIAL_STREET_NAME.csv:** An event identifying an official street name and may be associated with a bilingual name.

| Data Provided by ORN_OFFICIAL_STREET_NAME.csv: |             |                 |                    |                                                                                                                                                                                                                                  |
|------------------------------------------------|-------------|-----------------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Field Name**                                 | **Subject** | **Property**    | **Object**         | **Notes**                                                                                                                                                                                                                        |
| FULL_STREET_NAME                               | orn:Road    | genprop:hasName | {FULL_STREET_NAME} | This attribute is derived from the individual street name components where present, namely directional prefix, street type prefix, street name body, street type suffix and directional suffix and is stored in upper case text. |

*<u>Table 3: Mapping ORN_OFFICIAL_STREET_NAME.csv Road data to City Digital Twin</u>*

The ORN data is grouped using the road name to identify the collection of RoadLinks that form a single Road. A unique URI is generated for each Road entity, and all corresponding RoadLinks are created and linked to that Road using the partwhole:hasProperPart property.

## RoadLink

A RoadLink is the fundamental linear segment between two TransportNodes (to and from junctions) and is represented using the transinfras:RoadLink class. Roadlinks are grouped together to form a Road.

FROM_JCT and TO_JCT represent the identifiers for the start and end junctions, respectively.

- In the RDF output, these are used to construct the transnet:forth and transnet:to properties for the corresponding RoadLink.

Each RoadLink instance is generated using the unique OGF_ID as an identifier (e.g. transnet:roadLink_12345). This ensures consistent referencing across other entities such as Roads and Junctions. The OGF_ID also serves as the subject for attaching additional metadata like speed limits, surface type, and geometry (WKT). All supplementary CSV data is joined to the shapefile using this key during pre-processing.

Each RoadLink can be one of three element types: Ferry Connection, Road Element, and Virtual Road. We use the ELEM_TYPE attribute in the shapefile to filter out all the roads that are of type “Virtual Road.”

![Figure 1](https://github.com/csse-uoft/city-digital-twin-ontology/blob/751b7cde9ef9c6a9d22b4ba7dded51282c157016/Housing%20Potential%20Python/Housing%20Potential%20Diagrams/Figure%202%20Descriptions%20of%20road%20element%20types%20from%20the%20ORN%20dataset%2C%20including%20ferry%20connections%2C%20standard%20road%20elements%2C%20and%20virtual%20roads%20used%20for%20addressing%20in%20inaccessible%20areas.png)

*<u>Figure 2: Descriptions of road element types from the ORN dataset, including ferry connections, standard road elements, and virtual roads used for addressing in inaccessible areas</u>*

**All the following properties are for associated with the cdt:RoadLink class, which is a subclass of the RoadLink class in the TransportationInfrastructure ontology.**

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 19%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr class="header">
<th colspan="5">
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
<td rowspan="3">OGF_ID</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>genprop:hasIdentifier</td>
<td>{OGF_ID}</td>
<td rowspan="3">A unique numeric provincial identifier assigned to each object.</td>
</tr>
<tr class="odd">
<td>orn:roadLink_{OGF_ID}</td>
<td>rdf:type</td>
<td>cdt:RoadLink</td>
</tr>
<tr class="even">
<td>orn:roadLink_{OGF_ID}</td>
<td>genprop:hasName</td>
<td>Road Element {OGF_ID}</td>
</tr>
<tr class="odd">
<td>TO_JCT</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>transnet:to</td>
<td>orn:Junction_{JUNCTION_ID}</td>
<td>The end junction for a road element or ferry connection.</td>
</tr>
<tr class="even">
<td>FROM_JCT</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>transnet:from</td>
<td>orn:Junction_{JUNCTION_ID}</td>
<td>The beginning junction for a road element or ferry connection.</td>
</tr>
<tr class="odd">
<td>NID</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>cdt:nationUUID</td>
<td>{NID}</td>
<td>A unique national identifier assigned to a road net element, junction and selected event data such as Toll Point, Blocked Passage and Structure which are required to support the National Road Network (NRN).</td>
</tr>
<tr class="even">
<td>DIRECTION</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>transnet:allowedDirections</td>
<td>code:Code</td>
<td>The direction(s) of vehicular or motor traffic flow. All road elements must have a direction of traffic flow assigned. Mapped using an enumeration class to capture semantic direction values (Positive, Negative, Both) in accordance with ISO 5087-3.</td>
</tr>
<tr class="odd">
<td>EXIT_NUM</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>cdt:exitNum</td>
<td>{EXIT_NUM}</td>
<td>The number of an exit on or off a freeway, expressway or highway, assigned by an administrating body and is represented by a valid number or character.</td>
</tr>
<tr class="even">
<td>TOLL_ROAD</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>cdt:tollRoad</td>
<td>xsd:boolean</td>
<td>Indicates if the road net element is a toll road. </td>
</tr>
<tr class="odd">
<td rowspan="4">ACQTECH</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>cdt:dataAquisitionTechnique</td>
<td>orn:acqtech_ {OGF_ID}</td>
<td rowspan="4"><p>The type of data source or technique used to create or revise the road net element. </p>
<p></p></td>
</tr>
<tr class="even">
<td>orn:acqtech_ {OGF_ID}</td>
<td>rdf:type</td>
<td>cdt: AquisitionTechnique</td>
</tr>
<tr class="odd">
<td>orn:acqtech_ {OGF_ID}</td>
<td>code:Code</td>
<td>code:acqtech Code_ {OGF_ID}</td>
</tr>
<tr class="even">
<td>code:acqtech Code_ {OGF_ID}</td>
<td>genprop:hasName</td>
<td>{ACQTECH}</td>
</tr>
<tr class="odd">
<td>CREDATE</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>cdt:creationDate</td>
<td>{CREDATE}</td>
<td>The date the road net element was originally created. </td>
</tr>
<tr class="even">
<td>REVDATE</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>cdt:revisionDate</td>
<td>{REVDATE}</td>
<td>The date the road net element was last revised or updated. </td>
</tr>
<tr class="odd">
<td>GEO_UPD_DT</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>cdt:geoUpdateDate</td>
<td>{GEO_UPD_DT}</td>
<td>Date/time the geometry was created or last modified in the source database. </td>
</tr>
<tr class="even">
<td>EFF_DATE</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>cdt:effectiveDate</td>
<td>{EFF_DATE}</td>
<td>Date/time the record was created or last modified in the source database. </td>
</tr>
<tr class="odd">
<td rowspan="6">LENGTH</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>cdt:length</td>
<td>cityunits:length_{OGF_ID}</td>
<td rowspan="6">The measured planimetric length of a road net element in meters. </td>
</tr>
<tr class="even">
<td>cityunits:length_{OGF_ID}</td>
<td>rdf:type</td>
<td>cityunits:Length</td>
</tr>
<tr class="odd">
<td>cityunits:length_{OGF_ID}</td>
<td>i72:hasValue</td>
<td>cityunits: lengthMeasure_{OGF_ID}</td>
</tr>
<tr class="even">
<td>cityunits: lengthMeasure_{OGF_ID}</td>
<td>rdf:type</td>
<td>cityunits: Measure</td>
</tr>
<tr class="odd">
<td>cityunits: lengthMeasure_{OGF_ID}</td>
<td>i72:hasUnit</td>
<td>i72:metre</td>
</tr>
<tr class="even">
<td>cityunits: lengthMeasure_{OGF_ID}</td>
<td>i72:hasNumericalValue</td>
<td>{LENGTH}</td>
</tr>
<tr class="odd">
<td rowspan="6">ACCURACY </td>
<td>orn:roadLink_{OGF_ID}</td>
<td>cdt:roadAbsoluteAccuracy</td>
<td>cityunits: accuracy_{OGF_ID}</td>
<td rowspan="6">A statement that identifies the positional accuracy of the ORN road geometry, in metres.</td>
</tr>
<tr class="even">
<td>cityunits: accuracy_{OGF_ID}</td>
<td>rdf:type</td>
<td>cityunits:Length</td>
</tr>
<tr class="odd">
<td>cityunits:accuracy_{OGF_ID}</td>
<td>i72:hasValue</td>
<td>cityunits:accuracy Measure_ {OGF_ID}</td>
</tr>
<tr class="even">
<td>cityunits:accuracy Measure_ {OGF_ID}</td>
<td>rdf:type</td>
<td>cityunits: Measure</td>
</tr>
<tr class="odd">
<td>cityunits:accuracy Measure_ {OGF_ID}</td>
<td>i72:hasUnit</td>
<td>i72:metre</td>
</tr>
<tr class="even">
<td>cityunits:accuracy Measure_ {OGF_ID}</td>
<td>i72:hasNumericalValue</td>
<td>{LENGTH}</td>
</tr>
<tr class="odd">
<td rowspan="2">geometry</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>loc:hasLocation</td>
<td>loc:roadLinkLocation_{OGF_ID}</td>
<td rowspan="2">Geometry attribute.</td>
</tr>
<tr class="even">
<td>loc:roadLinkLocation_{OGF_ID}</td>
<td>geo:asWKT</td>
<td>{geometry}</td>
</tr>
</tbody>
</table>

*<u>Table 4: Mapping ORN_ROAD_NET_ELEMENT.shp Road Link data to City Digital Twin</u>*

**ORN_SPEED_LIMIT.csv:** The maximum speed limit assigned to a road element in kilometres per hour in accordance with Municipal By-Laws or Provincial Law. In cases where a road element has more than one speed limit value, the speed limit of the longest portion of the road element is supplied.

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr class="header">
<th colspan="5">Data Provided by ORN_SPEED_LIMIT.csv:</th>
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
<td rowspan="6">SPEED_LIMIT</td>
<td>orn: typicalRoadLinkUser</td>
<td>rdf:type</td>
<td>cdt:RoadLinkUser</td>
<td rowspan="6"><p>The maximum speed limit assigned to a road element in kilometres per hour in accordance with Municipal By-Laws or Provincial Law.</p>
<p>Property of a RoadLinkUser, and is linked with corresponding RoadLink using road:usedBy and road:uses properties.</p>
<p>cityunits:Speed</p></td>
</tr>
<tr class="odd">
<td>orn: typicalRoadLinkUser</td>
<td>cdt:speedLimit</td>
<td>cityunits:speed_{OGF_ID}</td>
</tr>
<tr class="even">
<td>cityunits:speed_{OGF_ID}</td>
<td>rdf:type</td>
<td>cityunits: speedLimit</td>
</tr>
<tr class="odd">
<td>cityunits:speed_{OGF_ID}</td>
<td>i72:hasValue</td>
<td>cityunits: speedMeasure_{OGF_ID}</td>
</tr>
<tr class="even">
<td>cityunits: speedMeasure_{OGF_ID}</td>
<td>rdf:type</td>
<td>cityunits: Measure</td>
</tr>
<tr class="odd">
<td>cityunits: speedMeasure_{OGF_ID}</td>
<td>i72: hasNumericalValue</td>
<td>{SPEED_LIMIT}</td>
</tr>
</tbody>
</table>

*<u>Table 5: Mapping ORN_SPEED_LIMIT.csv to City Digital Twin</u>*

**ORN_ROAD_CLASS.csv:** A linear event identifying the class of road based on a functional classification schema.

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr class="header">
<th colspan="5">Data Provided by ORN_ROAD_CLASS.csv:</th>
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
<td rowspan="4">ROAD_CLASS</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>cdt:hasRoadClass</td>
<td>orn:roadClass_{OGF_ID}</td>
<td rowspan="4"><p>The classification of a road.</p>
<p></p></td>
</tr>
<tr class="odd">
<td>orn:roadClass_{OGF_ID}</td>
<td>rdf:type</td>
<td>cdt:RoadClass</td>
</tr>
<tr class="even">
<td>orn:roadClass_{OGF_ID}</td>
<td>code:Code</td>
<td>code:roadClass_ Code_ {OGF_ID}</td>
</tr>
<tr class="odd">
<td>code:roadClass_ Code_ {OGF_ID}</td>
<td>genprop:hasName</td>
<td>{ROAD_CLASS}</td>
</tr>
</tbody>
</table>

*<u>Table 6: Mapping ORN_ROAD_CLASS.csv to City Digital Twin</u>*

**ORN_OFFICIAL_STREET_NAME.csv:** An event identifying an official street name and may be associated with a bilingual name.

| Data Provided by ORN_OFFICIAL_STREET_NAME.csv: |                        |                 |                     |                                                                                                                                                                                                                                  |
|------------------------------------------------|------------------------|-----------------|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Field Name**                                 | **Subject**            | **Property**    | **Object**          | **Notes**                                                                                                                                                                                                                        |
| FULL_STREET_NAME                               | orn:roadLink\_{OGF_ID} | genProp:hasName | { FULL_STREET_NAME} | This attribute is derived from the individual street name components where present, namely directional prefix, street type prefix, street name body, street type suffix and directional suffix and is stored in upper case text. |

*<u>Table 7: Mapping ORN_OFFICIAL_STREET_NAME.csv Road Link data to City Digital Twin</u>*

**ORN_JURISDICTION.csv:** Identifies jurisdictional, or custodianship, responsibility of the road  

| Data Provided by ORN_JURISDICTION.csv: |                        |                  |                             |                                                                                                                                                                                                                                                        |
|----------------------------------------|------------------------|------------------|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Field Name**                         | **Subject**            | **Property**     | **Object**                  | **Notes**                                                                                                                                                                                                                                              |
| JURISDICTION                           | orn:roadLink\_{OGF_ID} | cdt:hasCustodian | org:govOrg\_{OGF_ID}        | An indication of who has the jurisdictional, or custodianship responsibility for a road net element. The custodian would have the responsibility to ensure maintenance occurs, but is not necessarily the one who undertakes the maintenance directly. |
|                                        | org:govOrg\_{OGF_ID}   | rdf:type         | org:Government Organization |                                                                                                                                                                                                                                                        |
|                                        | org:govOrg\_{OGF_ID}   | genprop:hasName  | {JURISDICTION}              |                                                                                                                                                                                                                                                        |

*<u>Table 9: Mapping ORN_JURISDICTION.csv to City Digital Twin</u>*

**ORN_ROAD_SURFACE.csv:** The surface type of a road element.

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr class="header">
<th colspan="5">Data Provided by ORN_ROAD_SURFACE.csv:</th>
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
<td rowspan="4">SURFACE_TYPE</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>cdt:hasSurfaceType</td>
<td>orn:surface_type_{OGF_ID}</td>
<td rowspan="4"><p>A linear event indicating the surface type of a road element.</p>
<p></p></td>
</tr>
<tr class="odd">
<td>orn:surface_type_{OGF_ID}</td>
<td>rdf:type</td>
<td>cdt:SurfaceType</td>
</tr>
<tr class="even">
<td>orn:surface_ type_{OGF_ID}</td>
<td>code:Code</td>
<td>code:surfaceType_Code_{OGF_ID}</td>
</tr>
<tr class="odd">
<td>code:surface Type_Code_ {OGF_ID}</td>
<td>genprop:hasName</td>
<td>{SURFACE_TYPE }</td>
</tr>
<tr class="even">
<td>PAVEMENT_STATUS</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>cdt:pavementStatus</td>
<td>xsd:boolean</td>
<td>The surface type of a road element.</td>
</tr>
</tbody>
</table>

  *<u>Table 10: Mapping ORN_ROAD_SURFACE.csv to City Digital Twin</u>*

**ORN_NUMBER_OF_LANES.csv:** A linear event indicating the number of lanes. 

| Data Provided by ORN_NUMBER_OF_LANES.csv: |                        |              |                     |                                |
|-------------------------------------------|------------------------|--------------|---------------------|--------------------------------|
| **Field Name**                            | **Subject**            | **Property** | **Object**          | **Notes**                      |
| NUMBER_OF_LANES                           | orn:roadLink\_{OGF_ID} | cdt:numLanes | {NUMBER_OF\_ LANES} | The number of lanes of a road. |

*<u>Table 11: Mapping ORN_NUMBER_OF_LANES.csv to City Digital Twin</u>*

**ORN_ROUTE_NAME.csv:** The name attached to a road net element as defined by a Municipality, Provincial Ministry, or Federal Agency and is associated to an established and/or maintained route.  

| Data Provided by ORN_ROUTE_NAME.csv |                        |               |                      |                                                                                                                                                                                           |
|-------------------------------------|------------------------|---------------|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Field Name**                      | **Subject**            | **Property**  | **Object**           | **Notes**                                                                                                                                                                                 |
| ROUTE_NAME_ENGLISH                  | orn:roadLink\_{OGF_ID} | cdt:routeName | {ROUTE_NAME_ENGLISH} | The English name that is attached to a road net element as defined by a Municipality, Provincial Ministry, or Federal Agency and is associated to an established and/or maintained route. |

*<u>Table 12: Mapping ORN_ROUTE_NAME.csv to City Digital Twin</u>*

**ORN_ROUTE_NUMBER.csv:** The route number attached to a road net element as defined by a Municipality, Provincial Ministry, or Federal Agency and is typically associated with provincial highways, secondary highways, county roads and regional roads

| Data Provided by ORN_ROUTE_NUMBER.csv: |                        |                 |                  |                                                                                                                                                                                                                                                          |
|----------------------------------------|------------------------|-----------------|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Field Name**                         | **Subject**            | **Property**    | **Object**       | **Notes**                                                                                                                                                                                                                                                |
| ROUTE_NUMBER                           | orn:roadLink\_{OGF_ID} | cdt:routeNumber | {ROUTE\_ NUMBER} | The route number assigned to a road typically associated with provincial highways, secondary highways, county roads and regional roads and is represented by a numeric and/or an alpha-numeric character. A road can be assigned multiple route numbers. |

*<u>Table 13: Mapping ORN_ROUTE_NUMBER.csv to City Digital Twin</u>*

**ORN_STRUCTURE.csv:** The classification of a structure, that exists on a road element and is managed as a linear event. The types are mutually exclusive. 

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr class="header">
<th colspan="5">Data Provided by ORN_STRUCTURE.csv:</th>
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
<td rowspan="2">STRUCTURE_TYPE</td>
<td>transnet: RoadSegment</td>
<td>transinfras:supports</td>
<td>Infras: {STRUCTURE_ TYPE}_{OGF_ID}</td>
<td rowspan="2"><p>The classification of a structure, that exists on a road element and is managed as a linear event.</p>
<p></p></td>
</tr>
<tr class="odd">
<td>Infras: {STRUCTURE_ TYPE}_{OGF_ID}</td>
<td>rdf:type</td>
<td><p>Infras:</p>
<p>Infrastructure Element</p></td>
</tr>
</tbody>
</table>

*<u>Table 14: Mapping ORN_STRUCTURE.csv to City Digital Twin</u>*

**ORN_TOLL_POINT.csv:** A point event along a road element indicating the presence of a toll point.  

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr class="header">
<th colspan="5">Data Provided by ORN_TOLL_POINT.csv:</th>
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
<td rowspan="4">TOLL_POINT_TYPE</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>cdt:hasTollPoint</td>
<td>orn:tollPoint_ {OGF_ID}</td>
<td rowspan="4"><p>A point event on a road element identifying the existence of an underpass. An underpass occurs where the road element runs underneath a passage accommodating the movement of water, a building, road, rail, pedestrian or wildlife.</p>
<p></p></td>
</tr>
<tr class="odd">
<td>orn:tollPoint_ {OGF_ID}</td>
<td>rdf:type</td>
<td>cdt:TollPoint</td>
</tr>
<tr class="even">
<td>orn:tollPoint_ {OGF_ID}</td>
<td>cdt:hasTollPointType</td>
<td>orn: {TOLL_POINT_ TYPE}_{OGF_ID}</td>
</tr>
<tr class="odd">
<td>orn: {TOLL_POINT_ TYPE}_{OGF_ID}</td>
<td>rdf:type</td>
<td>orn:{TOLL_POINT_TYPE}TP</td>
</tr>
</tbody>
</table>

*<u>Table 15: Mapping ORN_TOLL_POINT.csv to City Digital Twin</u>*

**ORN_UNDERPASS.csv:** A point event on a road element identifying the existence of an underpass. An underpass occurs where the road element runs underneath a passage accommodating the movement of water, a building, road, rail, pedestrian or wildlife. 

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr class="header">
<th colspan="5">Data Provided by ORN_UNDERPASS.csv:</th>
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
<td rowspan="6">UNDERPASS_TYPE</td>
<td>orn:roadLink_{OGF_ID}</td>
<td>cdt:hasUnderpass</td>
<td>orn:underpass_{OGF_ID}</td>
<td rowspan="6"><p>Identifies the type of underpass present at this road location.</p>
<p></p></td>
</tr>
<tr class="odd">
<td>orn:underpass_{OGF_ID}</td>
<td>rdf:type</td>
<td>cdt:Underpass</td>
</tr>
<tr class="even">
<td>orn:underpass_{OGF_ID}</td>
<td>cdt:hasUnderpass</td>
<td><p>orn: underpass_type_</p>
<p>{OGF_ID}</p></td>
</tr>
<tr class="odd">
<td>orn:underpass_type_{OGF_ID}</td>
<td>rdf:type</td>
<td>cdt:Underpass Type</td>
</tr>
<tr class="even">
<td>orn:underpass_type_{OGF_ID</td>
<td>code:Code</td>
<td>code:underpass TypeCode_ {OGF_ID}</td>
</tr>
<tr class="odd">
<td>code:underpass TypeCode_ {OGF_ID}</td>
<td>genprop:hasName</td>
<td>{UNDERPASS_TYPE}</td>
</tr>
</tbody>
</table>

*<u>Table 16: Mapping ORN_UNDERPASS.csv to City Digital Twin</u>*

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr class="header">
<th colspan="5">Data Provided by ORN Capacities</th>
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
<td rowspan="18"></td>
<td>orn:roadLink_{OGF_ID}Service</td>
<td>rdf:type</td>
<td>tor:TorTransportationNetworkService</td>
<td rowspan="20"><p>{ SPEED_LIMIT}*{NUMBER_OF_LANES}*{C_DENSITY({ROAD_CLASS})} is a very rough approximation where C_DENSITY is a value dependent on ROAD_CLASS</p>
<p>{Capacity} * random.uniform(0.5, 0.95) is randomized use based on capacity;</p>
<p>Note that we can't really tell if it's over or under capacity without observing speed</p>
<p>C_DENSITY(ROAD_CLASS) = "Freeway",26,</p>
<p>"Expressway / Highway",24,</p>
<p>"Arterial",20,</p>
<p>"Collector",18,</p>
<p>"Ramp",22,</p>
<p>"Local / Street",12,</p>
<p>"Local / Strata",12,</p>
<p>"Local / Unknown",12,</p>
<p>"Service",10,</p>
<p>"Alleyway / Laneway",10,</p>
<p>"Resource / Recreation",16,</p>
<p>"Rapid Transit",28,</p>
<p>"Winter",18,</p>
<p>20 /* default if unmatched */</p></td>
</tr>
<tr class="odd">
<td>orn:roadLink_{OGF_ID}Service</td>
<td>hp:providedFromSite</td>
<td>orn:roadLink_{OGF_ID}</td>
</tr>
<tr class="even">
<td>orn:roadLink_{OGF_ID}</td>
<td>res:hasCapacity</td>
<td>orn:roadLinkCapacity_{OGF_ID}</td>
</tr>
<tr class="odd">
<td>orn:roadLink_{OGF_ID}Service</td>
<td>res:hasCapacity</td>
<td>orn:roadLinkCapacity_{OGF_ID}</td>
</tr>
<tr class="even">
<td>orn:roadLinkCapacity_{OGF_ID}</td>
<td>rdf:type</td>
<td>hp:VehicleThroughputRate</td>
</tr>
<tr class="odd">
<td>orn:roadLinkCapacity_{OGF_ID}</td>
<td>i72:hasValue</td>
<td>orn:roadLinkCapacityMeasure_{OGF_ID}</td>
</tr>
<tr class="even">
<td>orn:roadLinkCapacityMeasure_{OGF_ID}</td>
<td>i72:hasNumericalValue</td>
<td>{SPEED_LIMIT}*{NUMBER_OF_LANES}*{C_DENSITY({ROAD_CLASS})}</td>
</tr>
<tr class="odd">
<td>orn:roadLinkCapacityMeasure_{OGF_ID}</td>
<td>i72:hasUnit</td>
<td>hp:vehicles_per_hour</td>
</tr>
<tr class="even">
<td>orn:roadLink_{OGF_ID}</td>
<td>res:capacityInUse</td>
<td>orn:roadLinkCapacityUse_{OGF_ID}</td>
</tr>
<tr class="odd">
<td>orn:roadLink_{OGF_ID}Service</td>
<td>res:capacityInUse</td>
<td>orn:roadLinkCapacityUse_{OGF_ID}</td>
</tr>
<tr class="even">
<td>orn:roadLinkCapacityUse_{OGF_ID}</td>
<td>rdf:type</td>
<td>hp:VehicleThroughputRate</td>
</tr>
<tr class="odd">
<td>orn:roadLinkCapacityUse_{OGF_ID}</td>
<td>i72:hasValue</td>
<td>orn:roadLinkCapacityUseMeasure_{OGF_ID}</td>
</tr>
<tr class="even">
<td>orn:roadLinkCapacityUseMeasure_{OGF_ID}</td>
<td>i72:hasNumericalValue</td>
<td>{Capacity} * random.uniform(0.5, 0.95)</td>
</tr>
<tr class="odd">
<td>orn:roadLinkCapacityUseMeasure_{OGF_ID}</td>
<td>i72:hasUnit</td>
<td>hp:vehicles_per_hour</td>
</tr>
<tr class="even">
<td>orn:roadLink_{OGF_ID}</td>
<td>res:hasAvailableCapacity</td>
<td>orn:roadLinkCapacityAvail_{OGF_ID}</td>
</tr>
<tr class="odd">
<td>orn:roadLink_{OGF_ID}Service</td>
<td>res:hasAvailableCapacity</td>
<td>orn:roadLinkCapacityAvail_{OGF_ID}</td>
</tr>
<tr class="even">
<td>orn:roadLinkCapacityAvail_{OGF_ID}</td>
<td>rdf:type</td>
<td>hp:AvailableVehicleThroughputRate</td>
</tr>
<tr class="odd">
<td>orn:roadLinkCapacityAvail_{OGF_ID}</td>
<td>i72:hasValue</td>
<td>orn:roadLinkCapacityAvailMeasure_{OGF_ID}</td>
</tr>
<tr class="even">
<td></td>
<td>orn:roadLinkCapacityAvailMeasure_{OGF_ID}</td>
<td>i72:hasNumericalValue</td>
<td>{Capacity} - {Capacity In Use}</td>
</tr>
<tr class="odd">
<td></td>
<td>orn:roadLinkCapacityAvailMeasure_{OGF_ID}</td>
<td>i72:hasUnit</td>
<td>hp:vehicles_per_hour</td>
</tr>
</tbody>
</table>

*<u>Table 17: Mapping ORN Capacity to City Digital Twin</u>*

## Implementation of ORN Data Mapping to TTL 

**Script:** [Toronto_Roads.py](https://github.com/csse-uoft/city-digital-twin-ontology/tree/main/Housing%20Potential%20Python)

**URI strategy**

The script generates deterministic URIs mainly under the orn:, loc:, code:, and tor: namespaces so that junctions, roads, road links, and synthetic service/capacity nodes can be referenced consistently.

- **Junction:** orn:junction\_{JUNCTION_ID}

- **Junction location:** loc:junction_loc\_{JUNCTION_ID}

- **Junction type:** orn:junction_type\_{JUNCTION_ID}

- **Junction type code:** code:junctionType_Code\_{JUNCTION_ID}

- **Road:** orn:road\_{id}  
  (id is generated while grouping road links by full street name)

- **RoadLink:** orn:roadLink\_{OGF_ID}

- **RoadLink location:** loc:roadLinkLocation\_{OGF_ID}

- **Road class:** orn:roadClass\_{OGF_ID}

- **Road class code:** code:roadClass_Code\_{OGF_ID}

- **Surface type:** orn:surface_type\_{OGF_ID}

- **Surface type code:** code:surfaceType_Code\_{OGF_ID}

- **Acquisition technique:** orn:acqtech\_{OGF_ID}

- **Acquisition technique code:** code:acqtechCode\_{OGF_ID}

- **Underpass:** orn:underpass\_{OGF_ID}

- **Underpass type:** orn:underpass_type\_{OGF_ID}

- **Underpass type code:** code:underpassTypeCode\_{OGF_ID}

- **Toll point:** orn:tollPoint\_{OGF_ID}

- **Synthetic transportation service:** orn:roadLink\_{OGF_ID}Service

- **Synthetic capacity / use / available capacity nodes:**

  - orn:roadLinkCapacity\_{OGF_ID}, orn:roadLinkCapacityMeasure\_{OGF_ID}

  - orn:roadLinkCapacityUse\_{OGF_ID}, orn:roadLinkCapacityUseMeasure\_{OGF_ID}

  - orn:roadLinkCapacityAvail\_{OGF_ID}, orn:roadLinkCapacityAvailMeasure\_{OGF_ID}

**Inputs**

1.  **Primary road geometry dataset**

    - ORN_ROAD_NET_ELEMENT.shp

    - Required fields used include:

      - OGF_ID

      - FROM_JCT

      - TO_JCT

      - geometry

      - LENGTH

      - ACCURACY

      - NID

      - DIRECTION

      - EXIT_NUM

      - ELEM_TYPE

      - TOLL_ROAD

      - ACQTECH

      - CREDATE

      - REVDATE

      - GEO_UPD_DT

      - EFF_DATE

2.  **Supplementary ORN CSV datasets**

    - ORN_SPEED_LIMIT.csv

    - ORN_ROAD_CLASS.csv

    - ORN_OFFICIAL_STREET_NAME.csv

    - ORN_JUNCTION.csv

    - ORN_BLOCKED_PASSAGE.csv

    - ORN_ADDRESS_INFO.csv

    - ORN_JURISDICTION.csv

    - ORN_NUMBER_OF_LANES.csv

    - ORN_ROAD_SURFACE.csv

    - ORN_ROUTE_NAME.csv

    - ORN_ROUTE_NUMBER.csv

    - ORN_STRUCTURE.csv

    - ORN_TOLL_POINT.csv

    - ORN_UNDERPASS.csv  
      These are merged onto the shapefile data using OGF_ID ↔ ORN_ROAD_NET_ELEMENT_ID.

3.  **Toronto bounding filter**

    - The script restricts the mapped data to road links and junctions within a Toronto latitude/longitude bounding box.

**Outputs**

- **toronto_roads.ttl**  
  Contains: junctions, roads, road links, geometries, topology, road attributes, custodianship, structures, toll points, and underpasses.

- **road_synthetic.ttl**  
  Contains: synthetic transportation service instances and estimated capacity, capacity-in-use, and available capacity for road links.

**Step-by-step process**

**Step 1 - Load the ORN shapefile and supplementary CSVs**  
The script loads ORN_ROAD_NET_ELEMENT.shp with GeoPandas, converts OGF_ID to string for consistent joins, reads all supporting CSV files with pandas, renames overlapping columns, and left-joins them onto the shapefile data.

**Step 2 - Initialize RDF graphs and namespaces**  
Two RDF graphs are created:

- g for the core transportation network mapping

- synthetic for estimated service capacity metrics  
  Namespaces such as geo, transnet, transinfras, loc, cdt, i72, genprop, hp, res, orn, and tor are bound.

**Step 3 - Create Junction instances**  
Using ORN_JUNCTION.csv, the script creates junction nodes for all junctions inside the Toronto bounding box:

- orn:junction\_{JUNCTION_ID} is typed as cdt:Junction

- a location node is created and linked using loc:hasLocation

- point geometry is stored via geo:asWKT

- junction type, exit number, national UUID, and effective date are asserted where available.

**Step 4 - Group road elements into Roads**  
The merged road network data is grouped by FULL_STREET_NAME_road_names. Each group becomes a Road instance, and the associated RoadLink instances are later attached to it using partwhole:hasProperPart. This models a road as a collection of road links sharing the same street name.

**Step 5 - Create RoadLink instances and filter unwanted elements**  
For each shapefile row:

- create orn:roadLink\_{OGF_ID}

- skip geometries outside the Toronto bounds

- skip any row where ELEM_TYPE == "Virtual Road"  
  Each valid road link is typed as cdt:RoadLink, linked to its parent road, and linked to a generic RoadLinkUser through transnet:usedBy / transnet:uses.

**Step 6 - Map RoadLink attributes**  
The script conditionally asserts available attributes, including:

- identifier and name

- speed limit

- road class

- number of lanes

- length

- positional accuracy

- national UUID

- surface type

- travel direction

- exit number

- toll-road boolean

- acquisition technique

- route name

- route number

- creation / revision / geometry update / effective dates  
  Geometry is represented through a location node linked with loc:hasLocation and a WKT linestring via geo:asWKT.

**Step 7 - Map topology between RoadLinks and Junctions**  
FROM_JCT and TO_JCT are used to connect road links to existing junction instances:

- transnet:from / transnet:egress

- transnet:to / transnet:ingress  
  This preserves the topological structure of the transportation network.

**Step 8 - Map custodianship, structures, toll points, and underpasses**  
When the relevant CSV values are present, the script adds:

- a government organization custodian (cdt:hasCustodian)

- structure information (bridge, tunnel, dam, etc.)

- toll point information and toll point type

- underpass information and underpass type.

**Step 9 - Compute synthetic transportation service capacity**  
When ROAD_CLASS, SPEED_LIMIT, and NUMBER_OF_LANES are all available, the script creates a synthetic service node for the road link and estimates:

- **capacity** = road_class_capacity\[ROAD_CLASS\] \* SPEED_LIMIT \* NUMBER_OF_LANES

- **capacity in use** = a random value between 50% and 95% of capacity

- **available capacity** = capacity - capacity in use  
  These are asserted as res:hasCapacity, res:capacityInUse, and res:hasAvailableCapacity, with units in hp:vehicles_per_hour.

**Step 10 - Serialize the TTL files**  
The core graph is serialized to toronto_roads.ttl, and the synthetic capacity graph is serialized to road_synthetic.ttl.

**Notes / assumptions**

- The ORN data is filtered to Toronto using a hard-coded bounding box, so features outside that geographic extent are excluded.

- Roads are grouped by full street name, so unnamed road links are skipped at the road-grouping stage.

- Virtual roads are explicitly excluded from the mapping.

- The transportation capacity values are synthetic approximations intended for demo use, not observed traffic measurements. Capacity-in-use is randomized from estimated capacity.

- The current script types the synthetic service as TORONTO.TorTransportationNetworkServicee, which appears to include an extra e and may need correction if you want it to match the intended ontology class name exactly.
