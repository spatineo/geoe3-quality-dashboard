import pytest
from src.xml import ns
from src.extract import extract_rule
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

    result = extract_rule(test_rule['extractionRule'], test_model)
    print(f"value extracted via extraction rule: {result}")

    assert result == '2015-12-15'

