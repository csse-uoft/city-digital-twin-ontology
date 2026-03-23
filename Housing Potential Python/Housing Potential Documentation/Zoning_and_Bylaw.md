# Zoning and Bylaw

This is the ontological representation of Toronto’s zoning by-law
designations and zoning-type constraints, capturing how specific areas
of land are regulated under Toronto Zoning By-law 569-2013. Individual
zoning regulations are represented as instances of the hp:Regulation
class (e.g., tor:zoning_reg\_{OBJECTID}) and are linked to the regulated
land area (e.g., tor:area\_{OBJECTID}) using hp:definedFor. Each land
area is represented as an hp:AdministrativeArea with a geospatial
location (loc:hasLocation) and boundary geometry expressed as WKT
(geo:asWKT).

To represent zoning classification, each regulation designates one or
more zoning types using hp:designatesZoningType, with zoning types
represented as instances such as tor:zone\_{GEN_ZONE},
tor:zone\_{ZN_ZONE}, and tor:zone\_{ZN_STRING}. These are related
through hp:subZoningType to capture the hierarchy from broader zone
categories down to the fully specified zone label. Where applicable,
zoning exceptions and holding provisions are also represented as
additional regulatory structures linked to the relevant zone types.

To represent the built-form and dwelling unit constraints defined by the
zoning by-law (for example, minimum frontage, lot area, height limits,
and maximum units), the mapping creates zoning-type–specific regulation
constraint instances (e.g., tor:{ZN_STRING}\_regulation_constraints) and
links them to the relevant zoning type using opr:forZoningType.
Quantitative constraints are expressed through ISO measurement structure
(i72:hasValue, i72:hasNumericalValue, i72:hasUnit) so units and values
are explicit and machine-interpretable.

This section summarizes how the Toronto zoning by-law dataset (zoning
areas, zone labels, and regulation attributes) and the by-law text
section references are mapped into the City Digital Twin ontology.

The following is a list of namespace prefixes used in the mappings and
ontology definitions that follow:

- bylaw:
  https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Bylaw/

- genprop:
  https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/

- geo: http://www.opengis.net/ont/geosparql#

- hp: http://ontology.eil.utoronto.ca/HPCDM/

- i72: http://ontology.eil.utoronto.ca/ISO21972/iso21972#

- loc:
  https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/

- mer:
  https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Mereology/

- opr:http://www.theworldavatar.com/ontology/ontoplanningregulation/OntoPlanningRegulation.owl#

- rdfs: http://www.w3.org/2000/01/rdf-schema#

