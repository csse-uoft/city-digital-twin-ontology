Building and Parcel Documentation

Relevant Python Scripts:

- [**Buildings.py**](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/Buildings.py):
  generates most building and parcel related RDF data using Open
  Database of Buildings and Toronto Property Boundaries datasets

  - Dataset links

    - <https://open.toronto.ca/dataset/property-boundaries/>

    - <https://utoronto.maps.arcgis.com/home/item.html?id=9d123bc3e0da4555abf5c88fd8bb7b1b>

    - <https://utoronto.maps.arcgis.com/home/item.html?id=1d271ca5c49e406ea4a25f32aa15e066>

- [**BuildingsOwnership.py**](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/BuildingsOwnership.py):
  generates the RDF data for government land ownership using data from
  the provincial lands and GTHA Upper/Lower Tier datasets

  - Dataset links

    - <https://utoronto.maps.arcgis.com/home/item.html?id=799e35b0cb0d453f9abe7e0cc23819c3>

    - <https://utoronto.maps.arcgis.com/home/item.html?id=04d017165a09407b8df5b1649391121f#overview>

    - <https://utoronto.maps.arcgis.com/home/item.html?id=0ea9bb5b440241b68e6d783dcf9b18d3>

- [**FederalBuildings.py**](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/FederalBuildings.py):
  generates the RDF data for federal building information using the
  Federal Property Structures dataset

  - Dataset links

    - <https://utoronto.maps.arcgis.com/home/item.html?id=3c445fa008c54aaeb89ee41401ae7d57>

    - <https://utoronto.maps.arcgis.com/home/item.html?id=cb64f6e0b5084c388747827824c09f27#overview>

