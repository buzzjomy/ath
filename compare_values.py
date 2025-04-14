from jsonpath_rw import jsonpath, parse
import json
from lxml import etree
import logging

logger = logging.getLogger(__name__)


"""
"""
def validate_values_xml_to_cdm(mapping_list, fl_file, cdm_file):
    # for the elements which have firelight tags
    # check and validate the values in CDM
    cdm_json = read_json_file(cdm_file)

    # get dataitem name value dict
    xml_data_dict = get_fl_tag_dataitem_value(fl_file)

    # Find FL tag in mapping
    for mapping in mapping_list:
        for attr1_dict in mapping['attribute1_list']:
            if len(attr1_dict['attribute2_list'])==0 and "FirelightTag" in attr1_dict.keys():
                if attr1_dict["FirelightLogic"]=='nan' and attr1_dict['FirelightTag']!='Added by IA':
                    print(attr1_dict)
                    if attr1_dict['FirelightTag'] in xml_data_dict:
                        print(xml_data_dict[attr1_dict['FirelightTag']])
                        attr1_dict['FirelightValue']=xml_data_dict[attr1_dict['FirelightTag']]
                        validate_value_of_key_from_cdm(mapping['name'], attr1_dict, cdm_json, 
                                                  attr1_dict['FirelightValue'])
                else:
                    #items for which logic to be implemented
                    pass
                pass
            # elif "FirelightTag" in attr1_dict.keys():
            #     print("Error condition where Firelight tag and attribute list is non empty" + str(attr1_dict))
            for attr2_dict in attr1_dict['attribute2_list']:
                if len(attr2_dict['attribute3_list'])==0 and "FirelightTag" in attr2_dict.keys():
                    if attr2_dict["FirelightLogic"]=='nan' and attr2_dict['FirelightTag']!='Added by IA':
                        print(attr2_dict)
                        if attr2_dict['FirelightTag'] in xml_data_dict:
                            print(xml_data_dict[attr2_dict['FirelightTag']])
                            attr2_dict['FirelightValue']=xml_data_dict[attr2_dict['FirelightTag']]
                            validate_value_of_key_from_cdm(mapping['name'], attr2_dict, cdm_json, 
                                                    attr2_dict['FirelightValue'])
                else:
                    #items for which logic to be implemented
                    pass
                # else:
                #     print("Error condition where Firelight tag and attribute list is non empty" + attr2_dict)
                for attr3_dict in attr2_dict['attribute3_list']:
                    if len(attr3_dict['attribute4_list'])==0 and "FirelightTag" in attr3_dict.keys():
                        pass
                    # else:
                    #     print("Error condition where Firelight tag and attribute list is non empty" + attr3_dict)
                    for attr4_dict in attr3_dict['attribute4_list']:
                        if "FirelightTag" not in attr4_dict.keys():
                            pass
                        # else:
                        #     print("Error condition where Firelight tag and attribute list is non empty" + attr4_dict)
    # search for tag value in XML
    # compare the value in CDM json
    pass


def validate_value_of_key_from_cdm(domain, attr_dict, cdm_json, expected_value):
    # book_titles_path = parse('store.book[*].title')
    path = parse(return_json_parser(domain, attr_dict))
    cdm_value = [match.value for match in path.find(cdm_json)]
    if len(cdm_value)==1 and cdm_value[0]==expected_value:
        logger.info(f"PASS Values {str(cdm_value)} returned from \
                    CDM for {attr_dict} are as expected")
    elif len(cdm_value)!=1:
        logger.info(f"FAIL Errorenous values {str(cdm_value)} \
                    returned from CDM for {attr_dict}")
    elif len(cdm_value)==1 and cdm_value[0]!=expected_value:
        logger.info(f"FAIL Values {str(cdm_value)} returned from CDM\
                     for {attr_dict} are NOT as expected {expected_value}")
    input()

def return_json_parser(domain, attr_dict):
    parser_str = domain
    if len(attr_dict['attribute2_list'])==0:
        return'.'.join([parser_str,  attr_dict['attribute1']])
    if len(attr_dict['attribute2_list'])>0:
        if attr_dict['attribute1_type']=='array':
            parser_str = '.'.join([parser_str, attr_dict['attribute1']+"[*]"])
        else:
            parser_str = '.'.join([parser_str, attr_dict['attribute1']])
    if len(attr_dict['attribute3_list'])==0:
        return'.'.join([parser_str,  attr_dict['attribute2']])
    if len(attr_dict['attribute3_list'])>0:
        if attr_dict['attribute2_type']=='array':
            parser_str = '.'.join([parser_str, attr_dict['attribute2']+"[*]"])
        else:
            parser_str = '.'.join([parser_str, attr_dict['attribute2']])
    if len(attr_dict['attribute4_list'])==0:
        return'.'.join([parser_str,  attr_dict['attribute3']])
    if len(attr_dict['attribute4_list'])>0:
        if attr_dict['attribute3_type']=='array':
            parser_str = '.'.join([parser_str, attr_dict['attribute3']+"[*]"])
        else:
            parser_str = '.'.join([parser_str, attr_dict['attribute3']])
    
def get_fl_tag_dataitem_value(fl_file):
    tree = etree.parse(fl_file)
    root = tree.getroot()
    xml_data_dict = {}
    for i in root.findall('DataItems')[0].findall('DataItem'):
        if len(i.findall('Name'))==1:
            if len(i.findall('Value'))==1:
                xml_data_dict[i.findall('Name')[0].text] = i.findall('Value')[0].text
        else:
            print('value missing for a dataitem, please review FL xml')
    return xml_data_dict

"""
Compares xml to cdm
"""
def validate_nulls_in_cdm(mapping_list, cdm_file):
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

"""
If no Firelight tags are available, then the element in CDM should have null value
We are validating it in this below method
"""
def validate_no_fl_tag_items_in_mapping_is_null_in_cdm(item_info, cdm_file):
    cdm_json = read_json_file(cdm_file)
    ret_val = check_inner_key(cdm_json, item_info)
    # input(type(ret_val))
    if isinstance(ret_val, list):
        for i in ret_val:
            if i is not None:
                logger.info(f'FAIL {item_info} found in CDM but value is non null')
                # input()
            else:
                logger.info(f'PASS {item_info} found in CDM and value is null')
    elif ret_val==False:
        logger.info(f'FAIL {item_info} not found in CDM')
        # input()
    elif ret_val is not None:
        logger.info(f'FAIL {item_info} found in CDM but value is non null')
        # input()
    elif ret_val is None:
        logger.info(f'PASS {item_info} found in CDM and value is null')
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