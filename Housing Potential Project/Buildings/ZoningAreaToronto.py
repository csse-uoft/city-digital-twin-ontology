#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Toronto Zoning Area (CSV) -> RDF/Turtle (HPCDM-style, single-file script)

- Input: CSV with columns like:
  _id,GEN_ZONE,ZN_ZONE,ZN_HOLDING,HOLDING_ID,FRONTAGE,ZN_AREA,UNITS,DENSITY,
  COVERAGE,FSI_TOTAL,PRCNT_COMM,PRCNT_RES,PRCNT_EMMP,PRCNT_OFFC,ZN_EXCPTN,
  EXCPTN_NO,STAND_SET,ZN_STATUS,ZN_STRING,AREA_UNITS,ZBL_CHAPT,ZBL_SECTN,
  ZBL_EXCPTN,geometry

- geometry: stringified GeoJSON Polygon/MultiPolygon in EPSG:4326 (as in your sample)
- Skips rows with ZN_STATUS == 5
- Treats numeric -1 as "no value" (skips emitting those controls)
"""
from argparse import Namespace

CSV_PATH = "zoning-area-4326.csv"     # path to your CSV
OUT_TTL  = "toronto_zone.ttl"       # where to write TTL

import pandas as pd
import rdflib
from rdflib import Graph, Namespace, Literal, RDF, XSD, RDFS
from pathlib import Path
import json, math, re
import requests, pandas as pd
from shapely.geometry import shape
from shapely import to_wkt, is_valid, make_valid

BASE = "https://ckan0.cf.opendata.inter.prod-toronto.ca"

# get the datastore-active resource id
pkg = requests.get(f"{BASE}/api/3/action/package_show", params={"id": "zoning-by-law"}).json()
rid = next(r["id"] for r in pkg["result"]["resources"] if r.get("datastore_active"))

df = pd.read_csv(f"{BASE}/datastore/dump/{rid}")


# ---------------------- Namespaces (Not sure if they are correct URIs) ----------------
toronto = Namespace("http://ontology.eil.utoronto.ca/Toronto/Toronto#")
hpcdm = Namespace("http://ontology.eil.utoronto.ca/HPCDM/")
gen = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/GenericProperties/")
opr = Namespace("http://www.theworldavatar.com/ontology/ontoplanningregulation/OntoPlanningRegulation.owl#")
geo = Namespace("http://www.opengis.net/ont/geosparql#")
mer = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/Mereology/")
bylaw = Namespace("https://standards.iso.org/iso-iec/5087/-2/ed-1/en/ontology/Bylaw/")
loc = Namespace("https://standards.iso.org/iso-iec/5087/-1/ed-1/en/ontology/SpatialLoc/")
I72 = Namespace("http://ontology.eil.utoronto.ca/ISO21972/iso21972#")

# -----------------------------------------------------------------

def slugify(val):
    zoning_codes = {
        0: "Residential",
        1: "Open_Space",
        2: "Utility_and_Transportation",
        4: "Employment_Industrial",
        5: "Institutional",
        6: "Commercial_Residential_Employment",
        101: "Residential_Apartment",
        201: "Commercial",
        202: "Commercial_Residential",
    }
    if isinstance(val, tuple):
        if val[0] == "GEN_ZONE":
            return zoning_codes[int(val[1])]
        if val[0] == "ZN_ZONE":
            return val[1]
    else:
        s = str(val).strip().lower()
        s = re.sub(r"[^a-z0-9]+", "_", s)
        s = re.sub(r"_+", "_", s).strip("_")
        return s or "na"

g = Graph()
g.bind('tor', toronto)
g.bind('hp', hpcdm)
g.bind('geo', geo)
g.bind('opr', opr)
g.bind('mer', mer)
g.bind('bylaw', bylaw)
g.bind('loc', loc)
g.bind('i72', I72)
g.bind('genprop', gen)

# Global by-law node
zbl = toronto["zoning_by-law_569-2013"]
hold = toronto["holding_zone"]
frontage_var = toronto["frontage_var"]
area_var = toronto["area_var"]
units_var = toronto["num_dwellings_var"]
density_var = toronto["density_var"]
zone_pop = toronto["zone_population"]
tor_pop = toronto["TorontoZonePopulation"]
lot_pop = toronto["lot_population"]


g.add((zbl, RDF.type, hpcdm.ZoningBylaw))
g.add((zbl, bylaw.legislationIdentifier, Literal("ZONING_BY-LAW_569-2013", datatype=XSD.string)))

g.add((frontage_var, I72.hasName, hpcdm.hasFrontage))
g.add((area_var, I72.hasName, hpcdm.hasArea))
g.add((units_var, I72.hasName, hpcdm.hasNumDwellings))
g.add((density_var, I72.hasName, hpcdm.hasFSI))

g.add((zone_pop, RDF.type, tor_pop))
g.add((lot_pop, RDF.type, tor_pop))

g.add((lot_pop, RDFS.subClassOf, I72.Population))
g.add((tor_pop, I72.located_in,
       rdflib.URIRef("https://www.geonames.org/6167865/toronto.html")))
g.add((tor_pop, I72.defined_by, hpcdm.Lot))
g.add((tor_pop, I72.defined_by, hpcdm.AdministrativeArea))
g.add((hpcdm.AdministrativeArea, I72.definedFor, tor_pop))

for _, row in df.iterrows():
    # Skip non-by-law areas
    if str(row.get("ZN_STATUS", "")).strip() == "5":
        continue

    rid = row.get("_id")

    # Geometry from CSV 'geometry' column (stringified GeoJSON)
    geom_txt = row.get("geometry")


    area = toronto[f"area_{rid}"]
    geom = toronto[f"area_{rid}_geometry"]

    # OBJECTID
    reg = toronto[f"zoning_reg_{rid}"]
    g.add((zbl, hpcdm.definesRegulation, reg))
    g.add((reg, RDF.type, hpcdm.Regulation))
    g.add((reg, RDF.type, hpcdm.Regulation))

    g.add((reg, hpcdm.definedFor, area))
    g.add((reg, hpcdm.definedIn, zbl))

    g.add((area, RDF.type, hpcdm.AdministrativeArea))

    # geometry
    if geom_txt:
        try:
            geom_dict = json.loads(geom_txt)
            geom_obj = shape(geom_dict)

            if not is_valid(geom_obj):
                geom_obj = make_valid(geom_obj)

            if not geom_obj.is_empty:
                wkt_out = to_wkt(geom_obj, rounding_precision=-1)
                g.add((geom, geo.asWKT, Literal(wkt_out, datatype=geo.wktLiteral)))
                g.add((area, loc.hasLocation, geom))
        except Exception as e:
            print(f"Skipping geometry for _id={rid}: {e}")

    # Zoning hierarchy
    gen_zone = row.get("GEN_ZONE")
    zn_zone  = row.get("ZN_ZONE")
    zn_str   = row.get("ZN_STRING")

    z_gen = z_mid = z_full = None
    if pd.notna(gen_zone):
        z_gen = toronto[f"zone_{slugify(('GEN_ZONE', gen_zone))}"]
        g.add((reg, hpcdm.designatesZoningType, z_gen))

    if pd.notna(zn_zone):
        z_mid = toronto[f"zone_{slugify(('ZN_ZONE', zn_zone))}"]
        g.add((reg, hpcdm.designatesZoningType, z_mid))
        if z_gen:
            g.add((z_gen, hpcdm.subZoningType, z_mid))

    if pd.notna(zn_str):
        z_full = toronto[f"zone_{slugify(zn_str)}"]
        g.add((reg, hpcdm.designatesZoningType, z_full))
        if z_mid:
            g.add((z_mid, hpcdm.subZoningType, z_full))


    # By-law parts (varied header spellings)
    ch = row.get("ZBL_CHAPT")
    se = row.get("ZBL_SECTN")
    ex = row.get("ZBL_EXCPTN")

    ch_node = se_node = ex_node = None
    if pd.notna(ex):
        ex = str(ex).strip()
        ex_node = toronto[f"zoning_by-law_569-2013_{slugify(ex)}"]
        g.add((zbl, mer.hasProperPart, ex_node))
        g.add((ex_node, RDF.type, hpcdm.ZoningBylawPart))
        g.add((ex_node, gen.hasIdentifier, Literal(str(ex), datatype=XSD.string)))
    if pd.notna(se):
        se = str(se).strip()
        se_node = toronto[f"zoning_by-law_569-2013_SECTN{slugify(se)}"]
        g.add((se_node, RDF.type, hpcdm.ZoningBylawPart))
        g.add((se_node, gen.hasIdentifier, Literal(float(se), datatype=XSD.decimal)))
        if z_mid:
            g.add((z_mid, hpcdm.definedIn, se_node))
    if pd.notna(ch):
        ch = str(ch).strip()
        ch_node = toronto[f"zoning_by-law_569-2013_CH{ch}"]
        g.add((zbl, mer.hasProperPart, ch_node))
        g.add((ch_node, RDF.type, hpcdm.ZoningBylawPart))
        g.add((ch_node, gen.hasIdentifier, Literal(int(ch), datatype=XSD.integer)))
        if se_node:
            g.add((ch_node, mer.hasProperPart, se_node))

    zn_holding = row.get("ZN_HOLDING")
    holding_id = row.get("HOLDING_ID")
    if zn_holding == "Y" and holding_id:
        hz = toronto[f"holding_reg_{rid}"]
        g.add((hz, RDF.type, hpcdm.Regulation))
        g.add((hz, hpcdm.definedFor, area))
        g.add((hz, hpcdm.designatesZone, hold))
        if not pd.isna(holding_id):
            g.add((hz, gen.hasIdentifier, Literal(holding_id, datatype=XSD.integer)))

    # Exception
    zn_exc = row.get("ZN_EXCPTN")
    exc_no = row.get("EXCPTN_NO")

    if zn_exc == "Y" and exc_no:
        ex_reg = toronto[f"{slugify(zn_zone)}_{exc_no}"]
        g.add((ex_reg, hpcdm.definedIn, ex_node))
        if z_full:
            g.add((z_full, hpcdm.definesZoningException, ex_reg))

    # ---------- Numeric controls ----------
    FRONTAGE   = row.get("FRONTAGE")
    ZN_AREA    = row.get("ZN_AREA")
    AREA_UNITS = row.get("AREA_UNITS")
    UNITS      = row.get("UNITS")
    DENSITY    = row.get("DENSITY")
    FSI_TOTAL  = row.get("FSI_TOTAL")
    COVERAGE   = row.get("COVERAGE")
    PRCNT_COMM = row.get("PRCNT_COMM")
    PRCNT_RES  = row.get("PRCNT_RES")
    PRCNT_EMMP = row.get("PRCNT_EMMP")
    PRCNT_OFFC = row.get("PRCNT_OFFC")

    # STAND = row.get("STAND_SET")


    if not pd.isna(FRONTAGE) and zn_str:
        constraint = toronto[f"{slugify(zn_str)}_regulation_constraints"]
        units = toronto[f"min_frontage_{slugify(zn_str)}"]
        spec = toronto[f"min_frontage_{slugify(zn_str)}_specification"]
        restriction = toronto[f"zone_{slugify(zn_str)}_lots_min_frontage"]
        pop = toronto[f"lot_population_in_zone_{slugify(zn_str)}"]
        pop = toronto[f"lot_population_in_zone_{slugify(zn_str)}"]
        pop_type = toronto[f"TorontoLotPopulation_Zone{slugify(zn_str)}"]

        g.add((constraint, RDF.type, hpcdm.Regulation))
        g.add((constraint, hpcdm.definedIn, zbl))
        g.add((constraint, opr.forZoningType, z_full))
        g.add((constraint, hpcdm.specifiesConstraint, units))
        g.add((constraint, gen.hasName, Literal(f"Zone String {slugify(zn_str)}", datatype=XSD.string)))

        g.add((units, RDF.type, hpcdm.QuantityRequirement))
        g.add((units, I72.hasValue, spec))
        g.add((spec, I72.hasNumericalValue, Literal(FRONTAGE, datatype=XSD.decimal)))
        g.add((spec, I72.hasUnit, I72.metre))

        g.add((units, hpcdm.specifiesMinimumFor, restriction))
        g.add((restriction, RDF.type, hpcdm.Minimum))
        g.add((restriction, I72.parameter_of_var, frontage_var))
        g.add((restriction, hpcdm.minimumOf, pop))

        g.add((pop, RDF.type, pop_type))

        g.add((pop_type, RDFS.subClassOf, toronto.TorontoLotPopulation))
        g.add((pop_type, I72.located_in,
               rdflib.URIRef("https://www.geonames.org/6167865/toronto.html")))
        g.add((pop_type, I72.defined_by, hpcdm.Lot))
        g.add((pop_type, hpcdm.hasZone, z_full))

    if not pd.isna(ZN_AREA) and zn_str:
        constraint = toronto[f"{slugify(zn_str)}_regulation_constraints"]
        units = toronto[f"min_area_{slugify(zn_str)}"]
        spec = toronto[f"min_area_{slugify(zn_str)}_specification"]
        restriction = toronto[f"zone_{slugify(zn_str)}_lots_min_area"]
        pop = toronto[f"lot_population_in_zone_{slugify(zn_str)}"]
        pop_type = toronto[f"TorontoLotPopulation_Zone{slugify(zn_str)}"]

        g.add((constraint, RDF.type, hpcdm.Regulation))
        g.add((constraint, hpcdm.definedIn, zbl))
        g.add((constraint, opr.forZoningType, z_full))
        g.add((constraint, hpcdm.specifiesConstraint, units))
        g.add((constraint, gen.hasName, Literal(f"Zone String {slugify(zn_str)}", datatype=XSD.string)))

        g.add((units, RDF.type, hpcdm.QuantityRequirement))
        g.add((units, I72.hasValue, spec))
        g.add((spec, I72.hasNumericalValue, Literal(ZN_AREA, datatype=XSD.integer)))
        g.add((spec, I72.hasUnit, I72.square_metre))

        g.add((units, hpcdm.specifiesMinimumFor, restriction))
        g.add((restriction, RDF.type, hpcdm.Minimum))
        g.add((restriction, I72.parameter_of_var, area_var))
        g.add((restriction, hpcdm.minimumOf, pop))

        g.add((pop, RDF.type, pop_type))

        g.add((pop_type, RDFS.subClassOf, toronto.TorontoLotPopulation))
        g.add((pop_type, I72.located_in,
               rdflib.URIRef("https://www.geonames.org/6167865/toronto.html")))
        g.add((pop_type, I72.defined_by, hpcdm.Lot))
        g.add((pop_type, hpcdm.hasZone, z_full))


    if not pd.isna(UNITS) and zn_str:
        constraint = toronto[f"{slugify(zn_str)}_regulation_constraints"]
        units = toronto[f"max_units_{slugify(zn_str)}"]
        spec = toronto[f"max_units_{slugify(zn_str)}_specification"]
        restriction = toronto[f"zone_{slugify(zn_str)}_lots_max_dwelling"]
        pop = toronto[f"lot_population_in_zone_{slugify(zn_str)}"]
        pop_type = toronto[f"TorontoLotPopulation_Zone{slugify(zn_str)}"]

        g.add((constraint, RDF.type, hpcdm.Regulation))
        g.add((constraint, hpcdm.definedIn, zbl))
        g.add((constraint, opr.forZoningType, z_full))
        g.add((constraint, hpcdm.specifiesConstraint, units))
        g.add((constraint, gen.hasName, Literal(f"Zone String {slugify(zn_str)}", datatype=XSD.string)))

        g.add((units, RDF.type, hpcdm.QuantityAllowance))
        g.add((units, I72.hasValue, spec))
        g.add((spec, I72.hasNumericalValue, Literal(UNITS, datatype=XSD.integer)))
        g.add((spec, I72.hasUnit, I72.population_cardinality_unit))

        g.add((units, hpcdm.specifiesMaximumFor, restriction))
        g.add((restriction, RDF.type, hpcdm.Maximum))
        g.add((restriction, I72.parameter_of_var, units_var))
        g.add((restriction, hpcdm.maximumOf, pop))

        g.add((pop, RDF.type, pop_type))

        g.add((pop_type, RDFS.subClassOf, toronto.TorontoLotPopulation))
        g.add((pop_type, I72.located_in,
               rdflib.URIRef("https://www.geonames.org/6167865/toronto.html")))
        g.add((pop_type, I72.defined_by, hpcdm.Lot))


    if not pd.isna(DENSITY) and zn_str:
        constraint = toronto[f"{slugify(zn_str)}_regulation_constraints"]
        units = toronto[f"max_density_{slugify(zn_str)}"]
        spec = toronto[f"max_density_{slugify(zn_str)}_specification"]
        restriction = toronto[f"zone_{slugify(zn_str)}_lots_max_density"]
        pop = toronto[f"lot_population_in_zone_{slugify(zn_str)}"]
        pop_type = toronto[f"TorontoLotPopulation_Zone{slugify(zn_str)}"]

        g.add((constraint, RDF.type, hpcdm.Regulation))
        g.add((constraint, hpcdm.definedIn, zbl))
        g.add((constraint, opr.forZoningType, z_full))
        g.add((constraint, hpcdm.specifiesConstraint, units))
        g.add((constraint, gen.hasName, Literal(f"Zone String {slugify(zn_str)}", datatype=XSD.string)))

        g.add((units, RDF.type, hpcdm.QuantityAllowance))
        g.add((units, I72.hasValue, spec))
        g.add((spec, I72.hasNumericalValue, Literal(DENSITY, datatype=XSD.decimal)))

        g.add((units, hpcdm.specifiesMaximumFor, restriction))
        g.add((restriction, RDF.type, hpcdm.Maximum))
        g.add((restriction, I72.parameter_of_var, density_var))
        g.add((restriction, hpcdm.maximumOf, pop))

        g.add((pop, RDF.type, pop_type))

        g.add((pop_type, RDFS.subClassOf, toronto.TorontoLotPopulation))
        g.add((pop_type, I72.located_in,
               rdflib.URIRef("https://www.geonames.org/6167865/toronto.html")))
        g.add((pop_type, I72.defined_by, hpcdm.Lot))
        g.add((pop_type, hpcdm.hasZone, z_full))


    if not pd.isna(FSI_TOTAL) and zn_str:
        constraint = toronto[f"{slugify(zn_str)}_fsi_total"]
        units = toronto[f"max_fsi_total_{slugify(zn_str)}"]
        spec = toronto[f"max_fsi_total_{slugify(zn_str)}_measure"]

        g.add((constraint, RDF.type, hpcdm.Regulation))
        g.add((constraint, hpcdm.definedIn, zbl))
        g.add((constraint, opr.forZoningType, z_full))
        g.add((constraint, hpcdm.specifiesAllowance, units))
        g.add((constraint, hpcdm.onPopulation, zone_pop))
        g.add((constraint, gen.hasName, Literal(f"Zone String {slugify(zn_str)}", datatype=XSD.string)))

        g.add((units, RDF.type, hpcdm.ZoneFSI))
        g.add((units, RDFS.subClassOf, hpcdm.RatioQuantity))
        g.add((units, I72.numerator, toronto.ZoneGFA))
        g.add((units, I72.denominator, toronto.ZoneLotArea))

        g.add((units, I72.hasValue, spec))
        g.add((spec, I72.hasNumericalValue, Literal(FSI_TOTAL, datatype=XSD.decimal)))

    if not pd.isna(PRCNT_COMM) and zn_str:
        constraint = toronto[f"{slugify(zn_str)}_comm_fsi"]
        units = toronto[f"max_comm_fsi_{slugify(zn_str)}"]
        spec = toronto[f"max_comm_fsi_{slugify(zn_str)}_measure"]

        g.add((constraint, RDF.type, hpcdm.Regulation))
        g.add((constraint, hpcdm.definedIn, zbl))
        g.add((constraint, opr.forZoningType, z_full))
        g.add((constraint, hpcdm.specifiesAllowance, units))
        g.add((constraint, hpcdm.onPopulation, lot_pop))
        g.add((constraint, gen.hasName, Literal(f"Zone String {slugify(zn_str)}", datatype=XSD.string)))

        g.add((units, RDF.type, hpcdm.CommFSI))
        g.add((units, RDFS.subClassOf, hpcdm.FSI))
        g.add((units, I72.numerator, toronto.CommGFA))
        g.add((units, I72.denominator, toronto.LotArea))

        g.add((units, I72.hasValue, spec))
        g.add((spec, I72.hasNumericalValue, Literal(PRCNT_COMM, datatype=XSD.decimal)))


    if not pd.isna(PRCNT_RES) and zn_str:
        constraint = toronto[f"{slugify(zn_str)}_res_fsi"]
        units = toronto[f"max_res_fsi_{slugify(zn_str)}"]
        spec = toronto[f"max_res_fsi_{slugify(zn_str)}_measure"]

        g.add((constraint, RDF.type, hpcdm.Regulation))
        g.add((constraint, hpcdm.definedIn, zbl))
        g.add((constraint, opr.forZoningType, z_full))
        g.add((constraint, hpcdm.specifiesAllowance, units))
        g.add((constraint, hpcdm.onPopulation, lot_pop))
        g.add((constraint, gen.hasName, Literal(f"Zone String {slugify(zn_str)}", datatype=XSD.string)))

        g.add((units, RDF.type, hpcdm.ResFSI))
        g.add((units, RDFS.subClassOf, hpcdm.FSI))
        g.add((units, I72.numerator, toronto.ResGFA))
        g.add((units, I72.denominator, toronto.LotArea))

        g.add((units, I72.hasValue, spec))
        g.add((spec, I72.hasNumericalValue, Literal(PRCNT_RES, datatype=XSD.decimal)))


    if not pd.isna(PRCNT_EMMP) and zn_str:
        constraint = toronto[f"{slugify(zn_str)}_emmp_fsi"]
        units = toronto[f"max_emmp_fsi_{slugify(zn_str)}"]
        spec = toronto[f"max_emmp_fsi_{slugify(zn_str)}_measure"]

        g.add((constraint, RDF.type, hpcdm.Regulation))
        g.add((constraint, hpcdm.definedIn, zbl))
        g.add((constraint, opr.forZoningType, z_full))
        g.add((constraint, hpcdm.specifiesAllowance, units))
        g.add((constraint, hpcdm.onPopulation, lot_pop))
        g.add((constraint, gen.hasName, Literal(f"Zone String {slugify(zn_str)}", datatype=XSD.string)))

        g.add((units, RDF.type, hpcdm.EmmpFSI))
        g.add((units, RDFS.subClassOf, hpcdm.FSI))
        g.add((units, I72.numerator, toronto.EmmpGFA))
        g.add((units, I72.denominator, toronto.LotArea))

        g.add((units, I72.hasValue, spec))
        g.add((spec, I72.hasNumericalValue, Literal(PRCNT_EMMP, datatype=XSD.decimal)))

    if not pd.isna(PRCNT_OFFC) and zn_str:
        constraint = toronto[f"{slugify(zn_str)}_offc_fsi"]
        units = toronto[f"max_offc_fsi_{slugify(zn_str)}"]
        spec = toronto[f"max_offc_fsi_{slugify(zn_str)}_measure"]

        g.add((constraint, RDF.type, hpcdm.Regulation))
        g.add((constraint, hpcdm.definedIn, zbl))
        g.add((constraint, opr.forZoningType, z_full))
        g.add((constraint, hpcdm.specifiesAllowance, units))
        g.add((constraint, hpcdm.onPopulation, lot_pop))
        g.add((constraint, gen.hasName, Literal(f"Zone String {slugify(zn_str)}", datatype=XSD.string)))

        g.add((units, RDF.type, hpcdm.OffcFSI))
        g.add((units, RDFS.subClassOf, hpcdm.FSI))
        g.add((units, I72.numerator, toronto.OffcGFA))
        g.add((units, I72.denominator, toronto.LotArea))

        g.add((units, I72.hasValue, spec))
        g.add((spec, I72.hasNumericalValue, Literal(PRCNT_OFFC, datatype=XSD.decimal)))


    if not pd.isna(AREA_UNITS) and zn_str:
        constraint = toronto[f"{slugify(zn_str)}_area_units"]
        units = toronto[f"min_area_units_{slugify(zn_str)}"]
        spec = toronto[f"min_area_units_{slugify(zn_str)}_measure"]

        g.add((constraint, RDF.type, hpcdm.Regulation))
        g.add((constraint, hpcdm.definedIn, zbl))
        g.add((constraint, opr.forZoningType, z_full))
        g.add((constraint, hpcdm.specifiesAllowance, units))
        g.add((constraint, hpcdm.onPopulation, lot_pop))
        g.add((constraint, gen.hasName, Literal(f"Zone String {slugify(zn_str)}", datatype=XSD.string)))

        g.add((units, RDF.type, hpcdm.AreaUnits))
        g.add((units, RDFS.subClassOf, hpcdm.RatioQuantity))
        g.add((units, I72.denominator, hpcdm.NumberOfDwellings))
        g.add((units, I72.numerator, hpcdm.LotArea))

        g.add((units, I72.hasValue, spec))
        g.add((spec, I72.hasNumericalValue, Literal(AREA_UNITS, datatype=XSD.integer)))

Path(OUT_TTL).parent.mkdir(parents=True, exist_ok=True)
g.serialize(destination=str(OUT_TTL), format="turtle")
print(f"TTL written -> {OUT_TTL}")
