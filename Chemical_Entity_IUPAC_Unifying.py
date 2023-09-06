import os

import numpy as np
import pandas as pd
import pubchempy as pcp

data_path = os.path.join(os.getcwd(), 'sample_data', 'sample_Scopus_data_result.csv')
data = pd.read_csv(data_path)
#data = pd.read_csv(os.getcwd()+'\experiment_data\SimpleChemical_stanza_result.csv')

data['IUPACname'] = ''
data['cid'] = 0

for i in range(0,len(data)):
    compound_entity= data['entity'][i]    
    compounds = pcp.get_compounds(compound_entity, 'name')
    if compounds:
        data['IUPACname'][i] = compounds[0].iupac_name
        data['cid'][i] = compounds[0].cid
    else:
        data['IUPACname'][i] = 'None'
data = data[data['IUPACname'] != 'None']

data['count'] = data['count'].astype(int)
grouped_df = data.groupby('cid').agg({'entity': ', '.join, 'count': 'sum', 'IUPACname': 'first'}).reset_index()
data = grouped_df.sort_values('count', ascending=False)
data = data.reindex(columns=['entity', 'count', 'IUPACname', 'cid'])
save_path = os.path.join(os.getcwd(), 'sample_data', 'sample_entity_to_IUPAC.csv')
data.to_csv(save_path, index=False)
#data.to_csv(os.getcwd()+'\experiment_result\SimpleChemical_stanza_result_Iupacname.csv',index=False)
