# Clear the console
import os
clear = lambda: os.system('cls')
clear()


"""Unit tests for xpath extractor"""
import sys
sys.path.append('C:/Users/CCOSSEC/Work Folders/Evaluator configuration/geoe3-quality-dashboard/geoe3-quality-dashboard/src/')
from extract import extract_rule

import xml.etree.ElementTree as ET
from loader import load_dataset_metadata

def test__extract_publication_date__text():
    """Test that this xpath extractor with value function ***text*** works"""
    test_model = {
        'dataset-metadata': load_dataset_metadata('test_MD_Bui_EX_1.xml')
    }

    test_rule = {
        'extractionRule': {
            'source': "dataset-metadata",
            'type': "xpath",
            'rule': "//gmd:PositionalAccuracy//gmd:AbsolutePositionalAccuracy//gmd:MeanValuePositionalUncertainties",
            'value': "text"
        }
    }

    result = extract_rule(test_rule['extractionRule'], test_model)
    print(f"Value extracted via extraction rule: {result}")
    # assert result[0] == 'continual'

    return result


"""Unit tests for API extractor"""

from loader import load_API

def test__extract_data_api_services():
    # Create URL with requested service Id
    # list of service Id :   39859,164572,157386,88383,157353

    test_model = {
        'dataset-API': load_dataset_metadata('test_MD_Bui_EX_1.xml')
    }

    test_rule = {
        'extractionRule': {
            'source': "API",
            'type': "dot-notation",
            'serviceId': "39859",
            'url_start': "https://beta.spatineo-devops.com/api/public/geoe3-dashboard?privateAccessKey=RoYjl8a3NbJ3tx1Hh0-IK6iP55i3YnAhSpcWcD2xgwSE8jBBP0EA9Q&serviceIds=",
            'rule': "['services'][0]['serviceInfo']['type']",
            'value': "text"
        }
    }

    result = extract_rule(test_rule['extractionRule'], test_model)

    url_join = [url_start, serviceId]
    url = "".join(url_join)

    # Get data from API
    api_data = load_API(url)

    # Gets requested field from API data
    field_value = api_data['services'][0]['serviceInfo']['type']
    
    print(f"Value extracted via extraction rule: {field_value}")

    return field_value


#result = test__extract_publication_date__text()
#print(result)

field_value = test__extract_data_api_services()
print(field_value)
