import os
import sys
from pathlib import Path
from src.extract import extract_rule
from src.loader import load_dataset_metadata, load_API
import platform

def clear_console():
    if platform.system().lower() == "windows":
        os.system("cls")
    else:
        os.system("clear")

current_file_path = os.path.abspath(__file__)
os.chdir(os.path.dirname(current_file_path))
sys.path.append(str(Path(__file__).resolve().parent.parent))
clear_console()

spatineo_api_access_key = os.environ.get("SPATINEO_API_ACCESS_KEY")

def test__extract_publication_date__text():
    """Test that this xpath extractor with value function ***text*** works"""
    test_model = {"dataset-metadata": load_dataset_metadata("test_MD_Bui_EX_1.xml")}

    test_rule = {
        "extractionRule": {
            "source": "dataset-metadata",
            "type": "xpath",
            "rule": "//gmd:PositionalAccuracy//gmd:AbsolutePositionalAccuracy//gmd:MeanValuePositionalUncertainties",
            "value": "text",
        }
    }

    service_id = test_rule["extractionRule"].get("serviceId", "39859")
    result = extract_rule(test_rule["extractionRule"], test_model, None, service_id)
    print(f"Value extracted via extraction rule: {result}")

    return result


def test__extract_data_api_services():
    test_model = {"dataset-API": load_dataset_metadata("test_MD_Bui_EX_1.xml")}

    test_rule = {
        "extractionRule": {
            "source": "API",
            "type": "dot-notation",
            "serviceId": "39859",
            "url_start": f"https://beta.spatineo-devops.com/api/public/geoe3-dashboard?privateAccessKey={spatineo_api_access_key}&serviceIds=",
            "rule": "['services'][0]['serviceInfo']['type']",
            "value": "text",
        }
    }

    service_id = test_rule["extractionRule"]["serviceId"]
    result = extract_rule(test_rule["extractionRule"], test_model, None, service_id)

    url = test_rule["extractionRule"]["url_start"] + service_id

    api_data, _ = load_API(url, service_id)
    
    services = api_data.get('services', [])
    if services:
        service_info = services[0].get('serviceInfo', {})
        field_value = service_info.get('type', 'Key not found')
    else:
        field_value = 'Key not found'

    print(f"Value extracted via extraction rule: {field_value}")

    return field_value


if __name__ == "__main__":
    # result = test__extract_publication_date__text()
    # print(result)

    field_value = test__extract_data_api_services()
    print(field_value)
