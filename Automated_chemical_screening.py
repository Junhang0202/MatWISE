import Chemical_material
import pandas as pd
import os
import openai
import logging
openai.api_key = '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'

data = pd.DataFrame(columns=['entity','IUPACname','solid','soluble','filter'])

data_path = os.path.join(os.getcwd(), 'sample_data', 'sample_materials_for_screening.csv')
df = pd.read_csv(data_path)
#df = pd.read_csv(os.getcwd()+'/experiment_data/gpt4_entity.csv')

data['filter']=0
logging.basicConfig(filename='gpt4_api_errors.log', level=logging.ERROR)

def test_agent(task):
    try:
        chem_model = Chemical_material.Chembot(model="gpt-4", temp=0.1, max_iterations=2)
        return chem_model.run_sc(task)
    except openai.error.APIError as e:
        error_message = f"Caught an Error: {e}. Skipping this {task} task."
        print(error_message)
        logging.error(error_message)  # Log the error
        return None

try:
    for i in range(len(df)):
        chemical_materials = df['entity'][i]
        if isinstance(chemical_materials, str):
            chemical_materials = chemical_materials.split(',')
        for chemical_material in chemical_materials:
            print("Entity:", chemical_material.strip())
            filtered_chemical_material = []
            logging.info(f"Entity name:\n {chemical_material}") 
            task1 = f"Is {chemical_material} solid?"
            task2 = f"Is {chemical_material} soluble?"
            result1 = test_agent(task1)
            result2 = test_agent(task2)
            print("Question1's Final Answer:\n",result1)
            print("Question2's Final Answer:\n",result2)
            if result1 is None or result2 is None:
                skip_message = f"Can't handle {chemical_material}."
                data.loc[len(data)] = {'entity':str(chemical_material),'IUPACname':str(df['IUPACname'][i]),'solid':'None','soluble':'None','filter':0}
                logging.error(skip_message)  # Log the skip
                continue
            if result1 == "Yes" and result2 == "No":
                filtered_chemical_material.append(chemical_material)
                data.loc[len(data)] = {'entity':str(chemical_material),'IUPACname':str(df['IUPACname'][i]),'solid':str(result1),'soluble':str(result2),'filter':1}
            else:
                data.loc[len(data)] = {'entity':str(chemical_material),'IUPACname':str(df['IUPACname'][i]),'solid':str(result1),'soluble':str(result2),'filter':0}
except Exception as e:
    logging.error(f"An error occurred: {e}. Last processed chemical material was {chemical_material}")
finally:
    save_path = os.path.join(os.getcwd(), 'sample_data', 'sample_final_materials_test.csv')
    data.to_csv(save_path, index=False)
    #data.to_csv(os.getcwd()+'/experiment_data/finish_material_screening.csv', index=False)
