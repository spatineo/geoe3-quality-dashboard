from src.xml import ns
import logging

# This function executes xpath extraction rules
def execute_xpath_rule(rule, model):
    """Executes xpath extraction rule and returns the result value"""
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
        logging.warning('Unknown value extraction method (%s) in extractionRule', value_method)

    return result

extractor_by_type = {
    'xpath': execute_xpath_rule
}

def execute_rule(rule, model):
    extractor = extractor_by_type[rule['type']]
    if extractor is None:
        raise f"Unknown rule extractor type {rule['type']}"

    return extractor(rule, model)