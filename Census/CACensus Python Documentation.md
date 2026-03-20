# CACensus Documentation


Relevant Python Scripts: 


  * [CACensusPandas.py:](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Census/CACensusPandas.py) generates the RDF data related to the 2016 Canadian Census of Population.
    * Dataset links
      * <https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/index.cfm?Lang=E>
        * 2016 census profiles for all of Canada can be found here




**Inputs**


  1. **Census Profiles for All Census Tracts In Toronto as CSV Files**
     * Dataset links
       * <https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/index.cfm?Lang=E>
     * For convenience, the census profiles for every census tract in Toronto can be found in the CensusCSV folder in our shared OneDrive as CSV files (GitHub has file size limitations that prevent the uploading of this data).
  2. **census3.json**
     * GitHub link
       * <https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Census/census3.json>
     * This JSON file contains manually created Cellfie rule data that is used for creating URIs in the census Python script.
       * More information on Cellfie can be found here: <https://github.com/protegeproject/cellfie-plugin>




**Outputs**


  * CensusSample10.ttl to CensusSample570 and CensusSample572   
Contains: The census characteristics data as RDF triples, split into 58 separate files for performance reasons. Output files start from CensusSample10, CensusSample20, CensusSample30... CensusSample570 while CensusSample572 contains the remaining few census tracts. Each output file contains the census profile data for 10 different census tracts with the exception of the last output file (CensusSample572) which contains the data for the last few census tracts.




**Step-by-step process for CACensusPandas.py**


**Step 1 - Initialize RDF graphs and namespaces**  
One RDF graph is created:


  * g contains all triples for the current CensusSample output file




**Step 2 – Load the Cellfie Rule data from the census3.json file using the json Python package**  
The Cellfie data is loaded into a dictionary called “reversedict” which links the row number of a census profile CSV with the corresponding characteristic name used in the URIs.


**Step 3 - RDF triples are created using each CSV file in the CensusCSV folder in the data**  
Iterates through all CSV files in the CensusCSV folder and creates a pandas dataframe to hold the data. The data in this dataframe is iterated row by row and RDF triples are generated according to the representation outlined in the [Unlocking the Semantics of Census Data](https://github.com/csse-uoft/city-digital-twin-ontology/blob/main/Census/Unlocking%20the%20Semantics%20of%20Census%20Data.pdf) paper. Values for the triples are extracted from the corresponding column in the data.


**Note:** This Python script uses the row numbers of the census CSV files for its execution. Changing the row numbers will result in incorrect data in the output files.


**Step 4 - Serialize TTL**  
The graph g is written to CensusProfile{insert number}.ttl for every 10 census tracts. The graph g is then cleared before repeating step 3 and 4 again until all of the census profile data is mapped.


**Note:** This Python script may require several hours to finish executing due to the volume of data. 
