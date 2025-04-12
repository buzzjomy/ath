import json
from lxml import etree

def compareXmlToCDM(mapping_list, cdm_file):
    for mapping in mapping_list:
        # In the mapping document 
        # check where is there is no firelight tag, the value in CDM should be null
        for attr1_dict in mapping['attribute1_list']:
            # input(attr1_dict)
            if len(attr1_dict['attribute2_list'])==0 and "FirelightTag" not in attr1_dict.keys():
                item_path = f"{mapping['name']}.{attr1_dict['attribute1']}"
                validate_no_fl_tag_items_in_mapping_is_null_in_cdm(item_path, cdm_file)
                pass
            # check attr1_dict['attribute1'] is available in CDM with null value
            for attr2_dict in attr1_dict['attribute2_list']:
                if len(attr2_dict['attribute3_list'])==0 and "FirelightTag" not in attr2_dict.keys():
                    item_path = f"{mapping['name']}.{attr1_dict['attribute1']}^^{attr1_dict['attribute1_type']}\
                    .{attr2_dict['attribute2']}"
                    validate_no_fl_tag_items_in_mapping_is_null_in_cdm(item_path, cdm_file)
                pass
                for attr3_dict in attr2_dict['attribute3_list']:
                    if len(attr3_dict['attribute4_list'])==0 and "FirelightTag" not in attr3_dict.keys():
                        item_path = f"{mapping['name']}.{attr1_dict['attribute1']}^^{attr1_dict['attribute1_type']}\
                        .{attr2_dict['attribute2']}^^{attr2_dict['attribute2_type']}\
                            .{attr3_dict['attribute3']}"
                        validate_no_fl_tag_items_in_mapping_is_null_in_cdm(item_path, cdm_file)
                    pass
                    for attr4_dict in attr3_dict['attribute4_list']:
                        if "FirelightTag" not in attr4_dict.keys():
                            item_path = f"{mapping['name']}.{attr1_dict['attribute1']}^^{attr1_dict['attribute1_type']}\
                            .{attr2_dict['attribute2']}^^{attr2_dict['attribute2_type']}\
                            .{attr3_dict['attribute3']}^^{attr3_dict['attribute3_type']}\
                            .{attr4_dict['attribute4']}"
                            validate_no_fl_tag_items_in_mapping_is_null_in_cdm(item_path, cdm_file)
                        pass
        # look for firelight tags and verify if values are there in CDM
        pass


def check_inner_key(data, key_path):
    """
    Checks if an inner key exists in a nested dictionary.

    Args:
        data (dict): The dictionary to search within.
        key_path (str): A string representing the path to the key, 
                         with keys separated by dots (e.g., "level1.level2.target_key").

    Returns:
        bool: True if the key exists, False otherwise.
    """
    keys = key_path.split('.')
    current = data
    key_type = ''
    #########
    for key in keys:
        if len(keys)==2:
            key = key.strip()
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                print('Keys not found')
                input(key_path)
                return False
        elif len(keys)==3:
            if keys.index(key)==2 and key_type=='array': # last index, 3rd position
                out_list = []
                for i in current:
                    if key.strip() in i:
                        out_list.append(i[key.strip()])          
                    else:
                        print('++Keys not found')
                        input(key_path)
                        return False
                return out_list
            else:
                key = key.strip()
                if '^^array' in key:
                    key_type = key.split('^^')[1]
                    key = key.replace('^^array', '')
                    if isinstance(current, dict) and key in current:
                        current = current[key]
                    pass
                else:
                    if '^^' in key:
                        key = key.split('^^')[0]
                    if isinstance(current, dict) and key in current:
                        current = current[key]
                    else:
                        print('--Keys not found')
                        input(key_path)
                        return False
            pass
    #########
    # for key in keys:
    #     key = key.strip()
    #     if '_array' in key:
    #         key = key.replace('_array', '')
    #         if isinstance(current[key], list):
    #             for item in current[key]:
    #                 if isinstance(item, dict) and key in item:
    #                     current = current[key]
    #                 else:
    #                     print('Not found keys')
    #                     input(key_path)
    #                     return False
    #         pass
    #     if isinstance(current, dict) and key in current:
    #         current = current[key]
    #     else:
    #         print('Not found keys')
    #         input(key_path)
    #         return False
    print('found keys')
    print(current)
    return current

# Reading JSON from a file
def read_json_file(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

def validate_no_fl_tag_items_in_mapping_is_null_in_cdm(item_path, cdm_file):
    cdm_json = read_json_file(cdm_file)
    ret_val = check_inner_key(cdm_json, item_path)
    # input(type(ret_val))
    if isinstance(ret_val, list):
        for i in ret_val:
            if i is not None:
                print(f'FAIL {item_path} found in CDM but value is non null')
                input()
            else:
                print(f'PASS {item_path} found in CDM and value is null')
    elif ret_val==False:
        print(f'FAIL {item_path} not found in CDM')
        input()
    elif ret_val is not None:
        print(f'FAIL {item_path} found in CDM but value is non null')
        input()
    elif ret_val is None:
        print(f'PASS {item_path} found in CDM and value is null')
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