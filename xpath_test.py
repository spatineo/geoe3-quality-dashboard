from lxml import etree
from datetime import datetime
import isodate
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
  },
  'evaluationCriteria': {
    'type': 'date-not-older-than',
    'duration': 'P6M'
  }
}

# This context defines values from the current contaxt that rule evaluation criteria might be evaluated against
test_context = {
  'now': datetime.now()
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
        logging.error(f'Unknown value extraction method ({value_method}) in extractionRule')

    return result

def evaluate_results(eval_criteria, result, context):
    value = (None, "??")
    if eval_criteria['type'] == 'date-not-older-than':
        # result is expected to be in ISO format
        result_as_date = datetime.fromisoformat(result)

        duration = isodate.parse_duration(eval_criteria['duration'])
        reference = context['now'] - duration
        if result_as_date < reference:
            value = (0, f"date {result} older than {eval_criteria['duration']}")
        else:
            value = (1, f"date {result} not older than {eval_criteria['duration']}")
    else:
        value = (None, f"unknown evaluation method {eval_criteria['type']}")

    return value

x = execute_xpath_rule(test_rule['extractionRule'], test_model)
print(f"value extracted via extraction rule: {x}")

z = evaluate_results(test_rule['evaluationCriteria'], x, test_context)
print(f"evaluation result: {z}")