# Buildings

This folder contains the current building-data mapping workflow for the City Digital Twin.

## Overture Maps workflow

The active implementation maps Overture Maps building features into the City Digital Twin RDF model.

### Contents

- **Mappings/** - human-readable Overture building mapping specification.
- **Scripts/** - Overture-to-RDF/Turtle transformation code.
- **Samples/** - small source/output samples retained for reproducibility.
- **Validation/** - validation results from sample and full Toronto runs.
- **Metadata/** - download/release metadata for the full production source.

The full Overture GeoJSONSeq source and the generated production Turtle file are intentionally not stored in GitHub because of their size.

The current full Toronto run processed 569,053 input building features, retained 427,762 buildings within the Toronto boundary, excluded 141,291 outside the boundary, and wrote 7,665,615 RDF triples. First Canadian Place passed the known-example validation.
