Community Centre Documentation

Relevant Python Scripts:

- [CommunityCentre.py:](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/CommunityCentre.py)
  generates the RDF data related to community centres in Toronto and
  their capacities.

  - Dataset links

    - <https://open.toronto.ca/dataset/parks-and-recreation-facilities/>

    - Parks and Recreation Facilities - 4326 fake_capacity.xslx (with
      synthetic capacity data)

This is the ontological representation of Toronto’s community centre
data from the Toronto Open Data Portal. Services provided by community
centres are represented as instances of the
tor:TorCommunityCentreService class while the capacity data is derived
from a synthetic dataset.

This section summarizes how the community centre related datasets are
mapped into the City Digital Twin ontology.

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

| **Data Provided By the Community Centre Dataset and Synthetic Capacity Dataset (RDF generation done using CommunityCentre.py)** |  |  |  |  |
|:---|:---|:---|:---|:---|
| **Field Name** | **Subject** | **Property** | **Object** | **Notes** |
| \_id | tor:communitycentre_service{\_id} | rdf:type | tor:TorCommunityCentreService |  |
| ASSET_ID | tor:communitycentre_service{\_id} | hp:providedFromSite | tor:communitycentresite{ASSET_ID} |  |
|  | tor:communitycentresite{ASSET_ID} | genprop:hasIdentifier | "{ASSET_ID}" |  |
| ASSET_NAME |  | genprop:hasName | "{ASSET_NAME}" |  |
| geometry |  | loc:hasLocation | tor:communitycentresite{ASSET_ID}\_location |  |
|  | tor:communitycentresite{ASSET_ID}\_location | geo:asWKT | "{geometry}" |  |
| FAKE CAPACITY | tor:communitycentre_service{\_id} | res:hasCapacity | tor:communitycentre_service{\_id}Capacity |  |
|  | tor:communitycentre_service{\_id}Capacity | rdf:type | hp:CommunityCentreClientSpaces |  |
|  | tor:communitycentre_service{\_id}Capacity | i72:hasValue | tor:communitycentre_service{\_id}CapacityMeasure |  |
|  | tor:communitycentre_service{\_id}CapacityMeasure | i72:hasNumericalValue | {FAKE CAPACITY} |  |
|  | tor:communitycentre_service{\_id}CapacityMeasure | i72:hasUnit | i72:population_cardinality_unit |  |
|  | tor:communitycentre_service{\_id} | res:capacityInUse | tor:communitycentre_service{\_id}CapacityUse |  |
|  | tor:communitycentre_service{\_id}CapacityUse | rdf:type | hp:CommunityCentreClientSize |  |
|  | tor:communitycentre_service{\_id}CapacityUse | i72:hasValue | tor:communitycentre_service{\_id}CapacityUseMeasure |  |
|  | tor:communitycentre_service{\_id}CapacityUseMeasure | i72:hasNumericalValue | 13,903 | simplistic estimate of service population based on a 1km catchment area radius |
|  | tor:communitycentre_service{\_id}CapacityUseMeasure | i72:hasUnit | i72:population_cardinality_unit |  |
|  | tor:communitycentre_service{\_id} | res:hasAvailableCapacity | tor:communitycentre_service{\_id}CapacityAvail |  |
|  | tor:communitycentre_service{\_id}CapacityAvail | rdf:type | hp:CommunityCentreAvailableSpaces |  |
|  | tor:communitycentre_service{\_id}CapacityAvail | i72:hasValue | tor:communitycentre_service{\_id}CapacityAvailMeasure |  |
|  | tor:communitycentre_service{\_id}CapacityAvailMeasure | i72:hasNumericalValue | {FAKE CAPACITY - 13903} |  |
|  | tor:communitycentre_service{\_id}CapacityAvailMeasure | i72:hasUnit | i72:population_cardinality_unit |  |

Implementation of Community Centre Related Data in Mapping TTL

**Scripts:** CommunityCentre.py

**URI strategy**

- **Community Centre Site:**

  - tor:communitycentresite{ASSET_ID}

- **Community Centre Site Location:**

  - tor:communitycentresite{ASSET_ID}\_location

- **Community Centre Service:**

  - tor:communitycentre_service{\_id}

- **Community Centre Capacity:**

  - tor:communitycentre_service{\_id}CCapacity

- **Community Centre Capacity Use:**

  - tor:communitycentre_service{\_id}CapacityUse

- **Community Centre Capacity Available:**

  - tor:communitycentre_service{\_id}CapacityAvail

**Inputs**

1.  **Community Centre Synthetic Capacity Data (CommunityCentre.py)**

    - Dataset links

      - Parks and Recreation Facilities - 4326 fake_capacity.xslx (with
        synthetic capacity data)

    - This dataset already includes both the relevant data from the
      Toronto Open Data Portal and the synthetic data, so the former
      dataset does not need to be imported for the Python script.

**Outputs**

- CommunityCentre.ttl (CommunityCentre.py)  
  Contains: Community centre data for Toronto and their locations.

- CommunityCentreCapacity.ttl (CommunityCentre.py)  
  Contains: Synthetic information about community centre capacities.

**Step-by-step process for CommunityCentre.py**

**Step 1 - Initialize RDF graphs and namespaces**  
Two RDF graphs are created:

- g contains all triples for the CommunityCentre.ttl output file

- g2 contains all triples for the CommunityCentreCapacity.ttl output
  file

**Step 2 – Import data from the xlsx file using the pandas Python
package**  
The data from the community centre dataset is contained in the “df”
dataframe.

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
The graph g is written to CommunityCentre.ttl and g2 is written to
CommunityCentreCapacity.ttl.
