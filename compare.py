from lxml import etree

def compareXmlToCDM(mapping):
    for mapping in mapping:
        # check where is there is no firelight tag, the value in CDM should be null

        # look for firelight tags and verify if values are there in CDM
        pass


def validate_no_fl_tag_values_in_cdm(mapping):
    no_fl_cmd_attributes = []
    for attribute1 in mapping['attribute1_list']:
        if 'FirelightTag' in attribute1.keys():
            # get the value from xml

            # call method to verify attribute value in CDM
            pass



def print_tags_for_xpath():
    tree = etree.parse(r'C:\Users\E406692\Downloads\Athene\Athene\ea350232-fec5-4d33-8c5b-c5fdd0b366t1.xml')
    root = tree.getroot()

    elems = root.xpath("//DataItem//Name[text()='16257IrrevocableBeneficiary_SignatureDate']")
    for e in elems:
        print(e.text)
        if None!=e.getnext():
            print(e.getnext().text) 

        # .xpath("sibling::*")