"""This module contains functions to load input data into the model"""

from lxml import etree

from .xml import ns

def load_dataset_metadata(filename):
    """Read metadata file and return the MD_Metadata etree element"""
    tree = etree.parse(filename)
    root = tree.getroot()

    return root.xpath('//gmd:MD_Metadata', namespaces=ns)[0]
