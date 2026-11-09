# Administrative Areas

This folder contains the active Toronto administrative-area mapping workflow.

The current implementation maps Toronto wards, neighbourhoods, and census tracts and uses the ISO/IEC 5087-2 `city:administrativeAreaOf` relationship to associate each administrative area with the City of Toronto.

## Contents

- `Scripts/Toronto_Admin_Areas.py` - RDF/Turtle generation and validation.
- `Diagrams/AdministrativeAreas.png` - administrative-area ontology diagram.
- `Validation/` - validation outputs from the current implementation.

This implementation addresses GitHub issue #1, "Missing administrative area - city relationship."
