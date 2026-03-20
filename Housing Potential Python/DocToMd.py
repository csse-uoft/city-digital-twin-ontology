# -*- coding: utf-8 -*-
"""
DocToMd.py

Author: Anderson Wong

Date: February 3, 2025

Description: This is a Python program that takes a list of .docx files and
converts them to markdown (.md) format
"""

import mammoth
from bs4 import BeautifulSoup
import html2text

def html_to_markdown_preserving_tables(html):
    """
    Convert HTML to Markdown while preserving <table> elements as raw HTML.
    """
    soup = BeautifulSoup(html, "html.parser")
    h = html2text.HTML2Text()
    h.body_width = 0  # prevent line wrapping

    output_lines = []

    for element in soup.contents:
        # Keep tables exactly as HTML
        if element.name == "table":
            output_lines.append(str(element))
        else:
            # Convert everything else to Markdown
            output_lines.append(h.handle(str(element)))

    return "\n\n".join(output_lines)


def convert_docx_to_markdown_with_html_tables(docx_path, md_path):
    """
    Convert a DOCX file to Markdown, preserving tables as HTML.
    """
    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value

    markdown = html_to_markdown_preserving_tables(html)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Converted {docx_path} → {md_path}")


def convert_many(files):
    """
    Convert a list of DOCX files to Markdown.
    """
    for docx_file in files:
        md_file = docx_file.rsplit(".", 1)[0] + ".md"
        convert_docx_to_markdown_with_html_tables(docx_file, md_file)

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
