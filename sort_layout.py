#!/usr/bin/env python

import xml.etree.ElementTree as ET
import argparse

def sort_attributes(xml_file, output_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Function to sort attributes of an element
    def sort_element_attributes(elem):
        # Sort the element's attributes
        sorted_attrib = dict(sorted(elem.attrib.items()))
        elem.attrib = sorted_attrib
        
        # Recursively sort attributes of child elements
        for child in elem:
            sort_element_attributes(child)
    
    # Sort attributes starting from the root element
    sort_element_attributes(root)

    # Write the sorted XML to a new file
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Sort attributes of elements in an XML file.")
    parser.add_argument("input_xml", type=str, help="Path to the input XML file")
    parser.add_argument("output_xml", type=str, help="Path to the output XML file with sorted attributes")

    # Parse the arguments
    args = parser.parse_args()

    # Call the sorting function with the provided arguments
    sort_attributes(args.input_xml, args.output_xml)

if __name__ == "__main__":
    main()
