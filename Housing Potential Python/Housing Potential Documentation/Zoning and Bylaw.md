# Zoning and Bylaw

This is the ontological representation of Toronto's zoning by-law
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
and maximum units), the mapping creates zoning-type--specific regulation
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

-   bylaw:
    https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Bylaw/

-   genprop:
    https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/

-   geo: http://www.opengis.net/ont/geosparql#

-   hp: http://ontology.eil.utoronto.ca/HPCDM/

-   i72: http://ontology.eil.utoronto.ca/ISO21972/iso21972#

-   loc:
    https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/

-   mer:
    https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Mereology/

opr:
http://www.theworldavatar.com/ontology/ontoplanningregulation/OntoPlanningRegulation.owl#

-   rdfs: http://www.w3.org/2000/01/rdf-schema#

-   rdf:
    [http://www.w3.org/1999/02/22-rdf-syntax-ns#](http://www.w3.org/1999/02/22-rdf-syntax-ns)

-   tor: http://ontology.eil.utoronto.ca/Toronto/Toronto#

-   xsd:
    [http://www.w3.org/2001/XMLSchema#](http://www.w3.org/2001/XMLSchema)

This
[dataset](https://data.urbandatacentre.ca/catalogue/city-toronto-zoning-by-law)
defines zones with different land use regulations, along with
specialized limitations on lot dimensions such as frontage and land
area, and development density. Mappings from the dataset's fields are
grouped into the following categories: (1) definition of bylaw
references, (2) identification of applicable zoning types, and (3)
definition of the zoning type.

The fields identified in Table 1 capture different parts of the bylaw
that are referenced by the dataset. In particular, the section and
chapter identify the relevant parts for the identified zoning type.
These references are useful for referencing the relevant parts of a
document for a restriction.

![A screenshot of a computer screen AI-generated content may be
incorrect.](./image1.png){width="3.6769225721784777in"
height="2.770262467191601in"}

Figure 1: Diagram of bylaw reference mapping result

-   ZN_STATUS = (Status of the Zone, primarily indicating whether the
    lands have been incorporated into By-law 569-2013 or not.) \[0-4 and
    6 = In the By-law. 5 = Not Part of Zoning By-law 569-2013\]

-   Used as a filter; map as follows if {ZN_STATUS} != 5

  ------------------------------------------------------------------------------------------------------------------------------------------------------
  **\"Zone       **Mapping to HPCDM**                                                                                                      
  Categories\"                                                                                                                             
  Field**                                                                                                                                  
  -------------- --------------------------------------------- ----------------------------- --------------------------------------------- -------------
                 **Subject**                                   **Property**                  **Object**                                    **Notes**

                 tor:zoning_by-law_569-2013                    rdf:type                      hp:ZoningBylaw                                

                  tor:zoning_by-law_569-2013                   bylaw:legislationIdentifier   \"ZONING_BY-LAW_569-2013\"                    

  ZBL_EXCPTN =   tor:zoning_by-law_569-2013                    mer:hasProperPart             tor:zoning_by-law_569-2013\_{ZBL_EXCEPTN}     
  (By-law text                                                                                                                             
  section                                                                                                                                  
  number)                                                                                                                                  

                 tor:zoning_by-law_569-2013\_{ZBL_EXCEPTN}     rdf:type                      hp:ZoiningBylawPart                           

                 tor:zoning_by-law_569-2013\_{ZBL_EXCEPTN}     genprop:hasIdentifier         {ZBL_EXCPTN}                                  

  ZBL_CHAPTR =   tor:zoning_by-law_569-2013                    mer:hasProperPart             tor:zoning_by-law_569-2013_CH{ZBL_CHAPTR}     
  (By-law text                                                                                                                             
  chapter                                                                                                                                  
  number)                                                                                                                                  

                 tor:zoning_by-law_569-2013_CH{ZBL_CHAPTR}     rdf:type                      hp:ZoiningBylawPart                           

                 tor:zoning_by-law_569-2013_CH{ZBL_CHAPTR}     genprop:hasIdentifier         {ZBL_CHAPTR}                                  

  ZBL_SECTN =    tor:zoning_by-law_569-2013_CH{ZBL_CHAPTR}     mer:hasProperPart             tor:zoning_by-law_569-2013_SECTN{ZBL_SECTN}   
  (By-law text                                                                                                                             
  section                                                                                                                                  
  number)                                                                                                                                  

                 tor:zoning_by-law_569-2013_SECTN{ZBL_SECTN}   rdf:type                      hp:ZoiningBylawPart                           

                 tor:zoning_by-law_569-2013_SECTN{ZBL_SECTN}   genprop:hasIdentifier         {ZBL_SECTN}                                   
  ------------------------------------------------------------------------------------------------------------------------------------------------------

  : Table 1: Mapping bylaw references from Toronto \"Zone Categories\"
  data

![A screenshot of a computer screen AI-generated content may be
incorrect.](./image2.png){width="6.5in"
height="2.8666666666666667in"}

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

+---------+-------------+---------+-------------------+--------------+
| *       | **Mapping   |         |                   |              |
| *\"Zone | to HPCDM**  |         |                   |              |
| Categ   |             |         |                   |              |
| ories\" |             |         |                   |              |
| Field** |             |         |                   |              |
+=========+=============+=========+===================+==============+
|         | **Subject** | **Pro   | **Object**        | **Notes**    |
|         |             | perty** |                   |              |
+---------+-------------+---------+-------------------+--------------+
| O       | tor:        | hp:def  | tor:zonin         | #a           |
| BJECTID | zoning_by-l | inesReg | g_reg\_{OBJECTID} | regulation   |
| =       | aw_569-2013 | ulation |                   | (part of the |
| (Unique |             |         |                   | bylaw)       |
| system  |             |         |                   | applies to a |
| iden    |             |         |                   | specific     |
| tifier) |             |         |                   | area         |
|         |             |         |                   | (OBJECTID)   |
+---------+-------------+---------+-------------------+--------------+
|         | tor:        | r       | hp:Regulation     | to add in    |
|         | zoning_reg\ | df:type |                   | next         |
|         | _{OBJECTID} |         |                   | iteration    |
+---------+-------------+---------+-------------------+--------------+
|         | tor:        | hp:de   | tor:zonin         |              |
|         | zoning_reg\ | finedIn | g_by-law_569-2013 |              |
|         | _{OBJECTID} |         |                   |              |
+---------+-------------+---------+-------------------+--------------+
|         | tor:        | hp:def  | tor               |              |
|         | zoning_reg\ | inedFor | :area\_{OBJECTID} |              |
|         | _{OBJECTID} |         |                   |              |
+---------+-------------+---------+-------------------+--------------+
|         | tor:area\   | r       | hp:A              |              |
|         | _{OBJECTID} | df:type | dministrativeArea |              |
+---------+-------------+---------+-------------------+--------------+
|         | tor:area\   | l       | tor:area\_{OB     |              |
|         | _{OBJECTID} | oc:hasL | JECTID}\_geometry |              |
|         |             | ocation |                   |              |
+---------+-------------+---------+-------------------+--------------+
| g       | tor:area    | ge      | {geometry}        |              |
| eometry | \_{OBJECTID | o:asWKT |                   |              |
|         | }\_geometry |         |                   |              |
+---------+-------------+---------+-------------------+--------------+
| G       | tor:        | hp      | tor               | #the         |
| EN_ZONE | zoning_reg\ | :design | :zone\_{GEN_ZONE} | regulation   |
| = (The  | _{OBJECTID} | atesZon |                   | defines a    |
| land    |             | ingType |                   | zoning type  |
| use     |             |         |                   | for the area |
| c       |             |         |                   |              |
| ategory |             |         |                   |              |
| of the  |             |         |                   |              |
| lands   |             |         |                   |              |
| within  |             |         |                   |              |
| the     |             |         |                   |              |
| zone    |             |         |                   |              |
| bo      |             |         |                   |              |
| undary. |             |         |                   |              |
| Each    |             |         |                   |              |
| \"zone  |             |         |                   |              |
| cat     |             |         |                   |              |
| egory\" |             |         |                   |              |
| has its |             |         |                   |              |
| own     |             |         |                   |              |
| Chapter |             |         |                   |              |
| in the  |             |         |                   |              |
| text of |             |         |                   |              |
| By-law  |             |         |                   |              |
| 569     |             |         |                   |              |
| -2013.) |             |         |                   |              |
+---------+-------------+---------+-------------------+--------------+
|         | tor:zone\   | hp      | to                |              |
|         | _{GEN_ZONE} | :subZon | r:zone\_{ZN_ZONE} |              |
|         |             | ingType |                   |              |
+---------+-------------+---------+-------------------+--------------+
|         | tor:        | hp      | to                |              |
|         | zoning_reg\ | :design | r:zone\_{ZN_ZONE} |              |
| ZN_ZONE | _{OBJECTID} | atesZon |                   |              |
| = (The  |             | ingType |                   |              |
| land    |             |         |                   |              |
| use     |             |         |                   |              |
| c       |             |         |                   |              |
| ategory |             |         |                   |              |
| of the  |             |         |                   |              |
| lands   |             |         |                   |              |
| within  |             |         |                   |              |
| the     |             |         |                   |              |
| zone    |             |         |                   |              |
| bo      |             |         |                   |              |
| undary. |             |         |                   |              |
| Each    |             |         |                   |              |
| \"zone  |             |         |                   |              |
| cat     |             |         |                   |              |
| egory\" |             |         |                   |              |
| has its |             |         |                   |              |
| own     |             |         |                   |              |
| Chapter |             |         |                   |              |
| in the  |             |         |                   |              |
| text of |             |         |                   |              |
| By-law  |             |         |                   |              |
| 569     |             |         |                   |              |
| -2013.) |             |         |                   |              |
| \[Zoned |             |         |                   |              |
| dest    |             |         |                   |              |
| ination |             |         |                   |              |
| of the  |             |         |                   |              |
| zone    |             |         |                   |              |
| limited |             |         |                   |              |
| by      |             |         |                   |              |
| GE      |             |         |                   |              |
| N_ZONE. |             |         |                   |              |
+---------+-------------+---------+-------------------+--------------+
|         | tor:zone    | hp      | tor:              |              |
|         | \_{ZN_ZONE} | :subZon | zone\_{ZN_STRING} |              |
|         |             | ingType |                   |              |
+---------+-------------+---------+-------------------+--------------+
|         | tor:zone    | hp:de   | tor:zonin         |              |
|         | \_{ZN_ZONE} | finedIn | g_by-law_569-2013 |              |
|         |             |         | _SECTN{ZBL_SECTN} |              |
+---------+-------------+---------+-------------------+--------------+
| ZN      | tor:        | hp      | tor:              | #values      |
| _STRING | zoning_reg\ | :design | zone\_{ZN_STRING} | listed in    |
| =       | _{OBJECTID} | atesZon |                   | this dataset |
| (C      |             | ingType |                   | (and denoted |
| omplete |             |         |                   | in the       |
| label   |             |         |                   | ZN_STRING)   |
| of the  |             |         |                   | are defined  |
| zone.)  |             |         |                   | as part of   |
|         |             |         |                   | the zone     |
|         |             |         |                   | label, which |
|         |             |         |                   | is           |
|         |             |         |                   | essentially  |
|         |             |         |                   | a more       |
|         |             |         |                   | specific     |
|         |             |         |                   | zone         |
|         |             |         |                   | (subZoning)  |
|         |             |         |                   | for the      |
|         |             |         |                   | ZN_ZONE      |
+---------+-------------+---------+-------------------+--------------+
| EX      | tor:zone\_  | hp:d    | tor:{ZN_Z         | #provides a  |
| CPTN_NO | {ZN_STRING} | efinesZ | ONE}\_{EXCPTN_NO} | pointer to   |
| = (This |             | oningEx |                   | any          |
| is the  |             | ception |                   | exception(s) |
| Ex      |             |         |                   | to the       |
| ception |             |         |                   | ZN_ZONE      |
| Number  |             |         |                   | regulations  |
| for the |             |         |                   | applied to   |
| zone if |             |         |                   | this         |
| one     |             |         |                   | particular   |
| exists. |             |         |                   | zone         |
| The     |             |         |                   | (ZN_STRING); |
| ex      |             |         |                   | these are    |
| ception |             |         |                   | incorporated |
| number  |             |         |                   | into the     |
| is      |             |         |                   | definition   |
| p       |             |         |                   | of ZN_STRING |
| refaced |             |         |                   |              |
| by the  |             |         |                   |              |
| letter  |             |         |                   |              |
| \"x\"   |             |         |                   |              |
| in the  |             |         |                   |              |
| zone    |             |         |                   |              |
| label.  |             |         |                   |              |
| Each    |             |         |                   |              |
| zone    |             |         |                   |              |
| has its |             |         |                   |              |
| own     |             |         |                   |              |
| series  |             |         |                   |              |
| of      |             |         |                   |              |
| ex      |             |         |                   |              |
| ception |             |         |                   |              |
| n       |             |         |                   |              |
| umbers, |             |         |                   |              |
| s       |             |         |                   |              |
| tarting |             |         |                   |              |
| at 1,   |             |         |                   |              |
| so the  |             |         |                   |              |
| ex      |             |         |                   |              |
| ception |             |         |                   |              |
| number  |             |         |                   |              |
| must be |             |         |                   |              |
| read in |             |         |                   |              |
| conj    |             |         |                   |              |
| unction |             |         |                   |              |
| with    |             |         |                   |              |
| the     |             |         |                   |              |
| res     |             |         |                   |              |
| pective |             |         |                   |              |
| zone    |             |         |                   |              |
| s       |             |         |                   |              |
| ymbol.) |             |         |                   |              |
+---------+-------------+---------+-------------------+--------------+
| ZBL     | tor:        | hp:de   | tor:zon           |              |
| _EXCPTN | {ZN_ZONE}\_ | finedIn | ing_by-law_569-20 |              |
| =       | {EXCPTN_NO} |         | 13\_{ZBL_EXCEPTN} |              |
| (By-law |             |         |                   |              |
| text    |             |         |                   |              |
| section |             |         |                   |              |
| number) |             |         |                   |              |
+---------+-------------+---------+-------------------+--------------+
| ZN_     | to          | r       | hp:Regulation     | #holdings    |
| HOLDING | r:holding_r | df:type |                   | aren\'t      |
| = (To   | eg\_{OBJECT |         |                   | zones and    |
| i       | ID}         |         |                   | regulations  |
| ndicate |             |         |                   | defined      |
| whether |             |         |                   | within the   |
| there   |             |         |                   | bylaw        |
| is a    |             |         |                   | (though they |
| HOLDING |             |         |                   | are          |
| status  |             |         |                   | interpreted  |
| for the |             |         |                   | as zones);   |
| zone.   |             |         |                   | they are     |
| The     |             |         |                   | temporary    |
| zone    |             |         |                   | zones        |
| label   |             |         |                   | applied to a |
| will be |             |         |                   | particular   |
| p       |             |         |                   | area         |
| refaced |             |         |                   |              |
| by the  |             |         |                   |              |
| letter  |             |         |                   |              |
| (H).    |             |         |                   |              |
| These   |             |         |                   |              |
| are not |             |         |                   |              |
| common, |             |         |                   |              |
| and     |             |         |                   |              |
| when    |             |         |                   |              |
| used, a |             |         |                   |              |
| Holding |             |         |                   |              |
| Zone is |             |         |                   |              |
| most    |             |         |                   |              |
| often   |             |         |                   |              |
| applied |             |         |                   |              |
| to      |             |         |                   |              |
| s       |             |         |                   |              |
| pecific |             |         |                   |              |
| sites.) |             |         |                   |              |
| \[Yes   |             |         |                   |              |
| (Y) or  |             |         |                   |              |
| No      |             |         |                   |              |
| (N)\]   |             |         |                   |              |
+---------+-------------+---------+-------------------+--------------+
|         | to          | hp:def  | tor               | #details of  |
|         | r:holding_r | inedFor | :area\_{OBJECTID} | tor:         |
|         | eg\_{OBJECT |         |                   | holding_zone |
|         | ID}         |         |                   | are defined  |
|         |             |         |                   | furtherby    |
|         |             |         |                   | the bylaw    |
+---------+-------------+---------+-------------------+--------------+
|         | to          | hp      | tor:holding_zone  |              |
|         | r:holding_r | :design |                   |              |
|         | eg\_{OBJECT | atesZon |                   |              |
|         | ID}         | ingType |                   |              |
+---------+-------------+---------+-------------------+--------------+
| HOL     | to          | genprop | {HOLDING_ID}      |              |
| DING_ID | r:holding_r | :hasIde |                   |              |
| (       | eg\_{OBJECT | ntifier |                   |              |
| Holding | ID}         |         |                   |              |
| Number  |             |         |                   |              |
| if it   |             |         |                   |              |
| e       |             |         |                   |              |
| xists.) |             |         |                   |              |
+---------+-------------+---------+-------------------+--------------+

: Table 2: Mapping zoning type assignments in Toronto

The zoning type is defined with the instantiation of any applicable
regulations. Here, we outline example mappings for frontage, unit, and
density regulations defined for a zoning type. The complete mapping
specification is provided in the supplementary file. Table 3 specifies
the mapping to capture any frontage regulations for the zoning type. A
new Regulation is introduced that applies to the zoning, the regulation
specifies a *requirement* of some Frontage quantity, associated with the
"FRONTAGE" value provided in the data. The mapping encodes the intended
unit of measure (metres), along with the population that the regulation
applies to. In this case, an extension is introduced to define the
population of lots in Toronto (TorontoLotPopulation). In practice, the
required classes could be identified and defined in a separate extension
to the HPCDM, such that they could be referenced directly in any mapping
implementation.

![A computer screen shot of a diagram AI-generated content may be
incorrect.](./image3.png){width="6.5in"
height="4.2444444444444445in"}

Figure 3: Diagram of Frontage restriction mapping result

+---------+-------------+---------+-----------------+-----------------+
| *       | **Mapping   |         |                 |                 |
| *\"Zone | to HPCDM**  |         |                 |                 |
| Categ   |             |         |                 |                 |
| ories\" |             |         |                 |                 |
| f       |             |         |                 |                 |
| ields** |             |         |                 |                 |
+=========+=============+=========+=================+=================+
|         | **Subject** | **Pro   | **Object**      | **Notes**       |
|         |             | perty** |                 |                 |
+---------+-------------+---------+-----------------+-----------------+
| F       | tor:{Z      | r       | hp:Regulation   |                 |
| RONTAGE | N_STRING}\_ | df:type |                 |                 |
| = (The  | regulation_ |         |                 |                 |
| r       | constraints |         |                 |                 |
| equired |             |         |                 |                 |
| minimum |             |         |                 |                 |
| Lot     |             |         |                 |                 |
| F       |             |         |                 |                 |
| rontage |             |         |                 |                 |
| in the  |             |         |                 |                 |
| zone,   |             |         |                 |                 |
| and is  |             |         |                 |                 |
| a       |             |         |                 |                 |
| numeric |             |         |                 |                 |
| value   |             |         |                 |                 |
| p       |             |         |                 |                 |
| refaced |             |         |                 |                 |
| by the  |             |         |                 |                 |
| letter  |             |         |                 |                 |
| \"f\"   |             |         |                 |                 |
| within  |             |         |                 |                 |
| a       |             |         |                 |                 |
| resi    |             |         |                 |                 |
| dential |             |         |                 |                 |
| zone    |             |         |                 |                 |
| label.) |             |         |                 |                 |
| \[Unit  |             |         |                 |                 |
| =       |             |         |                 |                 |
| me      |             |         |                 |                 |
| tres.\] |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
|         |             |         |                 |                 |
+---------+-------------+---------+-----------------+-----------------+
|         | tor:{Z      | g       | Zone String     |                 |
|         | N_STRING}\_ | enprop: | {ZN_STRING}     |                 |
|         | regulation_ | hasName |                 |                 |
|         | constraints |         |                 |                 |
+---------+-------------+---------+-----------------+-----------------+
|         | tor:{Z      | hp:de   | tor:zoning_     |                 |
|         | N_STRING}\_ | finedIn | by-law_569-2013 |                 |
|         | regulation_ |         |                 |                 |
|         | constraints |         |                 |                 |
+---------+-------------+---------+-----------------+-----------------+
|         | tor:{Z      | opr     | tor:zo          |                 |
|         | N_STRING}\_ | :forZon | ne\_{ZN_STRING} |                 |
|         | regulation_ | ingType |                 |                 |
|         | constraints |         |                 |                 |
+---------+-------------+---------+-----------------+-----------------+
|         | tor:{Z      | h       | tor:min_fronta  |                 |
|         | N_STRING}\_ | p:speci | ge\_{ZN_STRING} |                 |
|         | regulation_ | fiesCon |                 |                 |
|         | constraints | straint |                 |                 |
+---------+-------------+---------+-----------------+-----------------+
|         | tor:min     | r       | hp:Quan         |                 |
|         | _frontage\_ | df:type | tityRequirement |                 |
|         | {ZN_STRING} |         |                 |                 |
+---------+-------------+---------+-----------------+-----------------+
|         | tor:min     | i72:h   | tor:min_fronta  |                 |
|         | _frontage\_ | asValue | ge\_{ZN_STRING} |                 |
|         | {ZN_STRING} |         | \_specification |                 |
+---------+-------------+---------+-----------------+-----------------+
|         | tor:min_fro | i72:has | {FRONTAGE}      |                 |
|         | ntage\_{ZN_ | Numeric |                 |                 |
|         | STRING}\_sp | alValue |                 |                 |
|         | ecification |         |                 |                 |
+---------+-------------+---------+-----------------+-----------------+
|         | tor:min_fro | i72:    | hp:metres       |                 |
|         | ntage\_{ZN_ | hasUnit |                 |                 |
|         | STRING}\_sp |         |                 |                 |
|         | ecification |         |                 |                 |
+---------+-------------+---------+-----------------+-----------------+
|         | tor:min     | h       | tor:zone\_      |                 |
|         | _frontage\_ | p:speci | {ZN_STRING}\_lo |                 |
|         | {ZN_STRING} | fiesMin | ts_min_frontage |                 |
|         |             | imumFor |                 |                 |
+---------+-------------+---------+-----------------+-----------------+
|         | tor:zon     | r       | hp:Minimum      |                 |
|         | e\_{ZN_STRI | df:type |                 |                 |
|         | NG}\_lots_m |         |                 |                 |
|         | in_frontage |         |                 |                 |
+---------+-------------+---------+-----------------+-----------------+
|         | tor:zon     | i72:pa  | t               |                 |
|         | e\_{ZN_STRI | rameter | or:frontage_var |                 |
|         | NG}\_lots_m | _of_var |                 |                 |
|         | in_frontage |         |                 |                 |
+---------+-------------+---------+-----------------+-----------------+
|         | tor:zon     | hp:mi   | tor:lot_p       |                 |
|         | e\_{ZN_STRI | nimumOf | opulation_in_zo |                 |
|         | NG}\_lots_m |         | ne\_{ZN_STRING} |                 |
|         | in_frontage |         |                 |                 |
+---------+-------------+---------+-----------------+-----------------+
|         | tor:f       | i72:    | \"h             | #we may         |
|         | rontage_var | hasName | p:hasFrontage\" | actually want   |
|         |             |         |                 | to distinguish  |
|         |             |         |                 | between the     |
|         |             |         |                 | object class    |
|         |             |         |                 | too (since a    |
|         |             |         |                 | lot could have  |
|         |             |         |                 | different       |
|         |             |         |                 | frontages,      |
|         |             |         |                 | according to    |
|         |             |         |                 | different       |
|         |             |         |                 | m               |
|         |             |         |                 | unicipalities); |
|         |             |         |                 | I think this is |
|         |             |         |                 | a general       |
|         |             |         |                 | requirement -   |
|         |             |         |                 | to restrict     |
|         |             |         |                 | parameters more |
|         |             |         |                 | precisely -     |
|         |             |         |                 | that should be  |
|         |             |         |                 | addressed by    |
|         |             |         |                 | 21972           |
+---------+-------------+---------+-----------------+-----------------+
|         | tor:lo      | r       | tor:Toront      |                 |
|         | t_populatio | df:type | oLotPopulation_ |                 |
|         | n_in_zone\_ |         | Zone{ZN_STRING} |                 |
|         | {ZN_STRING} |         |                 |                 |
+---------+-------------+---------+-----------------+-----------------+

: Table 3: Mapping the defined Frontage restriction for lots in the zone
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

+---------+--------------+---------+------------------+--------------+
| *       | **Mapping to |         |                  |              |
| *\"Zone | HPCDM**      |         |                  |              |
| Categ   |              |         |                  |              |
| ories\" |              |         |                  |              |
| f       |              |         |                  |              |
| ields** |              |         |                  |              |
+=========+==============+=========+==================+==============+
|         | **Subject**  | **Pro   | **Object**       | **Notes**    |
|         |              | perty** |                  |              |
+---------+--------------+---------+------------------+--------------+
| UNITS = | tor          | r       | hp:Regulation    | Note: no     |
| (The    | :{ZN_STRING} | df:type |                  | data         |
| pe      | \_regulation |         |                  | published    |
| rmitted | _constraints |         |                  |              |
| maximum |              |         |                  |              |
| number  |              |         |                  |              |
| of      |              |         |                  |              |
| D       |              |         |                  |              |
| welling |              |         |                  |              |
| Units   |              |         |                  |              |
| allowed |              |         |                  |              |
| on a    |              |         |                  |              |
| lot in  |              |         |                  |              |
| the     |              |         |                  |              |
| zone,   |              |         |                  |              |
| and is  |              |         |                  |              |
| a       |              |         |                  |              |
| numeric |              |         |                  |              |
| value   |              |         |                  |              |
| p       |              |         |                  |              |
| refaced |              |         |                  |              |
| by the  |              |         |                  |              |
| letter  |              |         |                  |              |
| \"u\"   |              |         |                  |              |
| in a    |              |         |                  |              |
| resi    |              |         |                  |              |
| dential |              |         |                  |              |
| zone.)  |              |         |                  |              |
|         |              |         |                  |              |
|         |              |         |                  |              |
+---------+--------------+---------+------------------+--------------+
|         | tor          | hp:de   | tor:zoning       |              |
|         | :{ZN_STRING} | finedIn | _by-law_569-2013 |              |
|         | \_regulation |         |                  |              |
|         | _constraints |         |                  |              |
+---------+--------------+---------+------------------+--------------+
|         | tor          | opr     | tor:z            |              |
|         | :{ZN_STRING} | :forZon | one\_{ZN_STRING} |              |
|         | \_regulation | ingType |                  |              |
|         | _constraints |         |                  |              |
+---------+--------------+---------+------------------+--------------+
|         | tor          | h       | tor:max_un       |              |
|         | :{ZN_STRING} | p:speci | its\_{ZN_STRING} |              |
|         | \_regulation | fiesCon |                  |              |
|         | _constraints | straint |                  |              |
+---------+--------------+---------+------------------+--------------+
|         | to           | r       | hp:Q             |              |
|         | r:max_units\ | df:type | uantityAllowance |              |
|         | _{ZN_STRING} |         |                  |              |
+---------+--------------+---------+------------------+--------------+
|         | to           | i72:h   | tor:max_u        |              |
|         | r:max_units\ | asValue | nits\_{ZN_STRING |              |
|         | _{ZN_STRING} |         | }\_specification |              |
+---------+--------------+---------+------------------+--------------+
|         | tor:m        | i72:has | {UNITS}          |              |
|         | ax_units\_{Z | Numeric |                  |              |
|         | N_STRING}\_s | alValue |                  |              |
|         | pecification |         |                  |              |
+---------+--------------+---------+------------------+--------------+
|         | tor:m        | i72:    | i72:population_  |              |
|         | ax_units\_{Z | hasUnit | cardinality_unit |              |
|         | N_STRING}\_s |         |                  |              |
|         | pecification |         |                  |              |
+---------+--------------+---------+------------------+--------------+
|         | to           | h       | tor:zone         |              |
|         | r:max_units\ | p:speci | \_{ZN_STRING}\_l |              |
|         | _{ZN_STRING} | fiesMax | ots_max_dwelling |              |
|         |              | imumFor |                  |              |
+---------+--------------+---------+------------------+--------------+
|         | tor:         | r       | hp:Maximum       |              |
|         | zone\_{ZN_ST | df:type |                  |              |
|         | RING}\_lots_ |         |                  |              |
|         | max_dwelling |         |                  |              |
+---------+--------------+---------+------------------+--------------+
|         | tor:         | i72:pa  | tor:n            |              |
|         | zone\_{ZN_ST | rameter | um_dwellings_var |              |
|         | RING}\_lots_ | _of_var |                  |              |
|         | max_dwelling |         |                  |              |
+---------+--------------+---------+------------------+--------------+
|         | tor:         | hp:ma   | tor:lot          |              |
|         | zone\_{ZN_ST | ximumOf | _population_in_z |              |
|         | RING}\_lots_ |         | one\_{ZN_STRING} |              |
|         | max_dwelling |         |                  |              |
+---------+--------------+---------+------------------+--------------+
|         | tor:num_d    | i72:    | hp               | has          |
|         | wellings_var | hasName | :hasNumDwellings | NumDwellings |
|         |              |         |                  | originally   |
|         |              |         |                  | plannedto be |
|         |              |         |                  | defined in   |
|         |              |         |                  | Toronto      |
|         |              |         |                  | extension    |
+---------+--------------+---------+------------------+--------------+
|         | tor          | r       | tor:Toro         | #a           |
|         | :lot_populat | df:type | ntoLotPopulation | lternatively |
|         | ion_in_zone\ |         | _Zone{ZN_STRING} | could define |
|         | _{ZN_STRING} |         |                  | based on the |
|         |              |         |                  | zone area    |
|         |              |         |                  | specified by |
|         |              |         |                  | the          |
|         |              |         |                  | geometry,    |
|         |              |         |                  | e.g.         |
|         |              |         |                  | tor:ar       |
|         |              |         |                  | ea\_{OBJECTI |
|         |              |         |                  | D}\_geometry |
+---------+--------------+---------+------------------+--------------+
|         | tor:         | r       | tor:Toro         |              |
|         | TorontoLotPo | dfs:sub | ntoLotPopulation |              |
|         | pulation_Zon | ClassOf |                  |              |
|         | e{ZN_STRING} |         |                  |              |
+---------+--------------+---------+------------------+--------------+
|         | tor:         | i72:loc | https://www.g    |              |
|         | TorontoLotPo | ated_in | eonames.org/6167 |              |
|         | pulation_Zon |         | 865/toronto.html |              |
|         | e{ZN_STRING} |         |                  |              |
+---------+--------------+---------+------------------+--------------+
|         | tor:         | i72:def | hp:Lot and       |              |
|         | TorontoLotPo | ined_by | hp:hasZone value |              |
|         | pulation_Zon | only    | tor:z            |              |
|         | e{ZN_STRING} |         | one\_{ZN_STRING} |              |
+---------+--------------+---------+------------------+--------------+
|         | tor:lo       | r       | tor:Toro         |              |
|         | t_population | df:type | ntoLotPopulation |              |
+---------+--------------+---------+------------------+--------------+

: Table 4: Mapping the maximum number of units per lot in the zone in
Toronto

Table 5 specifies the mapping to represent a regulation on density in
the zone. This regulation specifies a limit on floor space index (FSI)
and so is defined as a LotFSI value. LotFSI is defined in the HPCDM as a
ratio of gross floor area to lot area.

+---------+--------------+---------+----------------+----------------+
| *       | **Mapping to |         |                |                |
| *\"Zone | HPCDM**      |         |                |                |
| Categ   |              |         |                |                |
| ories\" |              |         |                |                |
| f       |              |         |                |                |
| ields** |              |         |                |                |
+=========+==============+=========+================+================+
|         | **Subject**  | **Pro   | **Object**     | **Notes**      |
|         |              | perty** |                |                |
+---------+--------------+---------+----------------+----------------+
| DENSITY | tor          | r       | hp:Regulation  |                |
| = (The  | :{ZN_STRING} | df:type |                |                |
| pe      | \_regulation |         |                |                |
| rmitted | _constraints |         |                |                |
| maximum |              |         |                |                |
| Density |              |         |                |                |
| in the  |              |         |                |                |
| zone by |              |         |                |                |
| FSI     |              |         |                |                |
| (floor  |              |         |                |                |
| space   |              |         |                |                |
| index), |              |         |                |                |
| and is  |              |         |                |                |
| a       |              |         |                |                |
| numeric |              |         |                |                |
| value   |              |         |                |                |
| p       |              |         |                |                |
| refaced |              |         |                |                |
| by the  |              |         |                |                |
| letter  |              |         |                |                |
| \"d\"   |              |         |                |                |
| in      |              |         |                |                |
| resi    |              |         |                |                |
| dential |              |         |                |                |
| zones.) |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
|         |              |         |                |                |
+---------+--------------+---------+----------------+----------------+
|         | tor          | hp:de   | tor:zoning_b   |                |
|         | :{ZN_STRING} | finedIn | y-law_569-2013 |                |
|         | \_regulation |         |                |                |
|         | _constraints |         |                |                |
+---------+--------------+---------+----------------+----------------+
|         | tor          | opr     | tor:zon        |                |
|         | :{ZN_STRING} | :forZon | e\_{ZN_STRING} |                |
|         | \_regulation | ingType |                |                |
|         | _constraints |         |                |                |
+---------+--------------+---------+----------------+----------------+
|         | tor          | h       | tor:max_densit |                |
|         | :{ZN_STRING} | p:speci | y\_{ZN_STRING} |                |
|         | \_regulation | fiesCon |                |                |
|         | _constraints | straint |                |                |
+---------+--------------+---------+----------------+----------------+
|         | tor:         | r       | hp:Qua         |                |
|         | max_density\ | df:type | ntityAllowance |                |
|         | _{ZN_STRING} |         |                |                |
+---------+--------------+---------+----------------+----------------+
|         | tor:         | i72:h   | t              |                |
|         | max_density\ | asValue | or:max_density |                |
|         | _{ZN_STRING} |         | \_{ZN_STRING}\ |                |
|         |              |         | _specification |                |
+---------+--------------+---------+----------------+----------------+
|         | tor:max      | i72:has | {DENSITY}      |                |
|         | _density\_{Z | Numeric |                |                |
|         | N_STRING}\_s | alValue |                |                |
|         | pecification |         |                |                |
+---------+--------------+---------+----------------+----------------+
|         | tor:         | h       | tor:zone\_{    |                |
|         | max_density\ | p:speci | ZN_STRING}\_lo |                |
|         | _{ZN_STRING} | fiesMax | ts_max_density |                |
|         |              | imumFor |                |                |
+---------+--------------+---------+----------------+----------------+
|         | tor          | r       | hp:Maximum     |                |
|         | :zone\_{ZN_S | df:type |                |                |
|         | TRING}\_lots |         |                |                |
|         | _max_density |         |                |                |
+---------+--------------+---------+----------------+----------------+
|         | tor          | i72:pa  | t              |                |
|         | :zone\_{ZN_S | rameter | or:density_var |                |
|         | TRING}\_lots | _of_var |                |                |
|         | _max_density |         |                |                |
+---------+--------------+---------+----------------+----------------+
|         | tor          | hp:ma   | tor:lot_pop    |                |
|         | :zone\_{ZN_S | ximumOf | ulation_in_zon |                |
|         | TRING}\_lots |         | e\_{ZN_STRING} |                |
|         | _max_density |         |                |                |
+---------+--------------+---------+----------------+----------------+
|         | tor          | i72:    | \"hp:hasFSI\"  |                |
|         | :density_var | hasName |                |                |
+---------+--------------+---------+----------------+----------------+
|         | tor          | r       | tor:TorontoL   |                |
|         | :lot_populat | df:type | otPopulation_Z |                |
|         | ion_in_zone\ |         | one{ZN_STRING} |                |
|         | _{ZN_STRING} |         |                |                |
+---------+--------------+---------+----------------+----------------+
|         | tor:         | r       | tor:Toront     |                |
|         | TorontoLotPo | dfs:sub | oLotPopulation |                |
|         | pulation_Zon | ClassOf |                |                |
|         | e{ZN_STRING} |         |                |                |
+---------+--------------+---------+----------------+----------------+

: Table 5: Mapping of density regulation in a zone in Toronto

Table 6 specifies the mapping to represent [Zoning Height
Overlay](https://open.toronto.ca/dataset/zoning-by-law/). The same
general approach can be defined for any area-based regulations defined
independently of zoning types (not incorporated in the zoning area
layer)

Table 6: Mapping of Zoning Height Overlay in Toronto

  ---------------------------------------------------------------------------------------------------------------------------------------------------
  **\"Zone       **Mapping to HPCDM**                                                                                               
  Categories\"                                                                                                                      
  Field**                                                                                                                           
  -------------- -------------------------------------------- ------------------------ -------------------------------------------- -----------------
                 **Subject**                                  **Property**             **Object**                                   **Notes**

  \_id           tor:height_zone{\_id}                        rdf:type                 hp:Regulation                                

                 tor:height_zone{\_id}                        genprop:hasName          \"Height Regulation {\_id}\"                 

                 tor:zoning_by-law_569-2013                   hp:definesRegulation     tor:height_zone{\_id}                        

  geometry       tor:height_zone{\_id}                        hp:definedFor            tor:height_zone{\_id}Area                    definition of the
                                                                                                                                    area that the
                                                                                                                                    regulation
                                                                                                                                    applies to

                 tor:height_zone{\_id}Area                    rdf:type                 hp:AdministrativeArea                        

                 tor:height_zone{\_id}Area                    loc:hasLocation          tor:height_zone{\_id}AreaLoc                 

                 tor:height_zone{\_id}AreaLoc                 geo:asWKT                {geometry}                                   

                 tor:height_zone{\_id}                        hp:specifiesConstraint   tor:height_zone{\_id}HeightConstraint        

                 tor:height_zone{\_id}HeightConstraint        rdf:type                 hp:QuantityAllowance                         

                 tor:height_zone{\_id}HeightConstraint        i72:hasValue             tor:height_zone{\_id}HeightConstraintValue   

  HT_LABEL       tor:height_zone{\_id}HeightConstraintValue   i72:hasNumericalValue    {HT_LABEL}                                   the maximum
                                                                                                                                    height in metres

                 tor:height_zone{\_id}HeightConstraintValue   i72:hasUnit              i72:metre                                    

                 tor:height_zone{\_id}HeightConstraint        hp:specifiesMaximumFor   tor:height_zone{\_id}MaxHeight               definition of the
                                                                                                                                    constrained
                                                                                                                                    property
                                                                                                                                    (building height)

                 tor:height_zone{\_id}MaxHeight               rdf:type                 hp:Maximum                                   Can define this
                                                                                                                                    population
                                                                                                                                    subclass in
                                                                                                                                    further detail if
                                                                                                                                    needed

                 tor:height_zone{\_id}MaxHeight               hp:maximumOf             tor:buildingPopulationHeightZone{\_id}       

                 tor:buildingPopulationHeightZone{\_id}       rdf:type                 tor:BuildingPopulation                       

                 tor:height_zone{\_id}MaxHeight               i72:parameter_of_var     tor:height_zone{\_id}BuildingHeight          

                 tor:height_zone{\_id}BuildingHeight          i72:hasName              \"hp:hasBuildngHeight\"                      

                 tor:BuildingPopulation                       rdfs:subClassOf          i72:Population                               
  ---------------------------------------------------------------------------------------------------------------------------------------------------

## 

## Implementation of ORN Data Mapping to TTL 

**Scripts:** [ZoningAreaToronto.py and
HeightZoning.py.](https://github.com/csse-uoft/city-digital-twin-ontology/tree/main/Housing%20Potential%20Python)

**URI strategy**

The scripts generate deterministic URIs under the tor: namespace so
zoning areas, zoning types, and regulations can be referenced
consistently.

**By-law + by-law parts**

-   Zoning by-law: tor:zoning_by-law_569-2013

-   Chapter nodes: tor:zoning_by-law_569-2013_CH{ZBL_CHAPT}

-   Section nodes: tor:zoning_by-law_569-2013_SECTN{ZBL_SECTN}

-   Exception part nodes: tor:zoning_by-law_569-2013\_{ZBL_EXCPTN}

**Area + regulation assignment (per zoning polygon row)**

-   Regulation: tor:zoning_reg\_{\_id}

-   Area (regulated area): tor:area\_{\_id}

-   Area geometry node: tor:area\_{\_id}\_geometry

**Zoning type hierarchy**

-   General zone: tor:zone\_{GEN_ZONE}

-   Mid zone: tor:zone\_{ZN_ZONE}

-   Full zone label: tor:zone\_{ZN_STRING}\
    (Constructed using slugify(\...) in the script.)

**Zoning-type constraint regulations (per ZN_STRING, when values
exist)**

-   Shared constraint regulation container:
    tor:{ZN_STRING}\_regulation_constraints

-   Example constraint nodes + specs:

    -   Frontage: tor:min_frontage\_{ZN_STRING},
        tor:min_frontage\_{ZN_STRING}\_specification

    -   Lot area: tor:min_area\_{ZN_STRING},
        tor:min_area\_{ZN_STRING}\_specification

    -   Max units: tor:max_units\_{ZN_STRING},
        tor:max_units\_{ZN_STRING}\_specification

    -   Density: tor:max_density\_{ZN_STRING},
        tor:max_density\_{ZN_STRING}\_specification

    -   FSI / percent FSI constraints: tor:{ZN_STRING}\_fsi_total,
        tor:{ZN_STRING}\_comm_fsi, tor:{ZN_STRING}\_res_fsi, etc.

    -   Area-units ratio: tor:{ZN_STRING}\_area_units,
        tor:min_area_units\_{ZN_STRING},
        tor:min_area_units\_{ZN_STRING}\_measure

**Holding + exception structures**

-   Holding regulation: tor:holding_reg\_{\_id}

-   Holding zone type node: tor:holding_zone

-   Exception regulation pointer: tor:{ZN_ZONE}\_{EXCPTN_NO}

**Height overlay (separate dataset)**

-   Height regulation: tor:height_zone{\_id}

-   Height regulated area: tor:height_zone{\_id}Area

-   Height area location node: tor:height_zone{\_id}AreaLoc

-   Height constraint nodes: tor:height_zone{\_id}HeightConstraint,
    tor:height_zone{\_id}HeightConstraintValue

-   Max structure: tor:height_zone{\_id}MaxHeight,
    tor:height_zone{\_id}BuildingHeight

-   Population: tor:buildingPopulationHeightZone{\_id}

**Inputs**

**1) Toronto Open Data "zoning-by-law" dataset (zoning areas +
attributes + geometry)**

-   Retrieved programmatically from the Toronto Open Data CKAN endpoint
    (package_show → datastore dump).

-   Key fields used include: \_id, ZN_STATUS, geometry, GEN_ZONE,
    ZN_ZONE, ZN_STRING, ZN_HOLDING, HOLDING_ID, ZN_EXCPTN, EXCPTN_NO,
    ZBL_CHAPT, ZBL_SECTN, ZBL_EXCPTN, and numeric constraint fields like
    FRONTAGE, ZN_AREA, UNITS, DENSITY, FSI_TOTAL, etc.

**2) Zoning height overlay dataset**

-   Local CSV: zoning-height-overlay-4326.csv (read by HeightZoning.py).

-   Key fields used: \_id, HT_LABEL, geometry.

**Outputs**

-   **toronto_zone.ttl** (from ZoningAreaToronto.py)\
    Contains: zoning by-law node + parts, zoning regulations per area,
    zoning type hierarchy, holding/exception links, and zoning-type
    constraint regulations with ISO measurements and units.

-   **Height.ttl** (from HeightZoning.py)\
    Contains: height overlay regulations, regulated areas + geometries,
    height constraint quantities (metres), and maximum structures for
    building height.

**Step-by-step process**

**Zoning areas + by-law references (ZoningAreaToronto.py)**

**Step 1 - Download and load the zoning dataset**\
The script queries the Toronto Open Data CKAN API to locate the
datastore-active resource for "zoning-by-law", then downloads the
datastore dump into a DataFrame.

**Step 2 - Initialize RDF graph + bind namespaces**\
A single RDF graph is created and key namespaces are bound (tor, hp,
geo, opr, mer, bylaw, loc, i72, genprop).

**Step 3 - Create global by-law and modeling scaffolding**\
The script creates tor:zoning_by-law_569-2013 as hp:ZoningBylaw, sets a
bylaw:legislationIdentifier, and defines a set of "variable" resources
used to parameterize minimum/maximum restrictions (frontage, area,
units, density). It also initializes population scaffolding used for
constraints.

**Step 4 - Iterate zoning rows, skip non-by-law areas**\
Rows with ZN_STATUS == 5 are skipped. For each remaining row, the script
mints a regulation tor:zoning_reg\_{\_id} and area tor:area\_{\_id}, and
links regulation → area using hp:definedFor and regulation → by-law
using hp:definedIn.

**Step 5 - Geometry mapping**\
Each area geometry is parsed from the geometry JSON, validated/fixed if
necessary, converted to WKT, asserted via geo:asWKT on
tor:area\_{\_id}\_geometry, and linked via loc:hasLocation.

**Step 6 - Zoning type hierarchy + assignment**\
For each row, GEN_ZONE, ZN_ZONE, and ZN_STRING are each treated as
zoning types designated by the regulation (hp:designatesZoningType), and
linked by hp:subZoningType to represent the hierarchy (GEN → ZN_ZONE →
ZN_STRING).

**Step 7 - By-law part references**\
If present, chapter/section/exception references are created as
hp:ZoningBylawPart nodes, linked using mer:hasProperPart, and
identifiers recorded with genprop:hasIdentifier. The mid-level zone
(ZN_ZONE) is linked to the section via hp:definedIn.

**Step 8 - Holdings and exceptions**\
Holdings create a separate regulation tor:holding_reg\_{\_id} applying
to the area and pointing to a holding zone type. Exceptions create an
exception pointer node and link it from the ZN_STRING zoning type.

**Step 9 - Zoning-type constraints (numeric controls)**\
For each numeric field that exists (frontage, lot area, max units,
density, FSI totals and breakdowns, etc.), the script creates or reuses
a zoning-type constraint regulation node (e.g.,
tor:{ZN_STRING}\_regulation_constraints), links it to the zoning type
(opr:forZoningType), names it (genprop:hasName), and attaches
constraint/allowance structures with ISO21972 measurements
(i72:hasValue, i72:hasNumericalValue, i72:hasUnit). Units are asserted
using i72:metre, i72:square_metre, and i72:population_cardinality_unit
as appropriate.

**Step 10 - Serialize Turtle**\
The final graph is serialized to toronto_zone.ttl.

**Height overlay (HeightZoning.py)**

**Step 1 - Load height overlay CSV and initialize graph**\
The script reads zoning-height-overlay-4326.csv, binds namespaces, and
creates tor:zoning_by-law_569-2013 as the container by-law node
reference for hp:definesRegulation.

**Step 2 - Geometry parsing and WKT conversion**\
Each row's geometry is parsed, validated/fixed, converted to WKT, and
asserted on tor:height_zone{\_id}AreaLoc via geo:asWKT.

**Step 3 - Create regulation + constraint structure**\
For each \_id, the script creates tor:height_zone{\_id} as
hp:Regulation, links it into the by-law (hp:definesRegulation), links it
to its administrative area (hp:definedFor), and adds a
hp:QuantityAllowance constraint with an ISO measurement node containing
the maximum height value and unit i72:metre. It also builds the
"maximum" structure over a building population and parameter-of-var
nodes.

**Step 4 - Serialize Turtle**\
The graph is serialized to Height.ttl.

**Notes / assumptions**

-   ZoningAreaToronto.py pulls data live from the Toronto Open Data CKAN
    endpoint; running the script later may reflect dataset updates
    (schema/values) in the output TTL.

-   All area boundaries and overlays assume valid GeoJSON in the
    geometry column; invalid shapes are repaired using make_valid when
    possible.

-   The zoning-type naming currently uses slugify(zn_str) in the
    genprop:hasName literal for the constraint regulation node; if you
    want the *original* ZN_STRING preserved in the label, the literal
    should use zn_str directly (without slugifying).
