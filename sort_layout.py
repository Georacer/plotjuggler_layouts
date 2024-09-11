#!/usr/bin/env python

import xml.etree.ElementTree as ET
import argparse

def sort_xml(xml_file, output_file):

    # Parse the XML file
    tree = ET.parse(xml_file)

    # Call the sorting functions with the provided arguments
    sort_attributes(tree)
    sort_snippets(tree)

    # Write the sorted XML to a new file
    tree.write(output_file, encoding="utf-8", xml_declaration=True)


def sort_attributes(tree):
    root = tree.getroot()

    # Function to sort attributes of an element
    def sort_element_attributes(elem):
        # Sort the element's attributes
        sorted_attrib = dict(sorted(elem.attrib.items()))
        elem.attrib = sorted_attrib

        # Round DockSplitter size resolution
        if elem.tag == 'DockSplitter':
            sizes = elem.attrib['sizes'].split(';')
            elem.attrib['sizes'] = ';'.join([f"{float(size):.2f}" for size in sizes])
        
        # Recursively sort attributes of child elements
        for child in elem:
            sort_element_attributes(child)
    
    # Sort attributes starting from the root element
    sort_element_attributes(root)


def sort_snippets(tree):
    root = tree.getroot()

    matheqs = root.find('customMathEquations')
    matheqs[:] = sorted(matheqs, key=lambda snippet: snippet.get("name"))


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Sort attributes of elements in an XML file.")
    parser.add_argument("input_xml", type=str, help="Path to the input XML file")
    parser.add_argument("output_xml", type=str, help="Path to the output XML file with sorted attributes")

    # Parse the arguments
    args = parser.parse_args()

    # Call the sorting function with the provided arguments
    sort_xml(args.input_xml, args.output_xml)

if __name__ == "__main__":
    main()
