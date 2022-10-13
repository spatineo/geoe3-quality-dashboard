from src.xml import ns
from lxml import etree

def load_dataset_metadata(filename):
    tree = etree.parse(filename)
    root = tree.getroot()

    return root.xpath('//gmd:MD_Metadata', namespaces=ns)[0]
