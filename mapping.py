import pandas as pd
 

def readMappingExcel(filename, consider_list):
    # Read an Excel file into a DataFrame
    df = pd.read_excel(filename, 
                    sheet_name="Sheet1", header=0, 
                    usecols=["domain", "attribute1", "attribute1 data type", 
                        "attribute2", "attribute2 data type",
                        "attribute3", "attribute3 data type",
                        "attribute4", "attribute4 data type",
                        "Firelight Tag", "Firelight Logic"]) 

    df = df.fillna("nan")
    mapping_list = []
    mapping = {} 
    consider = False
    existing_domains = []
    # Print the DataFrame
    # print(df)
    for index, row in df.iterrows():  
        # print(row['domain']) 
        # print(f"Index: {index}")     
        if row['domain'] in consider_list:
            print(row['domain']) 
            consider = True
        elif row['domain'] not in consider_list and row['domain']!='nan':
            consider = False
            if 'name'in mapping:
                for m in mapping_list:
                    # input(m)
                    existing_domains.append(m['name'])
                if len(mapping.keys())>0:
                    # input(mapping)
                    if mapping['name'] not in existing_domains:
                        mapping_list.append(mapping)
        if consider == True:
            if row['domain']!="nan":
                # clear all the vars
                dict_to_update_firelight = {}
                
                mapping= {'name' : row['domain'], 'attribute1_list': []}
            if row['attribute1']!="nan":
                dict_to_update_firelight = {"attribute1": row['attribute1'], 
                "attribute1_type": row['attribute1 data type'],
                "attribute2_list":[]}
                mapping['attribute1_list'].append(dict_to_update_firelight)
                # input('attr1: ' + str(mapping)        )
            if row['attribute2']!="nan":
                dict_to_update_firelight = {"attribute2": row['attribute2'],
                "attribute2_type": row['attribute2 data type'],
                "attribute3_list":[]}
                # get the last item in the attr list
                attr2_list = mapping['attribute1_list'][-1]['attribute2_list']
                attr2_list.append(dict_to_update_firelight)
                # input('attr2: ' + str(mapping)        )
            if row['attribute3']!="nan":
                # print('----------------------------')
                # print(row['attribute3'])
                dict_to_update_firelight = {"attribute3": row['attribute3'],
                "attribute3_type": row['attribute3 data type'],
                "attribute4_list":[]}
                # print('----------------------------')
                # print(dict_to_update_firelight)
                # print('----------------------------')
                # print(mapping['attribute1_list'][-1])
                # print('----------------------------')
                # print(mapping
                # ['attribute1_list'][-1]['attribute2_list'][-1])
                # print('----------------------------')
                # print(type(mapping
                # ['attribute1_list'][-1]['attribute2_list'][-1]['attribute3_list']))

                # get the last item in the attr list
                attr3_list = mapping['attribute1_list'][-1]\
                    ['attribute2_list'][-1]['attribute3_list']
                attr3_list.append(dict_to_update_firelight)
                # input('attr3: '  + str(mapping)        )  
            if row['attribute4']!="nan":
                dict_to_update_firelight = {"attribute4": row['attribute4'],
                "attribute4_type": row['attribute4 data type']}
                # attribute4 = row['attribute4']    
                attr4_list = mapping
                ['attribute1_list'][-1]['attribute2_list'][-1]['attribute3_list']\
                [-1]['attribute4_list']
                attr4_list.append(dict_to_update_firelight)   
                # input('attr4: '  + str(mapping)        )    
            if row['Firelight Tag']!="nan" or row['Firelight Logic']!="nan":
                dict_to_update_firelight['FirelightTag'] = row['Firelight Tag']
                dict_to_update_firelight['FirelightLogic'] = row['Firelight Logic']
                # input('firelight: '  + str(mapping)        )
                # input(mapping)
    print(mapping_list)
    return mapping_list