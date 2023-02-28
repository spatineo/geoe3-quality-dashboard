import os
from loader import load_dataset_metadata
from loader import load_cvs
from extract import read_rules_from_json
from extract import extract_all_info
from extract import extract_rule
from datetime import datetime

def main():
    clear = lambda: os.system('cls')
    clear()

    # Ask for location of files for metadata and quality evaluation results from GeoE3 software
    metadata_file = input("Please enter the path to Metadatafile (if in same folder as program, for instance 'MD_Bui_EX_1.xml'):")
    qualityEvaluation_file = input("Please enter the path to Metadatafile (eg. 'C:/Users/CCOSSEC/Work Folders/Evaluator configuration/geoe3-quality-dashboard/geoe3-quality-dashboard/src/buildings_and_errors/results_NO_cc.csv'):")
    # Ask for service ID of service we want the availability analysis from.
    serviceId = input("Please enter the service ID (list of service Id : 39859,164572,157386,88383,157353) :")
    # Read rules from JSON file that describes the structure of the dashboard and its rules.

    structure_file = read_rules_from_json("C:/Users/CCOSSEC/Work Folders/Evaluator configuration/geoe3-quality-dashboard/geoe3-quality-dashboard/Dashboard_structure.json")
    
    '''JUST FOR TESTING PHASE:
    metadata_file = 'MD_Bui_EX_1.xml'
    qualityEvaluation_file = 'C:/Users/CCOSSEC/Work Folders/Evaluator configuration/geoe3-quality-dashboard/geoe3-quality-dashboard/src/buildings_and_errors/results_NO_cc.csv'
    serviceId = '157353'
    JUST FOR TESTING PHASE:'''


    # Define model object
    model = {
    'dataset-metadata': load_dataset_metadata(metadata_file),
    'service-availability': 0,
    'quality-evaluation': load_cvs(qualityEvaluation_file)
    }
    # Extract rules from Structure file (JSON) and executes them. Result is a Dataframe table
    extractionRule_table, scores_table = extract_all_info(structure_file, metadata_file, serviceId, qualityEvaluation_file, func = extract_rule)
    
    # Save the DataFrames to an csv file  
    name_excel_file = serviceId + '_' + metadata_file.replace('.xml', '') + '_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.csv'
    scores_table.to_csv(name_excel_file, index=False)
    print('Results have been saved in an Excel file named : ', name_excel_file)






if __name__ == '__main__':
    main()