- rdf:
  [http://www.w3.org/1999/02/22-rdf-syntax-ns#](http://www.w3.org/1999/02/22-rdf-syntax-ns)

- tor: http://ontology.eil.utoronto.ca/Toronto/Toronto#

- xsd:
  [http://www.w3.org/2001/XMLSchema#](http://www.w3.org/2001/XMLSchema)

This
[dataset](https://data.urbandatacentre.ca/catalogue/city-toronto-zoning-by-law)
defines zones with different land use regulations, along with
specialized limitations on lot dimensions such as frontage and land
area, and development density. Mappings from the dataset’s fields are
grouped into the following categories: (1) definition of bylaw
references, (2) identification of applicable zoning types, and (3)
definition of the zoning type.

The fields identified in Table 1 capture different parts of the bylaw
that are referenced by the dataset. In particular, the section and
chapter identify the relevant parts for the identified zoning type.
These references are useful for referencing the relevant parts of a
document for a restriction.


![Figure 1](https://github.com/csse-uoft/city-digital-twin-ontology/blob/8805fc77c472c008d82c617f019b663efd477a6e/Housing%20Potential%20Python/Housing%20Potential%20Diagrams/Figure%201%20Diagram%20of%20bylaw%20reference%20mapping%20result.png)

Figure 1: Diagram of bylaw reference mapping result

- ZN_STATUS = (Status of the Zone, primarily indicating whether the
  lands have been incorporated into By-law 569-2013 or not.) \[0-4 and 6
  = In the By-law. 5 = Not Part of Zoning By-law 569-2013\]

- Used as a filter; map as follows if {ZN_STATUS} != 5



| **"Zone Categories" Field**               | **Mapping to HPCDM**                        |                             |                                             |           |
|-------------------------------------------|---------------------------------------------|-----------------------------|---------------------------------------------|-----------|
|                                           | **Subject**                                 | **Property**                | **Object**                                  | **Notes** |
|                                           | tor:zoning_by-law_569-2013                  | rdf:type                    | hp:ZoningBylaw                              |           |
|                                           |  tor:zoning_by-law_569-2013                 | bylaw:legislationIdentifier | "ZONING_BY-LAW_569-2013"                    |           |
| ZBL_EXCPTN = (By-law text section number) | tor:zoning_by-law_569-2013                  | mer:hasProperPart           | tor:zoning_by-law_569-2013\_{ZBL_EXCEPTN}   |           |
|                                           | tor:zoning_by-law_569-2013\_{ZBL_EXCEPTN}   | rdf:type                    | hp:ZoiningBylawPart                         |           |
|                                           | tor:zoning_by-law_569-2013\_{ZBL_EXCEPTN}   | genprop:hasIdentifier       | {ZBL_EXCPTN}                                |           |
| ZBL_CHAPTR = (By-law text chapter number) | tor:zoning_by-law_569-2013                  | mer:hasProperPart           | tor:zoning_by-law_569-2013_CH{ZBL_CHAPTR}   |           |
|                                           | tor:zoning_by-law_569-2013_CH{ZBL_CHAPTR}   | rdf:type                    | hp:ZoiningBylawPart                         |           |
|                                           | tor:zoning_by-law_569-2013_CH{ZBL_CHAPTR}   | genprop:hasIdentifier       | {ZBL_CHAPTR}                                |           |
| ZBL_SECTN = (By-law text section number)  | tor:zoning_by-law_569-2013_CH{ZBL_CHAPTR}   | mer:hasProperPart           | tor:zoning_by-law_569-2013_SECTN{ZBL_SECTN} |           |
|                                           | tor:zoning_by-law_569-2013_SECTN{ZBL_SECTN} | rdf:type                    | hp:ZoiningBylawPart                         |           |
|                                           | tor:zoning_by-law_569-2013_SECTN{ZBL_SECTN} | genprop:hasIdentifier       | {ZBL_SECTN}                                 |           |

Table 1: Mapping bylaw references from Toronto "Zone Categories" data


![Figure 2](https://github.com/csse-uoft/city-digital-twin-ontology/blob/8805fc77c472c008d82c617f019b663efd477a6e/Housing%20Potential%20Python/Housing%20Potential%20Diagrams/Figure%202%20Diagram%20of%20zoning%20type%20assignment%20mapping%20result.png)

Figure 2: Diagram of zoning type assignment mapping result

Each row in the table associates a zoning type with a particular area.
This mapping is outlined in Table 2 Note that each of GEN_ZONE, ZN_ZONE,
and ZN_STRING are considered zoning types (at different levels of
abstraction) that apply to the same area. A hold (when applied) is
interpreted as a different zoning type.

This allows for additional specification on the nature of the hold
(e.g., what developments may be permitted/prohibited). On the other
hand, exceptions are identified with respect to the ZN_STRING zoning
type, as they contribute to its interpretation.

ZN_EXCPTN = (This indicates whether a zone has an Exception.) \[Yes (Y)
or No (N)\]

details of the exception(s) are defined furtherby the bylaw (chapter
900) and should be incorported into the definition of the individual
zoning type (ZN_STRING)



<table>
<colgroup>
<col style="width: 14%" />
<col style="width: 20%" />
<col style="width: 14%" />
<col style="width: 27%" />
<col style="width: 22%" />
</colgroup>
<thead>
<tr class="header">
<th rowspan="2"><strong>"Zone Categories" Field</strong></th>
<th colspan="4"><strong>Mapping to HPCDM</strong></th>
</tr>
<tr class="odd">
<th><strong>Subject</strong></th>
<th><strong>Property</strong></th>
<th><strong>Object</strong></th>
<th><strong>Notes</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td rowspan="6">OBJECTID = (Unique system identifier)</td>
<td>tor:zoning_by-law_569-2013</td>
<td>hp:definesRegulation</td>
<td>tor:zoning_reg_{OBJECTID}</td>
<td>#a regulation (part of the bylaw) applies to a specific area
(OBJECTID)</td>
</tr>
<tr class="even">
<td>tor:zoning_reg_{OBJECTID}</td>
<td>rdf:type</td>
<td>hp:Regulation</td>
<td>to add in next iteration</td>
</tr>
<tr class="odd">
<td>tor:zoning_reg_{OBJECTID}</td>
<td>hp:definedIn</td>
<td>tor:zoning_by-law_569-2013</td>
<td rowspan="5"></td>
</tr>
<tr class="even">
<td>tor:zoning_reg_{OBJECTID}</td>
<td>hp:definedFor</td>
<td>tor:area_{OBJECTID}</td>
</tr>
<tr class="odd">
<td>tor:area_{OBJECTID}</td>
<td>rdf:type</td>
<td>hp:AdministrativeArea</td>
</tr>
<tr class="even">
<td>tor:area_{OBJECTID}</td>
<td>loc:hasLocation</td>
<td>tor:area_{OBJECTID}_geometry</td>
</tr>
<tr class="odd">
<td>geometry</td>
<td>tor:area_{OBJECTID}_geometry</td>
<td>geo:asWKT</td>
<td>{geometry}</td>
</tr>
<tr class="even">
<td rowspan="2">GEN_ZONE = (The land use category of the lands within
the zone boundary. Each "zone category" has its own Chapter in the text
of By-law 569-2013.)</td>
<td>tor:zoning_reg_{OBJECTID}</td>
<td>hp:designatesZoningType</td>
<td>tor:zone_{GEN_ZONE}</td>
<td rowspan="2">#the regulation defines a zoning type for the area</td>
</tr>
<tr class="odd">
<td>tor:zone_{GEN_ZONE}</td>
<td>hp:subZoningType</td>
<td>tor:zone_{ZN_ZONE}</td>
</tr>
<tr class="even">
<td rowspan="3"><p> </p>
<p>ZN_ZONE = (The land use category of the lands within the zone
boundary. Each "zone category" has its own Chapter in the text of By-law
569-2013.) [Zoned destination of the zone limited by GEN_ZONE.</p></td>
<td>tor:zoning_reg_{OBJECTID}</td>
<td>hp:designatesZoningType</td>
<td>tor:zone_{ZN_ZONE}</td>
<td></td>
</tr>
<tr class="odd">
<td>tor:zone_{ZN_ZONE}</td>
<td>hp:subZoningType</td>
<td>tor:zone_{ZN_STRING}</td>
<td rowspan="2"></td>
</tr>
<tr class="even">
<td>tor:zone_{ZN_ZONE}</td>
<td>hp:definedIn</td>
<td>tor:zoning_by-law_569-2013_SECTN{ZBL_SECTN}</td>
</tr>
<tr class="odd">
<td>ZN_STRING = (Complete label of the zone.)</td>
<td>tor:zoning_reg_{OBJECTID}</td>
<td>hp:designatesZoningType</td>
<td>tor:zone_{ZN_STRING}</td>
<td>#values listed in this dataset (and denoted in the ZN_STRING) are
defined as part of the zone label, which is essentially a more specific
zone (subZoning) for the ZN_ZONE</td>
</tr>
<tr class="even">
<td>EXCPTN_NO = (This is the Exception Number for the zone if one
exists. The exception number is prefaced by the letter "x" in the zone
label. Each zone has its own series of exception numbers, starting at 1,
so the exception number must be read in conjunction with the respective
zone symbol.)</td>
<td>tor:zone_{ZN_STRING}</td>
<td>hp:definesZoningException</td>
<td>tor:{ZN_ZONE}_{EXCPTN_NO}</td>
<td rowspan="2">#provides a pointer to any exception(s) to the ZN_ZONE
regulations applied to this particular zone (ZN_STRING); these are
incorporated into the definition of ZN_STRING</td>
</tr>
<tr class="odd">
<td>ZBL_EXCPTN = (By-law text section number)</td>
<td>tor:{ZN_ZONE}_{EXCPTN_NO}</td>
<td>hp:definedIn</td>
<td>tor:zoning_by-law_569-2013_{ZBL_EXCEPTN}</td>
</tr>
<tr class="even">
<td rowspan="3">ZN_HOLDING = (To indicate whether there is a HOLDING
status for the zone. The zone label will be prefaced by the letter (H).
These are not common, and when used, a Holding Zone is most often
applied to specific sites.) [Yes (Y) or No (N)]</td>
<td>tor:holding_reg_{OBJECT ID}</td>
<td>rdf:type</td>
<td>hp:Regulation</td>
<td>#holdings aren't zones and regulations defined within the bylaw
(though they are interpreted as zones); they are temporary zones applied
to a particular area</td>
</tr>
<tr class="odd">
<td>tor:holding_reg_{OBJECT ID}</td>
<td>hp:definedFor</td>
<td>tor:area_{OBJECTID}</td>
<td rowspan="3">#details of tor:holding_zone are defined furtherby the
bylaw</td>
</tr>
<tr class="even">
<td>tor:holding_reg_{OBJECT ID}</td>
<td>hp:designatesZoningType</td>
<td>tor:holding_zone</td>
</tr>
<tr class="odd">
<td>HOLDING_ID (Holding Number if it exists.)</td>
<td>tor:holding_reg_{OBJECT ID}</td>
<td>genprop:hasIdentifier</td>
<td>{HOLDING_ID}</td>
</tr>
</tbody>
</table>

Table 2: Mapping zoning type assignments in Toronto



The zoning type is defined with the instantiation of any applicable
regulations. Here, we outline example mappings for frontage, unit, and
density regulations defined for a zoning type. The complete mapping
specification is provided in the supplementary file. Table 3 specifies
the mapping to capture any frontage regulations for the zoning type. A
new Regulation is introduced that applies to the zoning, the regulation
specifies a *requirement* of some Frontage quantity, associated with the
“FRONTAGE” value provided in the data. The mapping encodes the intended
unit of measure (metres), along with the population that the regulation
applies to. In this case, an extension is introduced to define the
population of lots in Toronto (TorontoLotPopulation). In practice, the
required classes could be identified and defined in a separate extension
to the HPCDM, such that they could be referenced directly in any mapping
implementation.

![Figure 3](https://github.com/csse-uoft/city-digital-twin-ontology/blob/8805fc77c472c008d82c617f019b663efd477a6e/Housing%20Potential%20Python/Housing%20Potential%20Diagrams/Figure%203%20Diagram%20of%20Frontage%20restriction%20mapping%20result.png)

Figure 3: Diagram of Frontage restriction mapping result



<table>
<colgroup>
<col style="width: 14%" />
<col style="width: 20%" />
<col style="width: 14%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<thead>
<tr class="header">
<th rowspan="2"><strong>"Zone Categories" fields</strong></th>
<th colspan="4"><strong>Mapping to HPCDM</strong></th>
</tr>
<tr class="odd">
<th><strong>Subject</strong></th>
<th><strong>Property</strong></th>
<th><strong>Object</strong></th>
<th><strong>Notes</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td rowspan="15"><p>FRONTAGE = (The required minimum Lot Frontage in the
zone, and is a numeric value prefaced by the letter "f" within a
residential zone label.) [Unit = metres.]</p>
<p> </p>
<p> </p>
<p> </p>
<p> </p>
<p> </p>
<p> </p>
<p> </p>
<p> </p>
<p> </p>
<p> </p>
<p> </p></td>
<td>tor:{ZN_STRING}_regulation_constraints</td>
<td>rdf:type</td>
<td>hp:Regulation</td>
<td rowspan="13"></td>
</tr>
<tr class="even">
<td>tor:{ZN_STRING}_regulation_constraints</td>
<td>genprop:hasName</td>
<td>Zone String {ZN_STRING}</td>
</tr>
<tr class="odd">
<td>tor:{ZN_STRING}_regulation_constraints</td>
<td>hp:definedIn</td>
<td>tor:zoning_by-law_569-2013</td>
</tr>
<tr class="even">
<td>tor:{ZN_STRING}_regulation_constraints</td>
<td>opr:forZoningType</td>
<td>tor:zone_{ZN_STRING}</td>
</tr>
<tr class="odd">
<td>tor:{ZN_STRING}_regulation_constraints</td>
<td>hp:specifiesConstraint</td>
<td>tor:min_frontage_{ZN_STRING}</td>
</tr>
<tr class="even">
<td>tor:min_frontage_{ZN_STRING}</td>
<td>rdf:type</td>
<td>hp:QuantityRequirement</td>
</tr>
<tr class="odd">
<td>tor:min_frontage_{ZN_STRING}</td>
<td>i72:hasValue</td>
<td>tor:min_frontage_{ZN_STRING}_specification</td>
</tr>
<tr class="even">
<td>tor:min_frontage_{ZN_STRING}_specification</td>
<td>i72:hasNumericalValue</td>
<td>{FRONTAGE}</td>
</tr>
<tr class="odd">
<td>tor:min_frontage_{ZN_STRING}_specification</td>
<td>i72:hasUnit</td>
<td>hp:metres</td>
</tr>
<tr class="even">
<td>tor:min_frontage_{ZN_STRING}</td>
<td>hp:specifiesMinimumFor</td>
<td>tor:zone_{ZN_STRING}_lots_min_frontage</td>
</tr>
<tr class="odd">
<td>tor:zone_{ZN_STRING}_lots_min_frontage</td>
<td>rdf:type</td>
<td>hp:Minimum</td>
</tr>
<tr class="even">
<td>tor:zone_{ZN_STRING}_lots_min_frontage</td>
<td>i72:parameter_of_var</td>
<td>tor:frontage_var</td>
</tr>
<tr class="odd">
<td>tor:zone_{ZN_STRING}_lots_min_frontage</td>
<td>hp:minimumOf</td>
<td>tor:lot_population_in_zone_{ZN_STRING}</td>
</tr>
<tr class="even">
<td>tor:frontage_var</td>
<td>i72:hasName</td>
<td>"hp:hasFrontage"</td>
<td rowspan="2">#we may actually want to distinguish between the object
class too (since a lot could have different frontages, according to
different municipalities); I think this is a general requirement - to
restrict parameters more precisely - that should be addressed by
21972</td>
</tr>
<tr class="odd">
<td>tor:lot_population_in_zone_{ZN_STRING}</td>
<td>rdf:type</td>
<td>tor:TorontoLotPopulation_Zone{ZN_STRING}</td>
</tr>
</tbody>
</table>
Table 3: Mapping the defined Frontage restriction for lots in the zone
in Toronto


Table 4 specifies the mapping to formalize the maximum number of
dwelling units per lot for a particular zone. It is defined as another
Regulation that applies to the identified zoning type. The allowance is
specified as a quantity that represents the cardinality of the
population of dwelling units in a particular lot. The classes used to
represent the quantity associated with the regulation
(LotNumberOfDwellings and DwellingUnitPopulationInALot) are formulated
in the HPCDM. Any characteristics not covered by the model could be
defined in an extension.



<table>
<colgroup>
<col style="width: 14%" />
<col style="width: 21%" />
<col style="width: 14%" />
<col style="width: 27%" />
<col style="width: 21%" />
</colgroup>
<thead>
<tr class="header">
<th rowspan="2"><strong>"Zone Categories" fields</strong></th>
<th colspan="4"><strong>Mapping to HPCDM</strong></th>
</tr>
<tr class="odd">
<th><strong>Subject</strong></th>
<th><strong>Property</strong></th>
<th><strong>Object</strong></th>
<th><strong>Notes</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td rowspan="18"><p>UNITS = (The permitted maximum number of Dwelling
Units allowed on a lot in the zone, and is a numeric value prefaced by
the letter "u" in a residential zone.)</p>
<p> </p></td>
<td>tor:{ZN_STRING}_regulation_constraints</td>
<td>rdf:type</td>
<td>hp:Regulation</td>
<td rowspan="12">Note: no data published</td>
</tr>
<tr class="even">
<td>tor:{ZN_STRING}_regulation_constraints</td>
<td>hp:definedIn</td>
<td>tor:zoning_by-law_569-2013</td>
</tr>
<tr class="odd">
<td>tor:{ZN_STRING}_regulation_constraints</td>
<td>opr:forZoningType</td>
<td>tor:zone_{ZN_STRING}</td>
</tr>
<tr class="even">
<td>tor:{ZN_STRING}_regulation_constraints</td>
<td>hp:specifiesConstraint</td>
<td>tor:max_units_{ZN_STRING}</td>
</tr>
<tr class="odd">
<td>tor:max_units_{ZN_STRING}</td>
<td>rdf:type</td>
<td>hp:QuantityAllowance</td>
</tr>
<tr class="even">
<td>tor:max_units_{ZN_STRING}</td>
<td>i72:hasValue</td>
<td>tor:max_units_{ZN_STRING}_specification</td>
</tr>
<tr class="odd">
<td>tor:max_units_{ZN_STRING}_specification</td>
<td>i72:hasNumericalValue</td>
<td>{UNITS}</td>
</tr>
<tr class="even">
<td>tor:max_units_{ZN_STRING}_specification</td>
<td>i72:hasUnit</td>
<td>i72:population_cardinality_unit</td>
</tr>
<tr class="odd">
<td>tor:max_units_{ZN_STRING}</td>
<td>hp:specifiesMaximumFor</td>
<td>tor:zone_{ZN_STRING}_lots_max_dwelling</td>
</tr>
<tr class="even">
<td>tor:zone_{ZN_STRING}_lots_max_dwelling</td>
<td>rdf:type</td>
<td>hp:Maximum</td>
</tr>
<tr class="odd">
<td>tor:zone_{ZN_STRING}_lots_max_dwelling</td>
<td>i72:parameter_of_var</td>
<td>tor:num_dwellings_var</td>
</tr>
<tr class="even">
<td>tor:zone_{ZN_STRING}_lots_max_dwelling</td>
<td>hp:maximumOf</td>
<td>tor:lot_population_in_zone_{ZN_STRING}</td>
</tr>
<tr class="odd">
<td>tor:num_dwellings_var</td>
<td>i72:hasName</td>
<td>hp:hasNumDwellings</td>
<td>hasNumDwellings originally plannedto be defined in Toronto
extension</td>
</tr>
<tr class="even">
<td>tor:lot_population_in_zone_{ZN_STRING}</td>
<td>rdf:type</td>
<td>tor:TorontoLotPopulation_Zone{ZN_STRING}</td>
<td rowspan="5">#alternatively could define based on the zone area
specified by the geometry, e.g. tor:area_{OBJECTID}_geometry</td>
</tr>
<tr class="odd">
<td>tor:TorontoLotPopulation_Zone{ZN_STRING}</td>
<td>rdfs:subClassOf</td>
<td>tor:TorontoLotPopulation</td>
</tr>
<tr class="even">
<td>tor:TorontoLotPopulation_Zone{ZN_STRING}</td>
<td>i72:located_in</td>
<td>https://www.geonames.org/6167865/toronto.html</td>
</tr>
<tr class="odd">
<td>tor:TorontoLotPopulation_Zone{ZN_STRING}</td>
<td>i72:defined_by only</td>
<td>hp:Lot and hp:hasZone value tor:zone_{ZN_STRING}</td>
</tr>
<tr class="even">
<td>tor:lot_population</td>
<td>rdf:type</td>
<td>tor:TorontoLotPopulation</td>
</tr>
</tbody>
</table>
Table 4: Mapping the maximum number of units per lot in the zone in
Toronto


Table 5 specifies the mapping to represent a regulation on density in
the zone. This regulation specifies a limit on floor space index (FSI)
and so is defined as a LotFSI value. LotFSI is defined in the HPCDM as a
ratio of gross floor area to lot area.


<table>
<colgroup>
<col style="width: 14%" />
<col style="width: 21%" />
<col style="width: 14%" />
<col style="width: 24%" />
<col style="width: 24%" />
</colgroup>
<thead>
<tr class="header">
<th rowspan="2"><strong>"Zone Categories" fields</strong></th>
<th colspan="4"><strong>Mapping to HPCDM</strong></th>
</tr>
<tr class="odd">
<th><strong>Subject</strong></th>
<th><strong>Property</strong></th>
<th><strong>Object</strong></th>
<th><strong>Notes</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td rowspan="14"><p>DENSITY = (The permitted maximum Density in the zone
by FSI (floor space index), and is a numeric value prefaced by the
letter "d" in residential zones.)</p>
<p> </p>
<p> </p>
<p> </p>
<p> </p>
<p> </p>
<p> </p>
<p> </p>
<p> </p>
<p> </p>
<p> </p>
<p> </p></td>
<td>tor:{ZN_STRING}_regulation_constraints</td>
<td>rdf:type</td>
<td>hp:Regulation</td>
<td rowspan="14"></td>
</tr>
<tr class="even">
<td>tor:{ZN_STRING}_regulation_constraints</td>
<td>hp:definedIn</td>
<td>tor:zoning_by-law_569-2013</td>
</tr>
<tr class="odd">
<td>tor:{ZN_STRING}_regulation_constraints</td>
<td>opr:forZoningType</td>
<td>tor:zone_{ZN_STRING}</td>
</tr>
<tr class="even">
<td>tor:{ZN_STRING}_regulation_constraints</td>
<td>hp:specifiesConstraint</td>
<td>tor:max_density_{ZN_STRING}</td>
</tr>
<tr class="odd">
<td>tor:max_density_{ZN_STRING}</td>
<td>rdf:type</td>
<td>hp:QuantityAllowance</td>
</tr>
<tr class="even">
<td>tor:max_density_{ZN_STRING}</td>
<td>i72:hasValue</td>
<td>tor:max_density_{ZN_STRING}_specification</td>
</tr>
<tr class="odd">
<td>tor:max_density_{ZN_STRING}_specification</td>
<td>i72:hasNumericalValue</td>
<td>{DENSITY}</td>
</tr>
<tr class="even">
<td>tor:max_density_{ZN_STRING}</td>
<td>hp:specifiesMaximumFor</td>
<td>tor:zone_{ZN_STRING}_lots_max_density</td>
</tr>
<tr class="odd">
<td>tor:zone_{ZN_STRING}_lots_max_density</td>
<td>rdf:type</td>
<td>hp:Maximum</td>
</tr>
<tr class="even">
<td>tor:zone_{ZN_STRING}_lots_max_density</td>
<td>i72:parameter_of_var</td>
<td>tor:density_var</td>
</tr>
<tr class="odd">
<td>tor:zone_{ZN_STRING}_lots_max_density</td>
<td>hp:maximumOf</td>
<td>tor:lot_population_in_zone_{ZN_STRING}</td>
</tr>
<tr class="even">
<td>tor:density_var</td>
<td>i72:hasName</td>
<td>"hp:hasFSI"</td>
</tr>
<tr class="odd">
<td>tor:lot_population_in_zone_{ZN_STRING}</td>
<td>rdf:type</td>
<td>tor:TorontoLotPopulation_Zone{ZN_STRING}</td>
</tr>
<tr class="even">
<td>tor:TorontoLotPopulation_Zone{ZN_STRING}</td>
<td>rdfs:subClassOf</td>
<td>tor:TorontoLotPopulation</td>
</tr>
</tbody>
</table>
Table 5: Mapping of density regulation in a zone in Toronto


Table 6 specifies the mapping to represent [Zoning Height
Overlay](https://open.toronto.ca/dataset/zoning-by-law/). The same
general approach can be defined for any area-based regulations defined
independently of zoning types (not incorporated in the zoning area
layer)


| **"Zone Categories" Field** | **Mapping to HPCDM**                       |                        |                                            |                                                                 |
|-----------------------------|--------------------------------------------|------------------------|--------------------------------------------|-----------------------------------------------------------------|
|                             | **Subject**                                | **Property**           | **Object**                                 | **Notes**                                                       |
| \_id                        | tor:height_zone{\_id}                      | rdf:type               | hp:Regulation                              |                                                                 |
|                             | tor:height_zone{\_id}                      | genprop:hasName        | "Height Regulation {\_id}"                 |                                                                 |
|                             | tor:zoning_by-law_569-2013                 | hp:definesRegulation   | tor:height_zone{\_id}                      |                                                                 |
| geometry                    | tor:height_zone{\_id}                      | hp:definedFor          | tor:height_zone{\_id}Area                  | definition of the area that the regulation applies to           |
|                             | tor:height_zone{\_id}Area                  | rdf:type               | hp:AdministrativeArea                      |                                                                 |
|                             | tor:height_zone{\_id}Area                  | loc:hasLocation        | tor:height_zone{\_id}AreaLoc               |                                                                 |
|                             | tor:height_zone{\_id}AreaLoc               | geo:asWKT              | {geometry}                                 |                                                                 |
|                             | tor:height_zone{\_id}                      | hp:specifiesConstraint | tor:height_zone{\_id}HeightConstraint      |                                                                 |
|                             | tor:height_zone{\_id}HeightConstraint      | rdf:type               | hp:QuantityAllowance                       |                                                                 |
|                             | tor:height_zone{\_id}HeightConstraint      | i72:hasValue           | tor:height_zone{\_id}HeightConstraintValue |                                                                 |
| HT_LABEL                    | tor:height_zone{\_id}HeightConstraintValue | i72:hasNumericalValue  | {HT_LABEL}                                 | the maximum height in metres                                    |
|                             | tor:height_zone{\_id}HeightConstraintValue | i72:hasUnit            | i72:metre                                  |                                                                 |
|                             | tor:height_zone{\_id}HeightConstraint      | hp:specifiesMaximumFor | tor:height_zone{\_id}MaxHeight             | definition of the constrained property (building height)        |
|                             | tor:height_zone{\_id}MaxHeight             | rdf:type               | hp:Maximum                                 | Can define this population subclass in further detail if needed |
|                             | tor:height_zone{\_id}MaxHeight             | hp:maximumOf           | tor:buildingPopulationHeightZone{\_id}     |                                                                 |
|                             | tor:buildingPopulationHeightZone{\_id}     | rdf:type               | tor:BuildingPopulation                     |                                                                 |
|                             | tor:height_zone{\_id}MaxHeight             | i72:parameter_of_var   | tor:height_zone{\_id}BuildingHeight        |                                                                 |
|                             | tor:height_zone{\_id}BuildingHeight        | i72:hasName            | "hp:hasBuildngHeight"                      |                                                                 |
|                             | tor:BuildingPopulation                     | rdfs:subClassOf        | i72:Population                             |                                                                 |
Table 6: Mapping of Zoning Height Overlay in Toronto


## 

## Implementation of ORN Data Mapping to TTL 

**Scripts:** [ZoningAreaToronto.py and
HeightZoning.py.](https://github.com/csse-uoft/city-digital-twin-ontology/tree/main/Housing%20Potential%20Python)

**URI strategy**

The scripts generate deterministic URIs under the tor: namespace so
zoning areas, zoning types, and regulations can be referenced
consistently.

**By-law + by-law parts**

- Zoning by-law: tor:zoning_by-law_569-2013

- Chapter nodes: tor:zoning_by-law_569-2013_CH{ZBL_CHAPT}

- Section nodes: tor:zoning_by-law_569-2013_SECTN{ZBL_SECTN}

- Exception part nodes: tor:zoning_by-law_569-2013\_{ZBL_EXCPTN}

**Area + regulation assignment (per zoning polygon row)**

- Regulation: tor:zoning_reg\_{\_id}

- Area (regulated area): tor:area\_{\_id}

- Area geometry node: tor:area\_{\_id}\_geometry

**Zoning type hierarchy**

- General zone: tor:zone\_{GEN_ZONE}

- Mid zone: tor:zone\_{ZN_ZONE}

- Full zone label: tor:zone\_{ZN_STRING}  
  (Constructed using slugify(...) in the script.)

**Zoning-type constraint regulations (per ZN_STRING, when values
exist)**

- Shared constraint regulation container:
  tor:{ZN_STRING}\_regulation_constraints

- Example constraint nodes + specs:

  - Frontage: tor:min_frontage\_{ZN_STRING},
    tor:min_frontage\_{ZN_STRING}\_specification

  - Lot area: tor:min_area\_{ZN_STRING},
    tor:min_area\_{ZN_STRING}\_specification

  - Max units: tor:max_units\_{ZN_STRING},
    tor:max_units\_{ZN_STRING}\_specification

  - Density: tor:max_density\_{ZN_STRING},
    tor:max_density\_{ZN_STRING}\_specification

  - FSI / percent FSI constraints: tor:{ZN_STRING}\_fsi_total,
    tor:{ZN_STRING}\_comm_fsi, tor:{ZN_STRING}\_res_fsi, etc.

  - Area-units ratio: tor:{ZN_STRING}\_area_units,
    tor:min_area_units\_{ZN_STRING},
    tor:min_area_units\_{ZN_STRING}\_measure

**Holding + exception structures**

- Holding regulation: tor:holding_reg\_{\_id}

- Holding zone type node: tor:holding_zone

- Exception regulation pointer: tor:{ZN_ZONE}\_{EXCPTN_NO}

**Height overlay (separate dataset)**

- Height regulation: tor:height_zone{\_id}

- Height regulated area: tor:height_zone{\_id}Area

- Height area location node: tor:height_zone{\_id}AreaLoc

- Height constraint nodes: tor:height_zone{\_id}HeightConstraint,
  tor:height_zone{\_id}HeightConstraintValue

- Max structure: tor:height_zone{\_id}MaxHeight,
  tor:height_zone{\_id}BuildingHeight

- Population: tor:buildingPopulationHeightZone{\_id}

**Inputs**

**1) Toronto Open Data “zoning-by-law” dataset (zoning areas +
attributes + geometry)**

- Retrieved programmatically from the Toronto Open Data CKAN endpoint
  (package_show → datastore dump).

- Key fields used include: \_id, ZN_STATUS, geometry, GEN_ZONE, ZN_ZONE,
  ZN_STRING, ZN_HOLDING, HOLDING_ID, ZN_EXCPTN, EXCPTN_NO, ZBL_CHAPT,
  ZBL_SECTN, ZBL_EXCPTN, and numeric constraint fields like FRONTAGE,
  ZN_AREA, UNITS, DENSITY, FSI_TOTAL, etc.

**2) Zoning height overlay dataset**

- Local CSV: zoning-height-overlay-4326.csv (read by HeightZoning.py).

- Key fields used: \_id, HT_LABEL, geometry.

**Outputs**

- **toronto_zone.ttl** (from ZoningAreaToronto.py)  
  Contains: zoning by-law node + parts, zoning regulations per area,
  zoning type hierarchy, holding/exception links, and zoning-type
  constraint regulations with ISO measurements and units.

- **Height.ttl** (from HeightZoning.py)  
  Contains: height overlay regulations, regulated areas + geometries,
  height constraint quantities (metres), and maximum structures for
  building height.

**Step-by-step process**

**Zoning areas + by-law references (ZoningAreaToronto.py)**

**Step 1 - Download and load the zoning dataset**  
The script queries the Toronto Open Data CKAN API to locate the
datastore-active resource for “zoning-by-law”, then downloads the
datastore dump into a DataFrame.

**Step 2 - Initialize RDF graph + bind namespaces**  
A single RDF graph is created and key namespaces are bound (tor, hp,
geo, opr, mer, bylaw, loc, i72, genprop).

**Step 3 - Create global by-law and modeling scaffolding**  
The script creates tor:zoning_by-law_569-2013 as hp:ZoningBylaw, sets a
bylaw:legislationIdentifier, and defines a set of “variable” resources
used to parameterize minimum/maximum restrictions (frontage, area,
units, density). It also initializes population scaffolding used for
constraints.

**Step 4 - Iterate zoning rows, skip non-by-law areas**  
Rows with ZN_STATUS == 5 are skipped. For each remaining row, the script
mints a regulation tor:zoning_reg\_{\_id} and area tor:area\_{\_id}, and
links regulation → area using hp:definedFor and regulation → by-law
using hp:definedIn.

**Step 5 - Geometry mapping**  
Each area geometry is parsed from the geometry JSON, validated/fixed if
necessary, converted to WKT, asserted via geo:asWKT on
tor:area\_{\_id}\_geometry, and linked via loc:hasLocation.

**Step 6 - Zoning type hierarchy + assignment**  
For each row, GEN_ZONE, ZN_ZONE, and ZN_STRING are each treated as
zoning types designated by the regulation (hp:designatesZoningType), and
linked by hp:subZoningType to represent the hierarchy (GEN → ZN_ZONE →
ZN_STRING).

**Step 7 - By-law part references**  
If present, chapter/section/exception references are created as
hp:ZoningBylawPart nodes, linked using mer:hasProperPart, and
identifiers recorded with genprop:hasIdentifier. The mid-level zone
(ZN_ZONE) is linked to the section via hp:definedIn.

**Step 8 - Holdings and exceptions**  
Holdings create a separate regulation tor:holding_reg\_{\_id} applying
to the area and pointing to a holding zone type. Exceptions create an
exception pointer node and link it from the ZN_STRING zoning type.

**Step 9 - Zoning-type constraints (numeric controls)**  
For each numeric field that exists (frontage, lot area, max units,
density, FSI totals and breakdowns, etc.), the script creates or reuses
a zoning-type constraint regulation node (e.g.,
tor:{ZN_STRING}\_regulation_constraints), links it to the zoning type
(opr:forZoningType), names it (genprop:hasName), and attaches
constraint/allowance structures with ISO21972 measurements
(i72:hasValue, i72:hasNumericalValue, i72:hasUnit). Units are asserted
using i72:metre, i72:square_metre, and i72:population_cardinality_unit
as appropriate.

**Step 10 - Serialize Turtle**  
The final graph is serialized to toronto_zone.ttl.

**Height overlay (HeightZoning.py)**

**Step 1 - Load height overlay CSV and initialize graph**  
The script reads zoning-height-overlay-4326.csv, binds namespaces, and
creates tor:zoning_by-law_569-2013 as the container by-law node
reference for hp:definesRegulation.

**Step 2 - Geometry parsing and WKT conversion**  
Each row’s geometry is parsed, validated/fixed, converted to WKT, and
asserted on tor:height_zone{\_id}AreaLoc via geo:asWKT.

**Step 3 - Create regulation + constraint structure**  
For each \_id, the script creates tor:height_zone{\_id} as
hp:Regulation, links it into the by-law (hp:definesRegulation), links it
to its administrative area (hp:definedFor), and adds a
hp:QuantityAllowance constraint with an ISO measurement node containing
the maximum height value and unit i72:metre. It also builds the
“maximum” structure over a building population and parameter-of-var
nodes.

**Step 4 - Serialize Turtle**  
The graph is serialized to Height.ttl.

**Notes / assumptions**

- ZoningAreaToronto.py pulls data live from the Toronto Open Data CKAN
  endpoint; running the script later may reflect dataset updates
  (schema/values) in the output TTL.

- All area boundaries and overlays assume valid GeoJSON in the geometry
  column; invalid shapes are repaired using make_valid when possible.

- The zoning-type naming currently uses slugify(zn_str) in the
  genprop:hasName literal for the constraint regulation node; if you
  want the *original* ZN_STRING preserved in the label, the literal
  should use zn_str directly (without slugifying).
