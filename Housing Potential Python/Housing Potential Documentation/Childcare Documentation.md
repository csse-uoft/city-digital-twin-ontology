Childcare Documentation

Relevant Python Scripts:

- [Childcare.py:](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/Childcare.py)
  generates the RDF data related to childcare locations in Toronto and
  their capacities.

  - Dataset links

    - <https://open.toronto.ca/dataset/licensed-child-care-centres/>

    - Child care centres - 4326_fake occupancy.xslx (with synthetic
      capacity use data)

This is the ontological representation of Toronto’s childcare location
data from the Toronto Open Data Portal. Services provided by childcare
locations are represented as instances of the tor:TorChildcareService
class while the capacity use and capacity available data is derived from
a synthetic dataset.

This section summarizes how the childcare related datasets are mapped
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

<img src="/media/image.png" style="width:6.5in;height:4.72917in" />

| **Data Provided By the Childcare Dataset and Synthetic Capacity Dataset (RDF generation done using Childcare.py)** |  |  |  |
|:---|:---|:---|:---|
| **Field Name** | **Subject** | **Property** | **Object** |
| \_id | tor:childcareservice_toronto{\_id} | rdf:type | tor:TorChildcareService |
|  | tor:childcareservice_toronto{\_id} | hp:providedFromSite | tor:childcareservice_toronto{\_id}Site |
| LOC_ID | tor:childcareservice_toronto{\_id}Site | genprop:hasIdentifier | {LOC_ID} |
| LOC_NAME | tor:childcareservice_toronto{\_id}Site | genproper:hasName | {LOC_NAME} |
| geometry | tor:childcareservice_toronto{\_id}Site | loc:hasLocation | tor:childcareservice_toronto{\_id}SiteLoc |
|  | tor:childcareservice_toronto{\_id}SiteLoc | geo:asWKT | {geometry} |
| TOTSPACE | tor:childcareservice_toronto{\_id} | res:hasCapacity | tor:childcareservice_toronto{\_id}Capacity |
|  | tor:childcareservice_toronto{\_id}Capacity | rdf:type | hp:ChildcareEnrollmentSpaces |
|  | tor:childcareservice_toronto{\_id}Capacity | i72:hasValue | tor:childcareservice_toronto{\_id}CapacityMeasure |
|  | tor:childcareservice_toronto{\_id}CapacityMeasure | i72:hasNumericalValue | {TOTSPACE} |
|  | tor:childcareservice_toronto{\_id}CapacityMeasure | i72:hasUnit | i72:population_cardinality_unit |
| FAKE OCCUPANCY | tor:childcareservice_toronto{\_id} | res:capacityInUse | tor:childcareservice_toronto{\_id}CapacityUse |
|  | tor:childcareservice_toronto{\_id}CapacityUse | rdf:type | hp:ChildcareEnrollmentSize |
|  | tor:childcareservice_toronto{\_id}CapacityUse | i72:hasValue | tor:childcareservice_toronto{\_id}CapacityUseMeasure |
|  | tor:childcareservice_toronto{\_id}CapacityUseMeasure | i72:hasNumericalValue | {FAKE OCCUPANCY} |
|  | tor:childcareservice_toronto{\_id}CapacityUseMeasure | i72:hasUnit | i72:population_cardinality_unit |
|  | tor:childcareservice_toronto{\_id} | res:hasAvailableCapacity | tor:childcareservice_toronto{\_id}CapacityAvail |
|  | tor:childcareservice_toronto{\_id}CapacityAvail | rdf:type | hp:ChildcareAvailableEnrollmentSpaces |
|  | tor:childcareservice_toronto{\_id}CapacityAvail | i72:hasValue | tor:childcareservice_toronto{\_id}CapacityAvailMeasure |
|  | tor:childcareservice_toronto{\_id}CapacityAvailMeasure | i72:hasNumericalValue | {TOTSPACE - FAKE OCCUPANCY} |
|  | tor:childcareservice_toronto{\_id}CapacityAvailMeasure | i72:hasUnit | i72:population_cardinality_unit |

Implementation of Childcare Related Data in Mapping TTL

**Scripts:** Childcare.py

**URI strategy**

- **Childcare Site:**

  - tor:childcareservice_toronto{\_id}Site

- **Childcare Site Location:**

  - tor:childcareservice_toronto{\_id}SiteLoc

- **Childcare Service:**

  - tor:childcareservice_toronto{\_id}

- **Childcare Capacity:**

  - tor:childcareservice_toronto{\_id}Capacity

- **Childcare Capacity Use:**

  - tor:childcareservice_toronto{\_id}CapacityUse

- **Childcare Capacity Available:**

  - tor:childcareservice_toronto{\_id}CapacityAvail

**Inputs**

1.  **Childcare Synthetic Capacity Data (Childcare.py)**

    - Dataset links

      - Child care centres - 4326_fake occupancy.xslx (with synthetic
        capacity use data)

    - This dataset already includes both the relevant data from the
      Toronto Open Data Portal and the synthetic data so the former
      dataset does not need to be imported for the Python script.

**Outputs**

- Childcare.ttl (Childcare.py)  
  Contains: Childcare data for Toronto and their locations.

- ChildcareCapacity.ttl (Childcare.py)  
  Contains: Synthetic information about childcare capacities.

**Step-by-step process for Childcare.py**

**Step 1 - Initialize RDF graphs and namespaces**  
Two RDF graphs are created:

- g contains all triples for the Childcare.ttl output file

- g2 contains all triples for the ChildcareCapacity.ttl output file

**Step 2 – Import data from the xlsx file using the pandas Python
package**  
The data from the childcare dataset is contained in the “df” dataframe.

**Step 3 - RDF triples are created using each feature in the data**  
The data in stored in the df dataframe is iterated row by row and RDF
triples are generated according to the mapping specifications outlined
in the tables found earlier in this document. Values for the triples are
extracted from the corresponding column in the data.

**Note:** Geometries in this dataset are classified as MultiPoints even
if there is only one pair of coordinates available. This script converts
these MultiPoint geometries to Point geometries to avoid issues related
to geospatial reasoning in GraphDB.

**Step 4 - Serialize TTL**  
The graph g is written to Childcare.ttl and g2 is written to
ChildcareCapacity.ttl.
