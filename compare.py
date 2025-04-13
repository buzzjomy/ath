import json
from lxml import etree

def compareXmlToCDM(mapping_list, cdm_file):
    for mapping in mapping_list:
        # In the mapping document 
        # check where is there is no firelight tag, the value in CDM should be null
        for attr1_dict in mapping['attribute1_list']:
            # input(attr1_dict)
            if len(attr1_dict['attribute2_list'])==0 and "FirelightTag" not in attr1_dict.keys():
                item_info = {'domain': mapping['name'], 
                             'attributes': [
                                             {
                                                 'name': attr1_dict['attribute1'],
                                                 'type':attr1_dict['attribute1_type']
                                             }
                                             ]
                                             }
                validate_no_fl_tag_items_in_mapping_is_null_in_cdm(item_info, cdm_file)
                pass
            # check attr1_dict['attribute1'] is available in CDM with null value
            for attr2_dict in attr1_dict['attribute2_list']:
                if len(attr2_dict['attribute3_list'])==0 and "FirelightTag" not in attr2_dict.keys():
                    item_info = {'domain': mapping['name'],
                                 'attributes': [
                                             {
                                                 'name': attr1_dict['attribute1'],
                                                 'type':attr1_dict['attribute1_type']
                                             },
                                              {
                                                 'name': attr2_dict['attribute2'],
                                                 'type':attr2_dict['attribute2_type']
                                             }
                                             ]
                                             }
                    validate_no_fl_tag_items_in_mapping_is_null_in_cdm(item_info, cdm_file)
                pass
                for attr3_dict in attr2_dict['attribute3_list']:
                    if len(attr3_dict['attribute4_list'])==0 and "FirelightTag" not in attr3_dict.keys():
                        item_info = {'domain': mapping['name'],
                                         'attributes': [
                                             {
                                                 'name': attr1_dict['attribute1'],
                                                 'type':attr1_dict['attribute1_type']
                                             },
                                              {
                                                 'name': attr2_dict['attribute2'],
                                                 'type':attr2_dict['attribute2_type']
                                             },
                                              {
                                                 'name': attr3_dict['attribute3'],
                                                 'type':attr3_dict['attribute3_type']
                                             }]}
                        validate_no_fl_tag_items_in_mapping_is_null_in_cdm(item_info, cdm_file)
                    pass
                    for attr4_dict in attr3_dict['attribute4_list']:
                        if "FirelightTag" not in attr4_dict.keys():
                            item_info = {'domain': mapping['name'],
                                         'attributes': [
                                             {
                                                 'name': attr1_dict['attribute1'],
                                                 'type':attr1_dict['attribute1_type']
                                             },
                                              {
                                                 'name': attr2_dict['attribute2'],
                                                 'type':attr2_dict['attribute2_type']
                                             },
                                              {
                                                 'name': attr3_dict['attribute3'],
                                                 'type':attr3_dict['attribute3_type']
                                             },
                                              {
                                                 'name': attr4_dict['attribute4'],
                                                 'type':attr4_dict['attribute4_type']
                                             }
                                         ]
                                }
                            validate_no_fl_tag_items_in_mapping_is_null_in_cdm(item_info, cdm_file)
                        pass
        # look for firelight tags and verify if values are there in CDM
        pass

def containsArray(item_info):
    print(item_info)
    for i in item_info['attributes']:
        print(i['type'])
        if i['type']=='array':
            return True
    return False

def check_inner_key(data, item_info):
    current = data
    first_array_found = False
    cdm_item_list = [] 
    partial_path = ''
    if containsArray(item_info):
        key = item_info['domain']
        current = current[key]
        for i in item_info['attributes']:
            if i['type']=='array':
                cdm_item_list.append(current[i['name']])
                first_array_found = True
                pass
            else:
                if first_array_found==False:
                    current = current[i['name']]
                else:
                    cdm_item_list.append(i['name'])
                    pass
        # input(cdm_item_list)
        # the last item would be the key to look for in the array 
        # which would be inturn the second last item
        [last_array, key_list] = find_last_array_and_key(cdm_item_list)
        last_item = cdm_item_list[-1]
        val = None
        for i in last_array:
            if get_value_from_key_list(i, key_list)!=None:
                val = i[last_item]
                print(f"{item_info['attributes']} found as not None, value is {val}")
                return val
        print(f"{item_info['attributes']} found as None")
        return val
    else:
        key_list = [item_info['domain']]+[i['name'] for i in item_info['attributes']]
        # input(key_list)
        for key in key_list:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                print('--Keys not found')
                print(key_list)
                return False
        # input(current)
        return current

def get_value_from_key_list(last_array_item, key_list):
    value = ''
    # print("#############")
    # print(key_list)
    # input(last_array_item)
    for i in key_list[::-1]:
        value = last_array_item[i]
        last_array_item = value
    return value

def find_last_array_and_key(cdm_item_list):
    last_array = []
    key_list = []
    for i in reversed(cdm_item_list):
        if isinstance(i, list):
            last_array = i
            break            
        elif isinstance(i, str):
            key_list.append(i)
    return [last_array, key_list]
    

# Reading JSON from a file
def read_json_file(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

def validate_no_fl_tag_items_in_mapping_is_null_in_cdm(item_info, cdm_file):
    cdm_json = read_json_file(cdm_file)
    ret_val = check_inner_key(cdm_json, item_info)
    # input(type(ret_val))
    if isinstance(ret_val, list):
        for i in ret_val:
            if i is not None:
                print(f'FAIL {item_info} found in CDM but value is non null')
                # input()
            else:
                print(f'PASS {item_info} found in CDM and value is null')
    elif ret_val==False:
        print(f'FAIL {item_info} not found in CDM')
        # input()
    elif ret_val is not None:
        print(f'FAIL {item_info} found in CDM but value is non null')
        # input()
    elif ret_val is None:
        print(f'PASS {item_info} found in CDM and value is null')
    # input()

def print_tags_for_xpath():
    tree = etree.parse(r'C:\Users\E406692\Downloads\Athene\Athene\ea350232-fec5-4d33-8c5b-c5fdd0b366t1.xml')
    root = tree.getroot()

    elems = root.xpath("//DataItem//Name[text()='16257IrrevocableBeneficiary_SignatureDate']")
    for e in elems:
        print(e.text)
        if None!=e.getnext():
            print(e.getnext().text) 

        # .xpath("sibling::*")