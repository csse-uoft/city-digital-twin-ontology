## Library

This is the ontological representation of the library data. Libraries are represented as instances of the Library class which is a subclass of an Organization class. Libraries can have a name which is linked via the hasName property, a unique identifier which is linked via the hasIdentifier property, an address which his linked via the orgAddress property, services that it provides via the providesService property, a website which is linked via the website property, a branch code which is linked via the branchCode property, its operating hours which is linked via the operatingHours property, a site that represents the physical premise of the library which is linked via the hasSite property, and more. The site of a Library, can have an indicator for whether it is wheelchair accessible using the wheelchairAccess property, a Location instance and a set of geospatial coordinates linked using the hasLocation and asWKT property respectively, and more.

The [Toronto Open Data Portal](https://open.toronto.ca/dataset/library-branch-general-information/)**,** is one of the datasets used. The dataset is strictly around Toronto Public Libraries, where each library contains the same pieces of information. Meanwhile, the OpenStreetMap dataset is a wide collection of various libraries in Toronto. OpenStreetMap also contains a random assortment of properties related to each library, meaning there is no fixed set of properties that each library has.

The following is a list of namespace prefixes<u> used in the mappings and ontology definitions that follow</u>: 

- tor: http://ontology.eil.utoronto.ca/Toronto/Toronto#

- genprop: https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/

- loc: https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/

- geo: http://www.opengis.net/ont/geosparql#

- hp: http://ontology.eil.utoronto.ca/HPCDM/

- service: https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/CityService/

- org: https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Organization/

- contact: <https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Contact/>

- res: <https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Resource/>

- cdt: http://ontology.eil.utoronto.ca/CDT#

- i72: [http://ontology.eil.utoronto.ca/ISO21972/iso21972#](http://ontology.eil.utoronto.ca/ISO21972/iso21972)

- code:https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Code/

- city:https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/City/

- recurringevent:https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/RecurringEvent/

- cenensus:http://ontology.eil.utoronto.ca/tove/cacensus#

This section provides a brief summary of how the tags used in OpenStreetMap and Toronto Open Data Portal were mapped into the ontology used in the City Digital Twin.

<img src="Library_media/media/image1.png" style="width:6.5in;height:3.05in" alt="A black background with white squares AI-generated content may be incorrect." />*<u>Figure 1: Diagram of Library Pattern</u>*

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
<th colspan="5">Data Provided by OpenStreetMap</th>
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
<td rowspan="5">@id</td>
<td>tor:library_{@id}</td>
<td>genprop: hasIdentifier</td>
<td>{@id}</td>
<td rowspan="4">Not official. Uniquely identifies the OSM object (node, way, or relation).</td>
</tr>
<tr class="odd">
<td>tor:library_site_{@id}</td>
<td>genprop:hasName</td>
<td>{name}</td>
</tr>
<tr class="even">
<td>tor:addLibrary_{@id}</td>
<td>rdf:type</td>
<td>contact:Address</td>
</tr>
<tr class="odd">
<td>tor:library_site_{@id}</td>
<td>rdf:type</td>
<td>cdt:LibrarySite</td>
</tr>
<tr class="even">
<td>tor:library_{@id}</td>
<td>rdf:type</td>
<td>cdt:Library</td>
<td>defines the general, high-level library service; all other services are subactivities of this</td>
</tr>
<tr class="odd">
<td>access</td>
<td>tor:library_{@id}</td>
<td>cdt:isPublic</td>
<td>xsd:boolean</td>
<td>For describing the legal accessibility of a feature.</td>
</tr>
<tr class="even">
<td rowspan="3">addr:city</td>
<td>tor:addLibrary_{@id}</td>
<td>contact:hasCity</td>
<td>city:city_{@id}</td>
<td rowspan="3">The name of the largest settlement (city / town / other) that is included in the address.</td>
</tr>
<tr class="odd">
<td>city:city_{@id}</td>
<td>rdf:type</td>
<td>city:City</td>
</tr>
<tr class="even">
<td>city:city_{@id}</td>
<td>contact:legalName</td>
<td>{addr:city}</td>
</tr>
<tr class="odd">
<td>addr:floor</td>
<td>tor:library_site_{@id}</td>
<td>cdt:numFloor</td>
<td>{addr:floor}</td>
<td>The floor where an address feature is located, using locally used method of indicating specific floor.</td>
</tr>
<tr class="even">
<td>addr:housename</td>
<td>tor:library_{@id}</td>
<td>genprop:hasName</td>
<td>{addr:housename}</td>
<td>The house (or building) name that is included in the address. Popular in some countries like England, Spain, Portugal, Latvia instead of, or in addition to, a house number</td>
</tr>
<tr class="odd">
<td>addr:housenumber</td>
<td>tor:addLibrary_{@id}</td>
<td>contact: houseNumber</td>
<td>{addr: housenumber}</td>
<td>The house number (may contain letters, dashes or other characters).</td>
</tr>
<tr class="even">
<td>addr:postcode</td>
<td>tor:addLibrary_{@id}</td>
<td>contact: hasPostcode</td>
<td>{addr:postcode}</td>
<td>The postal code / zip code that is included in the address.</td>
</tr>
<tr class="odd">
<td rowspan="4">addr:province</td>
<td>tor:addLibrary_{@id}</td>
<td>contact:hasProvince</td>
<td>contact:state_ {@id}</td>
<td rowspan="4">The name of the province that is included in the address. A province is almost always an administrative division within a country or state.</td>
</tr>
<tr class="even">
<td>contact:state_ {@id}</td>
<td>rdf:type</td>
<td>contact:State</td>
</tr>
<tr class="odd">
<td>contact:state_{@id}</td>
<td>Code:hasCode</td>
<td>code:state_Code_{@id}</td>
</tr>
<tr class="even">
<td>code:state_Code_{@id}</td>
<td>genprop:hasName</td>
<td>{addr:province}</td>
</tr>
<tr class="odd">
<td>addr:street</td>
<td>tor:addLibrary_{@id}</td>
<td>contact:hasStreet</td>
<td>{addr:street}</td>
<td>The street name that this address is (and any others in this location are) grouped by. This street name should match that of a nearby road, track or path.</td>
</tr>
<tr class="even">
<td>after_hours_return</td>
<td>tor:library_site_{@id}</td>
<td>cdt:afterHoursReturns</td>
<td>xsd:boolean</td>
<td>Not official. Indicates the availability of a book/media return slot or similar feature when the facility is closed.</td>
</tr>
<tr class="odd">
<td>air_conditioning</td>
<td>tor:library_site_{@id}</td>
<td>cdt:airConditioning</td>
<td>xsd:boolean</td>
<td>Indication whether a feature has air-conditioning</td>
</tr>
<tr class="even">
<td>architect</td>
<td>tor:library_site_{@id}</td>
<td>cdt:architect</td>
<td>{architect}</td>
<td>Name of architect</td>
</tr>
<tr class="odd">
<td rowspan="3">building</td>
<td>tor:library_{@id}</td>
<td><p>cdt:isPublic</p>
<p>if value is ‘yes’</p></td>
<td>xsd:boolean</td>
<td rowspan="3">To mark the outline of a building, a man-made structure with a roof, standing more or less permanently in one place. </td>
</tr>
<tr class="even">
<td>tor:library_site_{@id}</td>
<td>cdt:hasBuildingType</td>
<td>cdt:buildingType_ {building}</td>
</tr>
<tr class="odd">
<td>cdt:buildingType_ {building}</td>
<td>rdf:type</td>
<td>cdt:BuildingType</td>
</tr>
<tr class="even">
<td rowspan="2">building:colour</td>
<td>tor:library_site_{@id}</td>
<td>cdt:hasColor</td>
<td>cdt:color_ {building:colour}</td>
<td rowspan="2">Indicates colour of the building. </td>
</tr>
<tr class="odd">
<td>cdt:color_ {building:colour}</td>
<td>rdf:type</td>
<td>cdt:Color</td>
</tr>
<tr class="even">
<td rowspan="2">building:material</td>
<td>tor:library_site_{@id}</td>
<td>cdt:material</td>
<td>cdt:material_ {building:material}</td>
<td rowspan="2">Outer material for the building façade</td>
</tr>
<tr class="odd">
<td>cdt:material_ {building:material}</td>
<td>rdf:type</td>
<td>cdt:Material</td>
</tr>
<tr class="even">
<td>built_date</td>
<td>tor:library_site_{@id}</td>
<td>cdt:openingYear</td>
<td>{built_year}</td>
<td>Not official. Specifies the construction date of a building or structure.</td>
</tr>
<tr class="odd">
<td>capacity</td>
<td>tor:library_site_{@id}</td>
<td>cdt:maxOccupancy</td>
<td>{maxOccupancy}</td>
<td>Describes the capacity a facility is suitable for.</td>
</tr>
<tr class="even">
<td>check_date</td>
<td>tor:library_site_{@id}</td>
<td>cdt:revisionDate</td>
<td>{check_date}</td>
<td>Date of latest review of the data. Format: YYYY-MM-DD. </td>
</tr>
<tr class="odd">
<td>description</td>
<td>tor:library_site_{@id}</td>
<td>genprop: hasDescription</td>
<td>{description}</td>
<td>To provide additional information about the related element to the end map user.</td>
</tr>
<tr class="even">
<td>email</td>
<td>tor:library_site_{@id}</td>
<td>cdt:hasEmail</td>
<td>cdt:email_{@id}</td>
<td>An email address associated with the object </td>
</tr>
<tr class="odd">
<td>height</td>
<td>tor:library_site_{@id}</td>
<td>cdt:height</td>
<td>{height}</td>
<td>Height is the measurement of vertical distance. It indicates how "tall" something is.</td>
</tr>
<tr class="even">
<td>internet_access</td>
<td>tor:library_site_{@id}</td>
<td>cdt: hasInternetAccess</td>
<td>xsd:boolean</td>
<td>Indicates if an object offers internet access. The access can be with given computers or WLAN access. The only limitation is that the internet access has to be public.</td>
</tr>
<tr class="odd">
<td>internet_access:fee</td>
<td>tor:library_site_{@id}</td>
<td>cdt:hasPaidWIFI</td>
<td>xsd:boolean</td>
<td>Indicates whether a fee is required to access internet service offered at a feature.</td>
</tr>
<tr class="even">
<td>internet_access:ssid</td>
<td>tor:library_site_{@id}</td>
<td>cdt:ssid</td>
<td>{internet_access: ssid}</td>
<td>Specifies the "ssid", also know as the network name, of a WLAN wireless internet network (Wi-Fi). </td>
</tr>
<tr class="odd">
<td>name</td>
<td>tor:library_{@id}</td>
<td>genProp:hasName</td>
<td>{name}</td>
<td>The primary name: in general, the most prominent signposted name or the most common name in the local language(s). </td>
</tr>
<tr class="even">
<td>name:fr</td>
<td>tor:library_{@id}</td>
<td>cdt:frName</td>
<td>{name:fr}</td>
<td>A name in French.</td>
</tr>
<tr class="odd">
<td>name:ta</td>
<td>tor:library_{@id}</td>
<td>cdt:taName</td>
<td>{name:ta}</td>
<td>A name in Tamil</td>
</tr>
<tr class="even">
<td>name:zh</td>
<td>tor:library_{@id}</td>
<td>cdt:zhName</td>
<td>{name:zh}</td>
<td>A name in Chinese</td>
</tr>
<tr class="odd">
<td>note</td>
<td>tor:library_site_{@id}</td>
<td>genprop: hasDescription</td>
<td>{note}</td>
<td>A note to yourself or to other mappers.</td>
</tr>
<tr class="even">
<td rowspan="5">opening_hours</td>
<td>tor:library_{@id}</td>
<td>org_city: operatingHours</td>
<td>org:{day}_{@id}</td>
<td rowspan="5">Describes when something is open or closed in a standard format. {day}, {closing_time} and {opening_time} is gotten from opening_hours.</td>
</tr>
<tr class="odd">
<td>org:{day}_{@id}</td>
<td>org:hasOpeningTime</td>
<td>{opening_time}</td>
</tr>
<tr class="even">
<td>org:{day}_{@id}</td>
<td>org:hasClosingTime</td>
<td>{closing_time}</td>
</tr>
<tr class="odd">
<td>org:{day}_{@id}</td>
<td>Recurringevent: hasDayofWeek</td>
<td>{day}</td>
</tr>
<tr class="even">
<td>org:{day}_{@id}</td>
<td>cdt:material_ {building:material}</td>
<td>org:Operator</td>
</tr>
<tr class="odd">
<td>operator</td>
<td>org:{operator}</td>
<td>org: hasSubOrganization</td>
<td>tor:library_{@id}</td>
<td>Сompany, corporation, person or any other entity who is directly in charge of the current operation of a map object</td>
</tr>
<tr class="even">
<td>operator:type</td>
<td>org:{operator}</td>
<td>rdf:type</td>
<td>org:Government Organization</td>
<td><p>Defines the type of operator, eg. "public", "private", "government".</p>
<p>if {operator:type} == “government”</p></td>
</tr>
<tr class="odd">
<td rowspan="2">parking</td>
<td>tor:library_site_{@id}</td>
<td>cdt:hasParkingType</td>
<td>cdt:parking_ {parking}</td>
<td rowspan="2">Indicates the type of the parking facility</td>
</tr>
<tr class="even">
<td>cdt:parking_ {parking}</td>
<td>rdf:type</td>
<td>cdt:ParkingType</td>
</tr>
<tr class="odd">
<td rowspan="3">phone</td>
<td>tor:library_{@id}</td>
<td>contact: hasTelephone</td>
<td>contact: phone_{@id}</td>
<td rowspan="3">A telephone number associated with the object. Use +CC XXX XXX XXX format, where CC is a country code</td>
</tr>
<tr class="even">
<td>phone_{@id}</td>
<td>rdf:type</td>
<td><p>contact:</p>
<p>PhoneNumber</p></td>
</tr>
<tr class="odd">
<td>contact: phone_{@id}</td>
<td>contact:has TelephoneNumber</td>
<td>{phone}</td>
</tr>
<tr class="even">
<td>ref</td>
<td>tor:library_{@id}</td>
<td>cdt:branchCode</td>
<td>{ref}</td>
<td>Used for reference numbers or codes. Common for roads, highway exits, routes, entrances to big buildings etc.</td>
</tr>
<tr class="odd">
<td>return_machine</td>
<td>tor:library_site_{@id}</td>
<td>cdt: hasReturnMachine</td>
<td>xsd:boolean</td>
<td>Not official. Indicates whether a facility has a machine-based return system, such as an automated book drop or self-service return kiosk.</td>
</tr>
<tr class="even">
<td rowspan="2">roof:colour</td>
<td>tor:library_site_{@id}</td>
<td>cdt:roofColor</td>
<td>cdt:color_ {roof:colour }</td>
<td rowspan="2">Colour of the roof</td>
</tr>
<tr class="odd">
<td>cdt:color_ { roof:colour }</td>
<td>rdf:type</td>
<td>cdt:Color</td>
</tr>
<tr class="even">
<td rowspan="2">roof:material</td>
<td>tor:library_site_{@id}</td>
<td>cdt:roofMaterial</td>
<td>cdt:material_ {roof:material}</td>
<td rowspan="2">Outer material for the building roof.</td>
</tr>
<tr class="odd">
<td>cdt:material_ {roof:material}</td>
<td>rdf:type</td>
<td>cdt:Material</td>
</tr>
<tr class="even">
<td>self_checkout</td>
<td>tor:library_site_{@id}</td>
<td>cdt:hasSelfCheckout</td>
<td>xsd:boolean</td>
<td>If a shop has a self-checkout counter.</td>
</tr>
<tr class="odd">
<td>source</td>
<td>tor:library_{@id}</td>
<td>cdt:dataSource</td>
<td>{source}</td>
<td>For indicating the source of all tags added to the OSM database. Show/edit corresponding data item.</td>
</tr>
<tr class="even">
<td>stars</td>
<td>tor:library_site_{@id}</td>
<td>cdt:rating</td>
<td>{stars}</td>
<td>Used to classify or rate certain places (e.g. restaurants, hotels, camp sites).</td>
</tr>
<tr class="odd">
<td>stars:system</td>
<td>tor:library_site_{@id}</td>
<td>cdt:rating</td>
<td>{stars:system}</td>
<td>Specifies the rating system used for the stars=* tag.</td>
</tr>
<tr class="even">
<td>start_date</td>
<td>tor:library_site_{@id}</td>
<td>cdt:openingYear</td>
<td>{start_date}</td>
<td>Date when feature opened or the construction of the feature finished.</td>
</tr>
<tr class="odd">
<td>toilets</td>
<td>tor:library_site_{@id}</td>
<td>cdt:hasToilets</td>
<td>xsd:boolean</td>
<td>Indicates if a feature has a toilet.</td>
</tr>
<tr class="even">
<td rowspan="3">geometry</td>
<td>tor:library_site_{@id}</td>
<td>loc:hasLocation</td>
<td>loc:location_{@id}</td>
<td rowspan="3">Geometry of the library.</td>
</tr>
<tr class="odd">
<td>loc:location_{@id}</td>
<td>rdf:type</td>
<td>loc:Location</td>
</tr>
<tr class="even">
<td>loc:location_{@id}</td>
<td>geo:asWKT</td>
<td>{geometry}</td>
</tr>
<tr class="odd">
<td>website</td>
<td>tor:library_{@id}</td>
<td>cdt:website</td>
<td>{website}</td>
<td>Specifies the link to the official website for a feature.</td>
</tr>
<tr class="even">
<td>wheelchair</td>
<td>tor:library_site_{@id}</td>
<td>cdt: wheelchairAccess</td>
<td>xsd:boolean</td>
<td>Indicate if a special place can be used with wheelchairs</td>
</tr>
</tbody>
</table>

Table 1: Mapping OpenStreetMap Library Data to City Digital Twin

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
<th colspan="5">Data Provided by Toronto Open Data</th>
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
<td rowspan="4">_id</td>
<td>tor:library_{_id}</td>
<td>genprop:hasIdentifier</td>
<td>xsd:string</td>
<td rowspan="4">Unique row identifier for Open Data database</td>
</tr>
<tr class="odd">
<td>tor:library_{_id}</td>
<td>rdf:type</td>
<td>cdt:Library</td>
</tr>
<tr class="even">
<td>tor:addLibrary_{_id}</td>
<td>rdf:type</td>
<td>contact:Address</td>
</tr>
<tr class="odd">
<td>tor:library_site_{_id}</td>
<td>rdf:type</td>
<td>cdt:LibrarySite</td>
</tr>
<tr class="even">
<td>BranchCode</td>
<td>tor:library_{_id }</td>
<td>cdt:branchCode</td>
<td>{BranchCode}</td>
<td>A code identifying the TPL branch.</td>
</tr>
<tr class="odd">
<td>PhysicalBranch</td>
<td>tor:library_{_id }</td>
<td>cdt:isPublic</td>
<td>xsd:boolean</td>
<td>Library branches with fixed locations are set to 1. Other TPL services and collections are set to 0.</td>
</tr>
<tr class="even">
<td>BranchName</td>
<td>tor:library_{_id }</td>
<td>genprop:hasName</td>
<td>{BranchName}</td>
<td>The name of the library branch.</td>
</tr>
<tr class="odd">
<td rowspan="9">Address</td>
<td rowspan="4">tor:addLibrary_{_id }</td>
<td>contact:hasStreet</td>
<td>{street}</td>
<td rowspan="9">The full address of the branch. Address has {street}, {street_number}, {city}, and {province} all in one string.</td>
</tr>
<tr class="even">
<td>contact: hasStreetNumber</td>
<td>{street_number}</td>
</tr>
<tr class="odd">
<td>contact:hasCity</td>
<td>city:city_{_id}</td>
</tr>
<tr class="even">
<td>contact:hasProvince</td>
<td>contact:state_ {_id}</td>
</tr>
<tr class="odd">
<td rowspan="2">city:city_{_id}</td>
<td>rdf:type</td>
<td>city:City</td>
</tr>
<tr class="even">
<td>contact:legalName</td>
<td>{city}</td>
</tr>
<tr class="odd">
<td rowspan="3">contact:state_ {_id}</td>
<td>rdf:type</td>
<td>contact:State</td>
</tr>
<tr class="even">
<td>Code:hasCode</td>
<td>code:state_ Code_{_id}</td>
</tr>
<tr class="odd">
<td>genprop:hasName</td>
<td>{province}</td>
</tr>
<tr class="even">
<td>PostalCode</td>
<td>tor:addLibrary_{_id }</td>
<td>contact:hasPostcode</td>
<td>{PostalCode}</td>
<td>The branch postal code.</td>
</tr>
<tr class="odd">
<td>Website</td>
<td>tor:library_{_id }</td>
<td>cdt:website</td>
<td>{website}</td>
<td>The branch website.</td>
</tr>
<tr class="even">
<td rowspan="3">Telephone</td>
<td>tor:addLibrary_{_id }</td>
<td>contact: hasTelephone</td>
<td>contact: phone_{_id}</td>
<td rowspan="3">The phone number for the branch.</td>
</tr>
<tr class="odd">
<td>phone_{_id}</td>
<td>rdf:type</td>
<td><p>contact:</p>
<p>PhoneNumber</p></td>
</tr>
<tr class="even">
<td>contact: phone_{@id}</td>
<td>contact:has TelephoneNumber</td>
<td>{Telephone }</td>
</tr>
<tr class="odd">
<td rowspan="20">SquareFootage</td>
<td>tor:library_site_{_id}</td>
<td>hp:hasFloorArea</td>
<td>tor:library_site_{_id}FloorArea</td>
<td rowspan="6">The total size of the branch in square feet.</td>
</tr>
<tr class="even">
<td>tor:library_site_{_id}FloorArea</td>
<td>rdf:type</td>
<td>hp:FloorArea</td>
</tr>
<tr class="odd">
<td>tor:library_site_{_id}FloorArea</td>
<td>i72:hasValue</td>
<td>tor:library_site_{_id}FloorAreaMeasure</td>
</tr>
<tr class="even">
<td>tor:library_site_{_id}FloorAreaMeasure</td>
<td>i72:hasNumericalValue</td>
<td>{SquareFootage}</td>
</tr>
<tr class="odd">
<td>tor:library_site_{_id}FloorAreaMeasure</td>
<td>i72:hasUnit</td>
<td>hp:square_foot</td>
</tr>
<tr class="even">
<td>tor:library_service{_id}</td>
<td>res:hasCapacity</td>
<td>tor:library_service{_id}Capacity</td>
</tr>
<tr class="odd">
<td>tor:library_service{_id}Capacity</td>
<td>rdf:type</td>
<td>hp:MinLibraryAreaPopulationRatio</td>
<td>suggested from ChatGPT</td>
</tr>
<tr class="even">
<td>tor:library_service{_id}Capacity</td>
<td>i72:hasValue</td>
<td>tor:library_service{_id}CapacityMeasure</td>
<td rowspan="6">Consideration: it may be more appropriate to define this as the <em>total</em> square footage of <em>all</em> libraries in the catchment area (not just the square footage for this library)</td>
</tr>
<tr class="odd">
<td>tor:library_service{_id}CapacityMeasure</td>
<td>i72:hasNumericalValue</td>
<td>1</td>
</tr>
<tr class="even">
<td>tor:library_service{_id}CapacityMeasure</td>
<td>i72:hasUnit</td>
<td>hp:square_metre_per_person</td>
</tr>
<tr class="odd">
<td>tor:library_service{_id}CapacityMeasure</td>
<td>res:capacityInUse</td>
<td>tor:library_service{_id}CapacityUse</td>
</tr>
<tr class="even">
<td>tor:library_service{_id}CapacityUse</td>
<td>rdf:type</td>
<td>hp:LibraryAreaPopulationRatio</td>
</tr>
<tr class="odd">
<td>tor:library_service{_id}CapacityUse</td>
<td>i72:hasValue</td>
<td>tor:library_service{_id}CapacityUseMeasure</td>
</tr>
<tr class="even">
<td>tor:library_service{_id}CapacityUseMeasure</td>
<td>i72:hasNumericalValue</td>
<td>{SquareFootage in metres} / 55613</td>
<td rowspan="7">library area converted to metres, divided by the estimated population of a 2km radius catchment area</td>
</tr>
<tr class="odd">
<td>tor:library_service{_id}CapacityUseMeasure</td>
<td>i72:hasUnit</td>
<td>hp:square_metre_per_person</td>
</tr>
<tr class="even">
<td>tor:library_service{_id}AvailCapacityMeasure</td>
<td>res:hasAvailableCapacity</td>
<td>tor:library_service{_id}AvailCapacityUse</td>
</tr>
<tr class="odd">
<td>tor:library_service{_id}AvailCapacityUse</td>
<td>rdf:type</td>
<td>hp:AvailableLibraryPopulationRatio</td>
</tr>
<tr class="even">
<td>tor:library_service{_id}AvailCapacityUse</td>
<td>i72:hasValue</td>
<td>tor:library_service{_id}AvailCapacityUseMeasure</td>
</tr>
<tr class="odd">
<td>tor:library_service{_id}AvailCapacityUseMeasure</td>
<td>i72:hasNumericalValue</td>
<td>1 - {SquareFootage in metres} / 55613</td>
</tr>
<tr class="even">
<td>tor:library_service{_id}CapacityUseMeasure</td>
<td>i72:hasUnit</td>
<td>hp:square_metre_per_person</td>
</tr>
<tr class="odd">
<td rowspan="2">PublicParking</td>
<td>tor:library_site_{_id}</td>
<td>cdt:numParking</td>
<td>{PublicParking}</td>
<td rowspan="2">The number of parking spaces available for the public. If a branch does not have any public parking spaces, this field is set to 0. If a branch shares parking spaces with another location (community centre, mall, etc.), this field is set to “shared”.</td>
</tr>
<tr class="even">
<td>tor:library_site_{_id}</td>
<td>cdt: hasSharedParking</td>
<td>xsd:boolean</td>
</tr>
<tr class="odd">
<td rowspan="3">KidsStop</td>
<td>tor:library_site_{_id}</td>
<td>cdt:providesService</td>
<td>cdt:kids_ stop_{_id}</td>
<td rowspan="3">This field denotes the presence of a KidsStop (1 for present, 0 for not present). KidsStops are learning and reading spaces created for parents and young children.</td>
</tr>
<tr class="even">
<td>cdt:kids_stop_{_id}</td>
<td>rdf:type</td>
<td>hp: LibraryService</td>
</tr>
<tr class="odd">
<td>cdt:kids_stop_{_id}</td>
<td>genprop:hasName</td>
<td>{KidsStop}</td>
</tr>
<tr class="even">
<td rowspan="3">Leading Reading</td>
<td>tor:library_site_{_id}</td>
<td>cdt:providesService</td>
<td>cdt: leadingReading_serv_{_id}</td>
<td rowspan="3">This field denotes the presence of the Leading To Reading service (1 for present, 0 for not present). Leading to Reading is a free service for children to receive one-on-one help and encouragement with their reading and writing skills.</td>
</tr>
<tr class="odd">
<td>cdt:leadingReading_ serv_{_id}</td>
<td>rdf:type</td>
<td>hp: LibraryService</td>
</tr>
<tr class="even">
<td>cdt:leadingReading_ serv_{_id}</td>
<td>genprop:hasName</td>
<td>{Leading Reading}</td>
</tr>
<tr class="odd">
<td rowspan="3">CLC</td>
<td>tor:library_site_{_id}</td>
<td>cdt:providesService</td>
<td>cdt:clc_serv_ {_id}</td>
<td rowspan="3">This field denotes the presence of a Computer Learning Centre (1 for present, 0 for not present). CLCs are computer labs that offer hands-on technology classes.</td>
</tr>
<tr class="even">
<td>cdt:clc_serv_{_ id}</td>
<td>rdf:type</td>
<td>hp: LibraryService</td>
</tr>
<tr class="odd">
<td>cdt:clc_serv_{_ id}</td>
<td>genprop:hasName</td>
<td>{CLC}</td>
</tr>
<tr class="even">
<td rowspan="3">DIH</td>
<td>tor:library_site_{_id}</td>
<td>cdt:providesService</td>
<td>cdt:dih_serv_{_ id}</td>
<td rowspan="3">This field denotes the presence of a Digital Innovation Hub (1 for present, 0 for not present). DIHs are learning and creation spaces with computers, professional software, and a wide variety of equipment, including 3D printers, audio and video production tools, Arduinos, and more.</td>
</tr>
<tr class="odd">
<td>cdt:dih_serv_{_ id}</td>
<td>rdf:type</td>
<td>hp: LibraryService</td>
</tr>
<tr class="even">
<td>cdt:dih_serv_{_ id}</td>
<td>genprop:hasName</td>
<td>{DIH}</td>
</tr>
<tr class="odd">
<td rowspan="3">TeenCouncil</td>
<td>tor:library_site_{_id}</td>
<td>cdt:providesService</td>
<td>cdt:teenCouncil_serv_{_ id}</td>
<td rowspan="3">This field denotes the presence of a Teen Council (1 for present, 0 for not present). Teen Councils are groups of teens that attend monthly meetings with library staff, collaborate on group projects, and work to benefit their libraries and communities.</td>
</tr>
<tr class="even">
<td><p>cdt: teenCouncil_serv_</p>
<p>{_ id}</p></td>
<td>rdf:type</td>
<td>hp: LibraryService</td>
</tr>
<tr class="odd">
<td><p>cdt: teenCouncil_serv_</p>
<p>{_ id}</p></td>
<td>genprop:hasName</td>
<td>{TeenCouncil}</td>
</tr>
<tr class="even">
<td rowspan="3">YouthHub</td>
<td>tor:library_site_{_id}</td>
<td>cdt:providesService</td>
<td>cdt:youthHub_ serv_{_id}</td>
<td rowspan="3">This field denotes the presence of a Youth Hub (1 for present, 0 for not present). Youth Hubs are drop-in spaces where teens can study, chat with friends, use technology, or take part in activities such as arts and crafts and gaming.</td>
</tr>
<tr class="odd">
<td>cdt:youthHub_ serv_{_ id}</td>
<td>rdf:type</td>
<td>hp: LibraryService</td>
</tr>
<tr class="even">
<td>cdt:youthHub_ serv_{_ id}</td>
<td>genprop:hasName</td>
<td>{YouthHub}</td>
</tr>
<tr class="odd">
<td rowspan="3">AdultLiteracy Program</td>
<td>tor:library_site_{_id}</td>
<td>cdt:providesService</td>
<td>cdt:adultLiteracy_serv_{_id}</td>
<td rowspan="3">This field denotes the presence of the Adult Literacy Program service (1 for present, 0 for not present). The Adult Literacy Program offers free, one-on-one tutoring in basic reading, writing, and math for English-speaking adults 19 years or older (exceptions may apply)</td>
</tr>
<tr class="even">
<td><p>cdt: adultLiteracy_serv_</p>
<p>{_id}</p></td>
<td>rdf:type</td>
<td>hp: LibraryService</td>
</tr>
<tr class="odd">
<td><p>cdt: adultLiteracy_serv_</p>
<p>{_id}</p></td>
<td>genprop:hasName</td>
<td>{AdultLiteracy Program}</td>
</tr>
<tr class="even">
<td>Workstations</td>
<td>tor:library_site_{_id}</td>
<td>cdt:numComputer</td>
<td>{Workstations}</td>
<td>A count of computers with internet access available for public use in the branch.</td>
</tr>
<tr class="odd">
<td rowspan="4">ServiceTier</td>
<td>tor:library_site_{_id}</td>
<td>cdt:hasServiceTier</td>
<td>cdt:serviceTier_{_id}</td>
<td rowspan="4"><p>Service tier refers to the scope and scale of the branch/service.</p>
<p>NL - Neighbourhood branches provide collections and services that meet many of the needs of the immediate community. Bookmobiles and Home Library Service are part of the NL service tier.</p>
<p>DL - District branches offer extensive informational and recreational collections, as well as services that meet the needs of the immediate community and the larger district.</p>
<p>RR - Research and reference branches provide comprehensive and specialized collections, as well asservices with an emphasis on access.</p>
<p>RA - Remote access offers self-serve systems (online and by phone).</p>
<p>OT - Other service activities.</p>
<p>For more information, please refer to <a href="https://www.torontopubliclibrary.ca/content/about-the-library/service-plans-strategies-frameworks/Service.Delivery.Model.pdf">Toronto Public Library’s Service Delivery Model</a></p></td>
</tr>
<tr class="even">
<td>cdt:serviceTier_{_id}</td>
<td>rdf:type</td>
<td>cdt:ServiceTier</td>
</tr>
<tr class="odd">
<td>cdt:serviceTier_{_id}</td>
<td>code:Code</td>
<td>code:tierCode_ {_id}</td>
</tr>
<tr class="even">
<td>code:tierCode_{_id}</td>
<td>genprop:hasName</td>
<td>{ServiceTier}</td>
</tr>
<tr class="odd">
<td>Lat</td>
<td rowspan="2">tor:library_site_{_id}</td>
<td rowspan="2">loc:hasLocation</td>
<td rowspan="2">loc:location_ {_id}</td>
<td>The latitude coordinate of the branch.</td>
</tr>
<tr class="even">
<td rowspan="3">Long</td>
<td rowspan="3">The longitude coordinate of the branch.</td>
</tr>
<tr class="odd">
<td>loc:location_ {_id}</td>
<td>rdf:type</td>
<td>loc:Location</td>
</tr>
<tr class="even">
<td>loc:location_ {_id}</td>
<td>geo:asWKT</td>
<td>POINT ({Long} {LAT})</td>
</tr>
<tr class="odd">
<td rowspan="2">NBHDNo</td>
<td>toronto: neighbourhood_{_id}</td>
<td>rdf:type</td>
<td>toronto: Neighbourhood</td>
<td rowspan="2">The ID number of the neighbourhood associated with the branch. Neighbourhood boundaries are designated by the City of Toronto. For more details, please refer to this <a href="https://www.toronto.ca/city-government/data-research-maps/neighbourhoods-communities/neighbourhood-profiles/about-toronto-neighbourhoods">website</a></td>
</tr>
<tr class="even">
<td>toronto: Neighbourhood</td>
<td>cdt:nbhdNum</td>
<td>{NBHDNo}</td>
</tr>
<tr class="odd">
<td>NBHDName</td>
<td>toronto: neighbourhood_{_id}</td>
<td>genprop:hasName</td>
<td>{NBHDName}</td>
<td>The name of a neighbourhood.</td>
</tr>
<tr class="even">
<td rowspan="3">TPLNIA</td>
<td>tor:library_site_{_id}</td>
<td>cdt:providesService</td>
<td>cdt:tplnia_serv_ {_id}</td>
<td rowspan="3">This field denotes whether the branch serves a neighbourhood improvement area (1 for yes, 0 for no). A branch serving a NIA may be located inside its boundaries or nearby. NIAs are designated by the City of Toronto. For more details, please refer to this <a href="https://www.toronto.ca/city-government/accountability-operations-customer-service/long-term-vision-plans-and-strategies/toronto-strong-neighbourhoods-strategy-2020">website</a></td>
</tr>
<tr class="odd">
<td>cdt:tplnia_serv_{_id}</td>
<td>rdf:type</td>
<td>hp: LibraryService</td>
</tr>
<tr class="even">
<td>cdt:tplnia_serv_{_id}</td>
<td>genprop:hasName</td>
<td>{TPLNIA}</td>
</tr>
<tr class="odd">
<td rowspan="2">WardNo</td>
<td>toronto:ward_{_id}</td>
<td>rdf:type</td>
<td>toronto:Ward</td>
<td rowspan="2">The ID of the municipal ward associated with the branch.</td>
</tr>
<tr class="even">
<td>toronto:ward_{_id}</td>
<td>cdt:wardNum</td>
<td>{WardNo}</td>
</tr>
<tr class="odd">
<td>WardName</td>
<td>toronto:ward_{_id}</td>
<td>genprop:hasName</td>
<td>{WardName}</td>
<td>The name of the municipal ward.</td>
</tr>
<tr class="even">
<td>Present SiteYear</td>
<td>tor:library_site_{_id}</td>
<td>cdt:openingYear</td>
<td>{PresentSite Year}</td>
<td>The year that the present location of the branch was officially opened to the general public.</td>
</tr>
</tbody>
</table>

Table 2: Mapping Toronto Open Data Portal Library Data to City Digital Twin

### Implementation of Library Data in Mapping TTL

**Script:** [Library.py](https://github.com/csse-uoft/city-digital-twin-ontology/tree/main/Housing%20Potential%20Python)

**URI strategy**

The script generates deterministic URIs under the tor: namespace so that Toronto Public Library (TPL) branches, library sites, and derived service/capacity nodes can be referenced consistently:

**Core library + site objects (TPL and/or OSM)**

- **Library (branch / OSM object):** tor:library\_{id}

  - id is \_id from the TPL CSV, or the numeric part of OSM @id

- **Library site (physical premise):** tor:library_site\_{id}

- **Address node:** tor:addLibrary\_{id}

- **Location node (point geometry):** loc:location\_{id}

**Administrative context**

- **Neighbourhood:** tor:neighbourhood\_{id}

- **Ward:** tor:ward\_{id}

**Service objects and synthetic capacity metrics**

- **Library service instance:** tor:library_service{id}

- **Capacity / usage / availability nodes (and measures):**

  - tor:library_service{id}Capacity, tor:library_service{id}CapacityMeasure

  - tor:library_service{id}CapacityUse, tor:library_service{id}CapacityUseMeasure

  - tor:library_service{id}AvailCapacity, tor:library_service{id}AvailCapacityMeasure

**Auxiliary code/category nodes**

- **Province/state:** contact:state\_{id}

- **State code:** code:state_Code\_{id}

- **Service tier node:** cdt:serviceTier\_{id}

- **Tier code:** code:tierCode\_{id}

**Inputs**

1.  **Toronto Public Library (Toronto Open Data)**

    - tpl-branch-general-information-2023.csv

    - Used to create the base set of TPL branch libraries (IDs, names, branch codes, address, phone, website, floor area, service tier, services provided, lat/long, ward + neighbourhood info, etc.)

2.  **OpenStreetMap libraries (GeoJSON extract)**

    - Library.geojson

    - Used to enrich TPL libraries when a feature name matches a TPL branch name, and to create additional library instances for OSM libraries not present in the TPL dataset.

    - Provides many optional tags (opening hours, wheelchair, internet access, building attributes, etc.) plus geometry.

**Outputs**

- **toronto_libraries.ttl**  
  Contains: library instances, library sites, addresses, location geometries, administrative context (ward/neighbourhood), and OSM-derived enrichment triples.

- **synthetic_libraries.ttl**  
  Contains: synthetic capacity modeling for the library service (capacity, capacity-in-use, and available capacity) derived from branch floor area and a fixed population assumption.

**Step-by-step process**

**Step 1 - Load datasets**

- Reads tpl-branch-general-information-2023.csv into a DataFrame.

- Loads Library.geojson to iterate through OSM features.

**Step 2 - Initialize RDF graphs and bind namespaces**  
Two graphs are created:

- g for the main library/site/address/geometry content

- synthetic for capacity metrics (hasCapacity, capacityInUse, hasAvailableCapacity)

Namespaces are bound (e.g., tor, cdt, org, contact, genprop, loc, geo, hp, i72, res, etc.).

**Step 3 - Create Toronto Public Library organization + class scaffolding**

- Creates a top-level organization node for Toronto Public Library and sets up some subclass relationships (e.g., treating library as a government organization pattern and connecting TorLibraryService as a subclass of library service in the project model).

**Step 4 - Map each TPL branch (core library + site + address + location)**  
For each row in the TPL CSV:

- Create tor:library\_{\_id} as a cdt:Library and assign identifier + name + branch code.

- Filter: if PhysicalBranch != 1, mark not public and skip mapping most branch details (so only physical branches proceed).

- Create address node tor:addLibrary\_{\_id} and parse the Address string into street/street number/city/province + postal code.

- Create phone node and attach the telephone number, and attach the website.

- Create a site node tor:library_site\_{\_id} as cdt:LibrarySite and link it to the library via org:hasSite.

- Add floor area as a structured measurement:

  - hp:hasFloorArea → hp:FloorArea → i72:hasValue → measure node

  - with unit hp:square_foot and numerical value from SquareFootage

- Add additional site attributes from the TPL dataset (parking, computers, opening year, service tier).

**Step 5 - Map “services provided” flags (KidsStop, DIH, etc.)**  
When a service flag is present (value 1), the script:

- Creates a service instance (e.g., tor:kids_stop\_{\_id}) typed as a Toronto-specific library service class,

- Links it from the branch via cdt:providesService,

- Links it to the site via hp:providedFromSite,

- Adds a name for the service instance.

**Step 6 - Create a branch-level library service instance + capacity metrics**  
For each branch, the script creates:

- tor:library_service{\_id} and links it as a service provided by the branch, with hp:providedFromSite to the site.

Then in the synthetic graph, it adds:

- **Capacity** (res:hasCapacity) as a constant (numerical value 1, unit hp:square_metre_per_person)

- **Capacity in use** (res:capacityInUse) as a ratio computed from floor area (converted/approximated) divided by an assumed population constant (55613)

- **Available capacity** (res:hasAvailableCapacity) as (1 − capacityInUse) with an “available capacity” class type (available library population ratio)

**Step 7 - Map neighbourhood + ward context and point geometry (Lat/Long)**  
For each branch, the script:

- Creates tor:neighbourhood\_{\_id} and tor:ward\_{\_id} instances, assigns their names + numeric IDs, and links neighbourhood ↔ ward.

- Creates a point WKT POINT (Long Lat) and stores it on loc:location\_{\_id} via geo:asWKT, linking site → location via loc:hasLocation.

**Step 8 - Enrich TPL entries with matching OSM features, and map extra OSM-only libraries**  
The script iterates through OSM GeoJSON features:

- If an OSM feature’s name matches a known TPL branch, it adds optional site/library properties from OSM (wheelchair access, internet access, building materials, after-hours return, opening hours parsing, etc.).

- If no matching TPL branch exists but an OSM @id exists, it creates a new tor:library\_{id} and tor:library_site\_{id} and maps whatever address/metadata is available from OSM tags.

**Step 9 - Serialize TTL**

- Serializes g to toronto_libraries.ttl

- Serializes synthetic to synthetic_libraries.ttl

**Notes / assumptions**

- **Branch matching between TPL and OSM** is done using a name containment heuristic (OSM name contains the TPL BranchName), so mismatches/near-matches can cause missing enrichments or incorrect matches.

- **Capacity metrics are synthetic** and depend on a fixed assumed population constant (55613) and a simplified conversion/ratio calculation; these should be treated as demo-friendly placeholders unless validated.

- **Only physical branches** (PhysicalBranch == 1) are fully mapped as public branch libraries; other TPL services/collections are skipped after being marked not public.

- **Address parsing** assumes the TPL Address field is a comma-separated string with street and city components; unusual formats may parse imperfectly.

If you want, paste your preferred “Library Implementation” formatting (exact bullet/numbering style like Water), and I’ll match it 1:1 (including your exact heading names and indentation).
