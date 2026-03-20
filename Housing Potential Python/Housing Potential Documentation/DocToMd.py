# -*- coding: utf-8 -*-
"""
DocToMd.py

Author: Anderson Wong

Date: February 3, 2025

Description: This is a Python program that takes a list of .docx files and
converts them to markdown (.md) format using pypandocs
"""

import pypandoc

def convert_many(files):
    for docx_file in files:
        # Create output filename by replacing .docx with .md
        md_file = docx_file.rsplit(".", 1)[0] + ".md"

        print(f"Converting {docx_file} → {md_file}")

        output = pypandoc.convert_file(
            docx_file,
            "gfm"  
        )

        with open(md_file, "w", encoding="utf-8") as f:
            f.write(output)

    print("All conversions complete!")

files_to_convert = [
    "Building and Parcel Documentation.docx",
    "Transit Documentation.docx",
    "Solid Waste Documentation.docx",
    "Power Documentation.docx",
    "Supermarket Documentation.docx",
    "Hospital Documentation.docx",
    "Parks Documentation.docx",
    "Public Schools Documentation.docx",
    "Childcare Documentation.docx",
    "CACensus Python Documentation.docx",
    "Community Centre Documentation.docx",
    "Long Term Care Documentation.docx",
    "Wastewater Documentation.docx"
]

convert_many(files_to_convert)
