import os
import extract
from datetime import datetime
from loader import load_dataset_metadata, load_cvs
from extract import read_rules_from_json, extract_all_info, extract_rule

def clear_screen():
    os.system('cls')

def get_user_inputs():
    metadata_file = input("Please enter the path to Metadatafile (if in same folder as program, for instance 'MD_Bui_EX_1.xml'):")
    qualityEvaluation_file = input("Please enter the path to Metadatafile (eg. 'C:/Users/CCOSSEC/Work Folders/Evaluator configuration/geoe3-quality-dashboard/geoe3-quality-dashboard/src/buildings_and_errors/results_NO_cc.csv'): ")
    interoperability_file = input("Please enter the path to Metadatafile (eg. 'C:/Users/CCOSSEC/Work Folders/Evaluator configuration/geoe3-quality-dashboard/geoe3-quality-dashboard/src/interoperability_maturityModel.csv'): ") 
    serviceId = input("Please enter the service ID (list of service Id : 39859,164572,157386,88383,157353) :")
    privateAccessKey = input("Please enter the Spatineo Monitor Private Access Key")
    
    # Pass the private_access_key to the function in extract.py
    extracted_data = extract.read_rules_from_json('Dashboard_structure.json', privateAccessKey)
    
    # Pass the private_access_key to the function 'test__extract_data_api_services'
    extracted_data = extract.test__extract_data_api_services('Dashboard_structure.json', privateAccessKey)

    return metadata_file, qualityEvaluation_file, interoperability_file, serviceId

def save_dataframes_to_csv(name_excel_file, scores_table, M, E, D, VP):
    scores_table.to_csv(name_excel_file + '.csv', index=False)
    VP.to_csv(name_excel_file + '_VP' + '.csv', index=False)
    D.to_csv(name_excel_file + '_D' + '.csv', index=False)
    E.to_csv(name_excel_file + '_E' + '.csv', index=False)
    M.to_csv(name_excel_file + '_M' + '.csv', index=False)

def main():
    clear_screen()

    metadata_file, qualityEvaluation_file, interoperability_file, serviceId = get_user_inputs()

    structure_file = read_rules_from_json("C:/Users/CCOSSEC/Work Folders/Evaluator configuration/geoe3-quality-dashboard/geoe3-quality-dashboard/Dashboard_structure.json")

    model = {
        'dataset-metadata': load_dataset_metadata(metadata_file),
        'service-availability': 0,
        'quality-evaluation': load_cvs(qualityEvaluation_file),
        'interoperability-maturity-model': load_cvs(interoperability_file)
    }

    scores_table, M, E, D, VP = extract_all_info(structure_file, metadata_file, serviceId, qualityEvaluation_file, interoperability_file, func=extract_rule)

    name_excel_file = f"{serviceId}_{metadata_file.replace('.xml', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    save_dataframes_to_csv(name_excel_file, scores_table, M, E, D, VP)
    
    print('Results have been saved in an Excel file named : ', name_excel_file)

if __name__ == '__main__':
    main()
