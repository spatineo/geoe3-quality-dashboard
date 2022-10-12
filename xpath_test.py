from lxml import etree
import logging

# Documentation: https://docs.python.org/3/library/xml.etree.elementtree.html#xpath-support

# https://inspire.ec.europa.eu/reports/ImplementingRules/metadata/MD_IR_and_ISO_20081219.pdf

ns = {
    'csw':    'http://www.opengis.net/cat/csw/2.0.2',
    'gmd':    'http://www.isotc211.org/2005/gmd',
    'gco':    'http://www.isotc211.org/2005/gco',
    'gml':    'http://www.opengis.net/gml',
    'gmx':    'http://www.isotc211.org/2005/gmx',
    'xsi':    'http://www.w3.org/2001/XMLSchema-instance',
    'xlink':  'http://www.w3.org/1999/xlink',
    'geonet': 'http://www.fao.org/geonetwork'
}

tree = etree.parse('example-metadata/Dataset MD Bui-ES-5.xml')
root = tree.getroot()

# Produced from service list item
test_model = {
  'dataset-metadata': root.xpath('//gmd:MD_Metadata', namespaces=ns)[0]
}

# This is the metric/dimension/etc from the configuration 
test_rule = {
  'extractionRule': {
    'source': "dataset-metadata",
    'type': "xpath",
    'rule': "gmd:identificationInfo[1]/*/gmd:citation/*/gmd:date[./*/gmd:dateType/*/text()='publication']/*/gmd:date",
    'value': "text"
  }
}

# This function executes xpath extraction rules
def execute_xpath_rule(rule, model):
    def extract_all_text(node_or_nodes, delimiter=' '):
        """extracts all non-whitespace text from an etree node or list of etree nodes"""
        def flatten(list_of_lists):
            return [item for sublist in list_of_lists for item in sublist]

        if isinstance(node_or_nodes, list):
            nodes = node_or_nodes
        else:
            nodes = [node_or_nodes]

        tmp = [
          filter(lambda str : str != '',
            map(lambda str : str.strip(), node.xpath(".//text()"))
          ) for node in nodes]

        return delimiter.join(flatten(tmp))

    source = model[rule['source']]
    xpath_rule = rule['rule']
    value_method = rule['value']


    result = source.xpath(xpath_rule, namespaces=ns)

    if value_method == 'text':
        result = extract_all_text(result)
    else:
        logging.error(f'Unknown value extraction method ({value_method}) in rule')

    return result

x = execute_xpath_rule(test_rule['extractionRule'], test_model)
print(x)
