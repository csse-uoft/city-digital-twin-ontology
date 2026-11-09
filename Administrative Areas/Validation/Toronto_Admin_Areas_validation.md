# Toronto Administrative-Area Mapping Validation

## Inputs
- City of Toronto 25-ward WGS84 dataset
- City of Toronto historical 140-neighbourhood dataset
- Statistics Canada 2016 Census Tract boundary file
- Legacy `Toronto2.ttl` used only to recover the historical ward-neighbourhood crosswalk

## Source schemas used
- Wards: `AREA_S_CD`, `AREA_NAME`, geometry (EPSG:4326)
- Neighbourhoods: `AREA_SHORT_CODE`, `AREA_NAME`, geometry (EPSG:4326)
- Census tracts: `CTUID`, `CMAUID`, geometry (Statistics Canada Lambert/NAD83, reprojected to EPSG:4326)

## Output counts
- 25 wards
- 140 neighbourhoods
- 572 census tracts
- 175 ward-neighbourhood links
- 140 Toronto-neighbourhood links
- 737 WKT geometries
- 7,583 RDF triples

## Mapping logic
- Census tracts are first restricted to Toronto CMA (`CMAUID=535`).
- City-of-Toronto tracts are selected using at least 5% area overlap with the union of the historical 140 neighbourhood polygons.
- Each selected census tract is assigned to the neighbourhood with which it has the largest intersection area.
- The ward-neighbourhood relationship is not encoded directly in the City source files. The exact 175 historical links are therefore recovered from `Toronto2.ttl`; a spatial fallback is available if the legacy TTL is omitted.

## Legacy issues intentionally fixed
- Uses the current ISO SpatialLoc namespace.
- Uses `genprop:hasName` instead of `rdfs:comment` for area names.
- Adds `cot:toronto cot:hasNeighbourhood ...` links.
- Generates ward WKT directly from the official source dataset.
- Keeps census-tract IDs as strings, fixing the malformed legacy `5350378.20` URI issue.
- Reprojects census-tract geometry to WGS84/EPSG:4326 before writing GeoSPARQL WKT.
