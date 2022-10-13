import pytest
from datetime import datetime
from src.xml import ns
from src.rules import execute_rule
from src.evaluate import evaluate_results
from src.loader import load_dataset_metadata

def test__extract_publication_date():
    test_model = {
        'dataset-metadata': load_dataset_metadata('example-metadata/Dataset MD Bui-ES-5.xml')
    }

    test_rule = {
        'extractionRule': {
            'source': "dataset-metadata",
            'type': "xpath",
            'rule': "gmd:identificationInfo[1]/*/gmd:citation/*/gmd:date[./*/gmd:dateType/*/text()='publication']/*/gmd:date",
            'value': "text"
        }
    }

    result = execute_rule(test_rule['extractionRule'], test_model)
    print(f"value extracted via extraction rule: {result}")

    assert result == '2015-12-15'


def test__date_not_older_than__positive():
    """2015-12-15 should be within 6 months of 2016-01-01"""
    test_rule = {
        'evaluationCriteria': {
            'type': 'date-not-older-than',
            'duration': 'P6M'
        }
    }

    test_context = {
        'now': datetime.fromisoformat('2016-01-01')
    }

    result = '2015-12-15'
    
    (value, explanation) = evaluate_results(test_rule['evaluationCriteria'], result, test_context)

    assert value == 1


def test__date_not_older_than__negative():
    """2015-12-15 should be older than 6 months from 2020-01-01"""
    test_rule = {
        'evaluationCriteria': {
            'type': 'date-not-older-than',
            'duration': 'P6M'
        }
    }

    test_context = {
        'now': datetime.fromisoformat('2020-01-01')
    }

    result = '2015-12-15'
    
    (value, explanation) = evaluate_results(test_rule['evaluationCriteria'], result, test_context)

    assert value == 0
    assert explanation == "date 2015-12-15 older than P6M"