import mapping
from compare_values import validate_values_xml_to_cdm
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(filename='result.log', level=logging.INFO)
cdm = r"C:\Users\E406692\Downloads\Athene\Athene\ea350232-fec5-4d33-8c5b-c5fdd0b366t1.json"
fl_xml = r"C:\Users\E406692\Downloads\Athene\Athene\ea350232-fec5-4d33-8c5b-c5fdd0b366t1.xml"
mapping_list = mapping.readMappingExcel\
    (r"C:\Users\E406692\Downloads\CDM V6.xlsx",
                         ["annuitant", "transaction"])

# compare.validate_nulls_in_cdm(mapping_list,cdm                         )

validate_values_xml_to_cdm(mapping_list,fl_xml, cdm)