- [**ParcelPerimeter.py**](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/ParcelPerimeter.py):
  generates the RDF data for parcel perimeter information

  - Dataset links

    - [https://utoronto.maps.arcgis.com/home/item.html?id=fc726031daf24da6b2962a05d8968f47#overview](https://can01.safelinks.protection.outlook.com/?url=https%3A%2F%2Futoronto.maps.arcgis.com%2Fhome%2Fitem.html%3Fid%3Dfc726031daf24da6b2962a05d8968f47%23overview&data=05%7C02%7Canderson.wong%40mail.utoronto.ca%7C354b87bd957f49d1542908de3463a56c%7C78aac2262f034b4d9037b46d56c55210%7C0%7C0%7C639005799748388885%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=2NEgMW%2B%2BjRMXNo5coKFX7VVl3mMS4v4F5CxzLWzc4XU%3D&reserved=0)

- [**Fakeowners.py**](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Housing%20Potential%20Python/Fakeowners.py):
  generates RDF data for synthetic parcel ownership data
  (fakeowners_1of2.csv)

This is the ontological representation of Toronto’s building and land
parcel data. Buildings are represented as instances of the hp:Building
class while parcels are represented as instances of the hp:Parcel class.
A building can be asserted to occupy a given land parcel using the
hp:occupies property. Furthermore, ownership information can also be
represented by linking the owner and the parcel with the hp:ownership
property.

This section summarizes how the building and parcel related datasets are
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

- i72: <http://ontology.eil.utoronto.ca/ISO21972/iso21972>\#

- org_city:
  <https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Organization/>

- bdg:
  <https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Building/>

<img src="/media/image.png" style="width:6.5in;height:5.80208in" />

<img src="/media/image2.png" style="width:4.4794in;height:4.70163in" />

<img src="/media/image3.png" style="width:5.71875in;height:6.5in" />

| **Data Provided By Toronto Parcel Boundaries Dataset and Parcel Perimeter Dataset (RDF generation done using Buildings.py and ParcelPerimeter.py for the perimeter data)** |  |  |  |  |
|:---|:---|:---|:---|:---|
| **Field Name** | **Subject** | **Property** | **Object** | **Notes** |
| PARCELID | tor:Property{PARCELID} | rdf:type | hp:Parcel |  |
| STATEDAREA | tor:Property{PARCELID} | hp:hasArea | tor:PropertyArea{PARCELID} |  |
|  | tor:PropertyArea{PARCELID} | i72:hasValue | tor:PropertyAreaMeasure{PARCELID} |  |
|  | tor:PropertyAreaMeasure{PARCELID} | i72:hasNumericalValue | "{STATEDAREA}" | parsed for numerical value only (remove units) |
|  | tor:PropertyAreaMeasure{PARCELID} | i72:hasUnit | i72:square_metre |  |
| geometry | tor:Property{PARCELID} | loc:hasLocation | tor:PropertyLoc{PARCELID} |  |
|  | tor:PropertyLoc{PARCELID} | geo:asWKT | "{geometry}" |  |
| Perimeter | tor:Property{PARCELID} | hp:hasPerimeter | tor:PropertyPerimeter{PARCELID} | Note: Perimeter computed in AGOL in metres (no graphDB support for geof:perimeter) |
|  | tor:PropertyPerimeter{PARCELID} | i72:hasValue | tor:PropertyPerimeterMeasure{PARCELID} |  |
|  | tor:PropertyPerimeterMeasure{PARCELID} | i72:hasNumericalValue | {Perimeter} | to compute in mapping |
|  | tor:PropertyPerimeterMeasure{PARCELID} | i72:hasUnit | i72:metre |  |

| **Data Provided By The Open Database of Buildings (RDF generation done using Buildings.py)** |  |  |  |  |
|:---|:---|:---|:---|:---|
| **Field Name** | **Subject** | **Property** | **Object** | **Notes** |
| id | tor:Building{id} | rdf:type | hp:Building |  |
| name | tor:Building{id} | genprop:hasName | "{name}" |  |
| address | tor:Building{id} | contact:hasAddress | tor:BuildingAddress{id} | if there is no data available in the "address" field, address information is parsed from "ADDRESS_NUMBER" and "LINEAR_NAME_FULL" if available |
|  | tor:BuildingAddress{id} | contact:hasStreetNumber | number parsed from {address} if available |  |
|  | tor:BuildingAddress{id} | contact:hasStreet | street name parsed from {address} if available |  |
|  | tor:BuildingAddress{id} | contact:hasStreetType | street type parsed from {address} if available |  |
| type | tor:Building{id} | bdg:use | tor:BuildingUse{type} |  |
|  | tor:BuildingUse{type} | code:hasCode | tor:BuildingUseCode{type} |  |
|  | tor:BuildingUseCode{type} | genprop:hasName | "{type}" |  |
| height | tor:Building{id} | hp:hasBuilidngHeight | tor:BuildingHeight{id} |  |
|  | tor:BuildingHeight{id} | i72:hasValue | tor:BuildingHeightMeasure{id} |  |
|  | tor:BuildingHeightMeasure{id} | i72:hasNumericalValue | "{height}" |  |
|  | tor:BuildingHeightMeasure{id} | i72:hasUnit | i72:metre |  |
| floors | tor:BuildingHeight{id} | i72:hasValue | tor:BuildingFloorsMeasure{id} | another measure of height |
|  | tor:BuildingFloorsMeasure{id} | i72:hasUnit | hp:storeys |  |
| year_built | tor:Building{id} | bdg:yearOfConstruction | tor:Year{year_built} |  |
|  | tor:Year{year_built} | time:year | "{year_built}" |  |
| geometry | tor:Building{id} | loc:hasLocation | tor:Building{id}Loc |  |
|  | tor:Building{id}Loc | geo:asWKT | "{geometry}" |  |
| PARCELID | tor:Building{id} | hp:occupies | tor:Property{PARCELID} | computed via spatial join |

| **Data Provided By The Government Land Ownership Dataset (RDF generation done using BuildingsOwnership.py)** |  |  |  |  |
|:---|:---|:---|:---|:---|
| **Field Name** | **Subject** | **Property** | **Object** | **Notes** |
| OBJECTID_1 | tor:{data_source}property{OBJECTID_1} | rdf:type | hp:Parcel |  |
| Tier or myp_tier | tor:{data_source}property{OBJECTID_1} | hp:ownership | hp:{Tier}Org\* | Rewritten to camelcase |
|  | hp:{Tier}Org\* | rdf:type | org_city:GovernmentOrganization |  |
|  | tor:{data_source}property{OBJECTID_1} | loc:hasLocation | tor:{data_source}property{OBJECTID_1}Loc |  |
| geometry | tor:{data_source}property{OBJECTID_1}Loc | geo:asWKT | {geometry} |  |

| **Data Provided By The Federal Property Structures Dataset (RDF generation done using FederalBuildings.py)** |  |  |  |  |
|:---|:---|:---|:---|:---|
| **Field** | **Subject** | **Property** | **Object** | **Notes** |
| Structure_Number | tor:{Structure_Number}Building | rdf:type | hp:Building | No integration with ODB data in this iteration |
|  | tor:{Structure_Number}Building | genprop:hasIdentifier | {Structure_Number} | Geometry may not cover all cases (some points are defined outside of the building footprints), but may be more accurate than addresses (OBD addresses are incomplete) |
| Structure_Name_E | tor:{Structure_Number}Building | genprop:hasName | {Structure_Name_E} |  |
| Address_E | tor:{Structure_Number}Building | contact:hasAddress | tor:{Structure_Number}Address | Parsed for address components |
|  | tor:{Structure_Number}Address | contact:hasStreetNumber | parsed from {Address_E} if available |  |
|  | tor:{Structure_Number}Address | contact:hasStreet | parsed from {Address_E} if available |  |
|  | tor:{Structure_Number}Address | contact:hasStreetType | parsed from {Address_E} if available |  |
| Floor_Area | tor:{Structure_Number}Building | hp:hasFloorArea | tor:{Structure_Number}BuildingFloorArea |  |
|  | tor:{Structure_Number}BuildingFloorArea | i72:hasValue | tor:{Structure_Number}BuildingFloorAreaMeasure |  |
|  | tor:{Structure_Number}BuildingFloorAreaMeasure | i72:hasNumericalValue | {Floor_Area} |  |
| unitofMeasure | tor:{Structure_Number}BuildingFloorAreaMeasure | i72:hasUnit | i72:square_metre or hp:square_foot | Convert from unitofMeasure |
| Construction_Year | tor:{Structure_Number}Building | bdg:yearOfConstruction | tor:Year{Construction_Year} |  |
|  | tor:Year{Construction_Year} | time:year | {Construction_Year} |  |
| Condition_E | tor:{Structure_Number}Building | hp:hasCondition | tor:{Structure_Number}BuildingCondition |  |
|  | tor:{Structure_Number}BuildingCondition | rdf:type | hp:BuildingCondition |  |
|  | tor:{Structure_Number}BuildingCondition | code:hasCode | tor:{Structure_Number}BuildingConditionCode |  |
| code | tor:{Structure_Number}BuildingConditionCode | genprop:hasIdentifier | {code} |  |
|  | tor:{Structure_Number}BuildingConditionCode | genprop:hasName | {Condition_E} |  |
| Location | tor:{Structure\_}Building | loc:hasLocation | tor:{Structure\_}BuildingLoc |  |
|  | tor:{Structure\_}BuildingLoc | geo:asWKT | POINT({Longitude} {Latitude}) |  |
| Tenants | tor:{Structure\_}Building | hp:occupiedBy | tor:{Tenant code}tenant |  |
|  | tor:{Tenant code}tenant | rdf:type | org_city:Organization |  |
|  | tor:{Tenant code}tenant | genprop:hasName | {Name_E} |  |
| UseTypes | tor:{Structure\_}Building | bdg:use | tor:{Structure\_}BuildingUse{code} |  |
|  | tor:{Structure\_}BuildingUse{code} | code:hasCode | tor:{Structure\_}BuildingUse{code}Code |  |
|  | tor:{Structure\_}BuildingUse{code}Code | genprop:hasIdentifier | {code} |  |
|  | tor:{Structure\_}BuildingUse{code}Code | genprop:hasName | {Use_Name_E} |  |
| PARCELID | tor:{Structure\_}Building | hp:occupies | tor:Property{PARCELID} | Computed via spatial join |

| **Data Provided By The Fakeowners Dataset (RDF generation done using Fakeowners.py)** |  |  |  |  |
|:---|:---|:---|:---|:---|
| **Field** | **Subject** | **Property** | **Object** | **Notes** |
| PARCELID | tor:Property{PARCELID} | hp:ownership | tor:{PARCELID}Ownership{Fake Owner} |  |
| Fake Owner | tor:{PARCELID}Ownership{Fake Owner} | genprop:hasName | "{Fake Owner}" |  |

Implementation of Building and Parcel Related Data in Mapping TTL

**Scripts:** Buildings.py + ParcelPerimeter.py

**URI strategy**

- **Parcel:**

  - tor:Property{PARCELID}

- **Parcel Stated Area + Measure:**

  - tor:PropertyArea{PARCELID}

  - tor:PropertyAreaMeasure{PARCELID}

- **Parcel Location**:

  - tor:PropertyLoc{PARCELID}

- **Parcel Perimeter + Measure (for ParcelPerimeter.py):**

  - tor:PropertyPerimeter{PARCELID}

  - tor:PropertyPerimeterMeasure{PARCELID}

- **Building:**

  - tor:Building{id}

- **Building Address:**

  - tor:BuildingAddress{id}

- **Building Use:**

  - tor:BuildingUse{type}

- **Building Height + Measure**

  - tor:BuildingHeight{id}

  - tor:BuildingHeightMeasure{id}

- **Building Location:**

  - tor:Building{id}Loc

**Scripts:** BuildingsOwnership.py

- **Government Land Parcel:**

  - tor:{data_source}property{OBJECTID_1}

- **Government Organization:**

  - hp:{Tier}Org

**Scripts:** FederalBuildings.py

- **Federal Building:**

  - tor:{Structure_Number}Building

- **Building Address:**

  - tor:{Structure_Number}Address

- **Floor Area + Measure:**

  - tor:{Structure_Number}BuildingFloorArea

  - tor:{Structure_Number}BuildingFloorAreaMeasure

- **Building Condition:**

  - tor:{Structure_Number}BuildingCondition

- **Building Location:**

  - tor:{Structure\_}BuildingLoc

- **Tenant:**

  - tor:{Tenant code}tenant

- **Building Use Type:**

  - tor:{Structure\_}BuildingUse{code}

**Scripts:** Fakeowners.py

- **Synthetic Owner:**

  - tor:{PARCELID}Ownership{Fake Owner}

**Inputs**

1.  **Building Data (Building.py)**

    - Dataset links

      - <https://open.toronto.ca/dataset/property-boundaries/>

      - <https://utoronto.maps.arcgis.com/home/item.html?id=9d123bc3e0da4555abf5c88fd8bb7b1b>

      - <https://utoronto.maps.arcgis.com/home/item.html?id=1d271ca5c49e406ea4a25f32aa15e066>

    - Exported from ArcGIS Online as geoJSON files and named as
      TorontoBuildings1.geojson or TorontoBuildings2.geojson in the
      script for readability

2.  **Parcel Data (for Building.py)**

    - Dataset links

      - [https://utoronto.maps.arcgis.com/home/item.html?id=fc726031daf24da6b2962a05d8968f47#overview](https://can01.safelinks.protection.outlook.com/?url=https%3A%2F%2Futoronto.maps.arcgis.com%2Fhome%2Fitem.html%3Fid%3Dfc726031daf24da6b2962a05d8968f47%23overview&data=05%7C02%7Canderson.wong%40mail.utoronto.ca%7C354b87bd957f49d1542908de3463a56c%7C78aac2262f034b4d9037b46d56c55210%7C0%7C0%7C639005799748388885%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=2NEgMW%2B%2BjRMXNo5coKFX7VVl3mMS4v4F5CxzLWzc4XU%3D&reserved=0)

    - Exported from ArcGIS Online as a geoJSON file and named as
      Parcel.geojson in the script for readability

3.  **Parcel Perimeter (for ParcelPerimeter.py)**

    - Dataset links

      - [https://utoronto.maps.arcgis.com/home/item.html?id=fc726031daf24da6b2962a05d8968f47#overview](https://can01.safelinks.protection.outlook.com/?url=https%3A%2F%2Futoronto.maps.arcgis.com%2Fhome%2Fitem.html%3Fid%3Dfc726031daf24da6b2962a05d8968f47%23overview&data=05%7C02%7Canderson.wong%40mail.utoronto.ca%7C354b87bd957f49d1542908de3463a56c%7C78aac2262f034b4d9037b46d56c55210%7C0%7C0%7C639005799748388885%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=2NEgMW%2B%2BjRMXNo5coKFX7VVl3mMS4v4F5CxzLWzc4XU%3D&reserved=0)

    - Exported from ArcGIS Online as a geoJSON file named as
      “PropertyBoundaries_4326_with_perimeter.geojson” in the script

4.  **Government Land Ownership (for BuildingOwnership.py)**

    - Dataset links

      - <https://utoronto.maps.arcgis.com/home/item.html?id=799e35b0cb0d453f9abe7e0cc23819c3>

      - <https://utoronto.maps.arcgis.com/home/item.html?id=04d017165a09407b8df5b1649391121f#overview>

      - <https://utoronto.maps.arcgis.com/home/item.html?id=0ea9bb5b440241b68e6d783dcf9b18d3>

    - Exported from ArcGIS Online as a geoJSON files named as
      ProvincialLands.geojson, GTHAUpperTier.geojson, and
      GTHALowerTier.geojson respectively in the script

5.  **Federal Property Structures (for FederalBuildings.py)**

    - Dataset links

      - <https://utoronto.maps.arcgis.com/home/item.html?id=3c445fa008c54aaeb89ee41401ae7d57>

      - <https://utoronto.maps.arcgis.com/home/item.html?id=cb64f6e0b5084c388747827824c09f27#overview>

    - Exported from ArcGIS Online as a geoJSON files named as
      FederalBuildings1.geojson, and FederalBuildings2.geojson
      respectively in the script

6.  **Synthetic Parcel Ownership Data (for Fakeowners.py)**

    - Synthetic data from a CSV file named as fakeowners_1of2.csv
      fakeowners_2of2.csv and as Fakeowners1.csv and Fakeowners2.csv
      respectively in the script

**Outputs**

- Buildings1.nt to Buildings10.nt (Buildings.py)  
  Contains: RDF triples for the corresponding Building and Parcel
  related datasets listed above, split into 10 parts for
  performance-related reasons.

- ParcelPerimeter.ttl (ParcelPerimeter.py)  
  Contains: Parcel perimeter information

- GTHAUpperTier.ttl, GTHALowerTier.ttl, ProvincialLands.ttl
  (BuildingsOwnership.py)  
  Contains: Government land ownership information

- FederalBuildings.ttl (FederalBuildings.py)  
  Contains: Federal property structures data

- Fakeowners.ttl (Fakeowners.py)  
  Contains: Synthetic parcel ownership data

**Step-by-step process for Buildings.py**

**Step 1 - Initialize RDF graphs and namespaces**  
One RDF graph is created:

- g contains all triples found in a single N-Triples (.nt) file

**Step 2 – Import geojson datasets using geopandas Python package**  
Building data is contained in the “Buildings” Pandas dataframe, parcel
data is contained in the “Parcel” dataframe, then, unnecessary columns
are dropped before both dataframes are merged into one dataframe called
“df” for row-by-row parsing.

**Note:** the script is designed to take one building geoJSON dataset at
a time for performance reasons. The script should be run once for each
building geoJSON dataset (so 2 times in total) to generate the RDF for
all available data. Counter values for naming the output files should be
modified in order to avoid the overwriting of the output files. The
“counter2” variable should be initialized with a value of 1 for the
first dataset as 5 output files are created (Buildings1.nt to
Buildings5.nt) and should be initialized with a value of 6 for the
second dataset in order to create the next five output files
(Buildings6.nt to Buildings10.nt) without overwriting the first 5 .nt
files.

**Step 3 – RDF triples are created using each row of data in the df
dataframe**  
The df dataframe is iterated row by row and RDF triples are generated
according to the mapping specifications outlined in the tables found
earlier in this document. Values for the triples are extracted from the
corresponding column in the dataframe.

**Step 4 - Keep count of the number of entries that have been
processed**  
When the current graph g contains RDF triples for 10000 data entries,
export the current graph as a N-Triples file, as described in the next
step. The data is serialized into multiple files to improve script
performance and speed while working around the file size limitation for
uploading RDF files in GraphDB Workbench.

**Step 5 - Serialize NT**  
The graphs are written to:

- Buildings1.nt to Buildings10.nt

**Step 6 – Prepare for the next graph to be serialized**  
After the current graph is serialized, clear all data in graph g and run
Python garbage collection (i.e., gc.collect()) in order to free up
system resources and improve script performance. Increment the value of
counter2 by 1 to avoid overwriting the last exported file. Counter2 is
used for the value of the number in the exported file name.

**Step 7 – Repeat steps 3-6 until all data has been mapped to RDF
triples**  
There should be 5 exports for each building geoJSON dataset which
results in the creation of files Buildings1.nt to Buildings10.nt upon
completion.

**Step-by-step process for ParcelPerimeter.py**

**Step 1 - Initialize RDF graphs and namespaces**  
One RDF graph is created:

- g contains all triples found in the output ttl file

**Step 2 – Import geojson datasets using json Python package**  
The imported geoJSON data is stored in the “perimeter” variable.

**Step 3 – RDF triples are created using each feature found in the
imported geojson data**  
The geoJSON data is iterated feature by feature and RDF triples are
generated according to the mapping specifications outlined in the tables
found earlier in this document. Values for the triples are extracted
from the corresponding property in the geoJSON data.

**Step 4 - Serialize TTL**  
The graphs are written to ParcelPerimeter.ttl.

**Step-by-step process for BuildingsOwnership.py**

**Step 1 - Initialize RDF graphs and namespaces**  
One RDF graph is created:

- g contains all triples found in the output ttl file

**Step 2 – Import geojson datasets using json Python package**  
The imported geoJSON data is stored in the “data” variable.

**Step 3 – RDF triples are created using each feature found in the
imported geojson data**  
The geoJSON data is iterated feature by feature and RDF triples are
generated according to the mapping specifications outlined in the tables
found earlier in this document. Values for the triples are extracted
from the corresponding property in the geoJSON data.

**Step 4 - Serialize TTL**  
The graphs are written to GTHAUpperTier.ttl, GTHALowerTier.ttl,
ProvincialLands.ttl depending on the dataset that was processed.

Note: This script only processes one of the three datasets at a time.
You can change the dataset that is being processed by modifying the
“filename” variable in the script accordingly. Additionally, ensure that
the value of the “dataset” variable is also modified accordingly as the
value of that variable is used as the {data_source} value in the mapping
specification found in the tables above.

**Step-by-step process for FederalBuildings.py**

**Step 1 - Initialize RDF graphs and namespaces**  
One RDF graph is created:

- g contains all triples found in the output ttl file

**Step 2 – Import geojson datasets using json Python package**  
The imported geoJSON data is stored in the “building1” and “building2”
variables.

**Step 3 – Import XML data using the etree Python package**  
The imported XML data is stored in the “tree” variable for the XML tree
and the “root” variable for the XML root.

**Step 4 – RDF triples are created using each feature found in the
imported geojson data**  
The geoJSON data is iterated feature by feature and RDF triples are
generated according to the mapping specifications outlined in the tables
found earlier in this document. Values for the triples are extracted
from the corresponding property in the geoJSON data and the XML data.

**Step 5 - Serialize TTL**  
The graphs are written to FederalBuildings.ttl.

**Step-by-step process for Fakeowners.py**

**Step 1 - Initialize RDF graphs and namespaces**  
One RDF graph is created:

- g contains all triples found in the output ttl file

**Step 2 – Import geojson datasets using json Python package**  
The imported geoJSON data is stored in the “df1” and “df2” variables and
then merged into one dataframe called “df”.

**Step 3 – RDF triples are created using each feature found in the
imported geojson data**  
The geoJSON data is iterated feature by feature and RDF triples are
generated according to the mapping specifications outlined in the tables
found earlier in this document. Values for the triples are extracted
from the corresponding property in the geoJSON data.

**Step 4 - Serialize TTL**  
The graphs are written to Fakeowners.ttl.
