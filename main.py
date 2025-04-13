import mapping
import compare


mapping_list = mapping.readMappingExcel\
    (r"C:\Users\E406692\Downloads\CDM V6.xlsx",
                         ["annuitant", "transaction"])

compare.compareXmlToCDM(mapping_list,
                        r"C:\Users\E406692\Downloads\Athene\Athene\ea350232-fec5-4d33-8c5b-c5fdd0b366t1.json")