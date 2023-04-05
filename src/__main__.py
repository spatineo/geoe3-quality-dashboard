import os
from datetime import datetime
from test_extractor_xpath import test__extract_data_api_services
from extract import read_rules_from_json, extract_all_info, extract_rule
from loader import load_dataset_metadata, load_csv
import platform

current_dir = os.getcwd()


def clear_console():
    if platform.system().lower() == "windows":
        os.system("cls")
    else:
        os.system("clear")

def get_user_inputs():
    
    metadata_prompt = "Please enter the path to Metadatafile (if in same folder as program, for instance 'MD_Bui_EX_1.xml'): "
    quality_evaluation_prompt = "Please enter the path to Quality Evaluation file (eg. 'results_NO_cc.csv'): "
    interoperability_prompt = "Please enter the path to Interoperability file (eg. 'interoperability_maturityModel.csv'): "
    service_id_prompt = "Please enter the service ID (list of service Id : 39859,164572,157386,88383,157353): "
    access_key_prompt = "Please enter the Spatineo Monitor API Access Key: "

    metadata_file = input(metadata_prompt)
    qualityEvaluation_file = os.path.join(current_dir, input(quality_evaluation_prompt))
    interoperability_file = os.path.join(current_dir, input(interoperability_prompt))
    serviceId = input(service_id_prompt)
    spatineo_api_access_key = input(access_key_prompt)

    # Pass the private_access_key to the function in extract.py
    test_data_read = read_rules_from_json("Dashboard_structure.json", spatineo_api_access_key)

    # Pass the private_access_key to the function 'test__extract_data_api_services'
    test_result = test__extract_data_api_services(spatineo_api_access_key)


    return metadata_file, qualityEvaluation_file, interoperability_file, serviceId, test_data_read, test_result



def save_dataframes_to_csv(name_excel_file, scores_table, M, E, D, VP):
    scores_table.to_csv(name_excel_file + ".csv", index=False)
    VP.to_csv(name_excel_file + "_VP" + ".csv", index=False)
    D.to_csv(name_excel_file + "_D" + ".csv", index=False)
    E.to_csv(name_excel_file + "_E" + ".csv", index=False)
    M.to_csv(name_excel_file + "_M" + ".csv", index=False)


def main():
    clear_console()

    (
        metadata_file,
        qualityEvaluation_file,
        interoperability_file,
        serviceId,
    ) = get_user_inputs()

    structure_file = read_rules_from_json(os.path.join(current_dir, "Dashboard_structure.json"))

    model = {
        "dataset-metadata": load_dataset_metadata(metadata_file),
        "service-availability": 0,
        "quality-evaluation": load_csv(qualityEvaluation_file),
        "interoperability-maturity-model": load_csv(interoperability_file),
    }

    scores_table, M, E, D, VP = extract_all_info(
        structure_file,
        metadata_file,
        serviceId,
        qualityEvaluation_file,
        interoperability_file,
        func=extract_rule,
    )

    name_excel_file = f"{serviceId}_{metadata_file.replace('.xml', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    save_dataframes_to_csv(name_excel_file, scores_table, M, E, D, VP)

    print("Results have been saved in an Excel file named : ", name_excel_file)


if __name__ == "__main__":
    main()
