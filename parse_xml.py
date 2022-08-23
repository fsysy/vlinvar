#-*- encoding: utf-8 -*-
import xml.etree.ElementTree as et
import gzip
import pandas as pd

file_name = "data/ClinVarFullRelease_00-latest.xml.gz"

file_data = et.iterparse(gzip.GzipFile(file_name), events = ('end', 'start'))

initial = True
current_ClinVarSet = ""
dfs = {}
df = {}

def get_max_index(df):
    if len(df.keys()) == 0 :
        return 0
    max_index = max([len(df[a]) for a in df.keys()])
    return max_index

def new_input(df, current_tag):
    max_index= get_max_index(df)
    if current_tag not in df.keys():
        df[current_tag] = []



def set_tag(prev_tag, element_tag, elem_tag):
    tags = [element_tag, elem_tag]
    if prev_tag != "":
        tags = [prev_tag]+tags
    return "_".join(tags)
            
def etree_auto_input(df, element, prev_tag, avoid_target = []):
    for elem in element.iter():
        if elem.tag in avoid_target:
            continue
        if prev_tag != "":
            current_tag = prev_tag + "_" + elem.tag
        else:
            current_tag = elem.tag
        
        
        #input text
        text_element = (elem.text != None) and (type(elem.text)==str) and (elem.text.strip()!="")
        #print("*", elem.tag, text_element, elem.text)
        if text_element:
            new_input(df, current_tag)
            df[current_tag].append(elem.text)
        
        #input attrib
        for attrib_key in elem.attrib.keys():
            added_tag = set_tag(prev_tag, elem.tag, attrib_key)
            new_input(df, added_tag)
            df[added_tag].append(elem.attrib[attrib_key])
    return df
               
            

counter = 0
total_keys = []

operating_option = 1 #clinvarassertion 정리
#operating_option = 2 #clinvarset 정리
print(f"operating option: {operating_option}")
if operating_option == 1:
    print("start")
    for event, element in file_data:
        if element.tag != "ClinVarAssertion":
            continue
        else:
            prev_tag = ""
            df = etree_auto_input(df, element, prev_tag)
        for key_item in df.keys():
            if key_item not in dfs:
                dfs[key_item] = [""]*(get_max_index(dfs)-1)
            dfs[key_item].append("||".join(df[key_item]))
        
        max_index = get_max_index(dfs)
        for key_item in dfs.keys():
            if len(dfs[key_item]) < max_index:
                dfs[key_item].append("")
        df = {}
        counter += 1
        
    for key_name in dfs.keys():
        print(key_name, len(dfs[key_name]))
    pd_df = pd.DataFrame(data = dfs)
    pd_df = pd_df.drop_duplicates()
    pd_df.to_csv("clinvar_sub.csv", index = False)

         
if operating_option == 2:
    avoid_target = ["ClinVarAssertion"]
    for event, element in file_data:
        if element.tag != "ClinVarSet":
            continue
        else:
            prev_tag = ""
            df = etree_auto_input(df, element, prev_tag, avoid_target=avoid_target)
            
        for key_item in df.keys():
            if key_item not in dfs:
                dfs[key_item] = [""]*(get_max_index(dfs)-1)
            dfs[key_item].append("||".join(df[key_item]))
        max_index = get_max_index(dfs)
        for key_item in dfs.keys():
            if len(dfs[key_item]) < max_index:
                dfs[key_item].append("")
        df = {}
        counter += 1
        if counter % 10 == 1:
            print(f"Item number : {counter}")
        
    for key_name in dfs.keys():
        print(key_name, len(dfs[key_name]))
    pd_df = pd.DataFrame(data = dfs)
    pd_df = pd_df.drop_duplicates()
    pd_df.to_csv("clinvar_set.csv", index = False)
    
"""
for event, element in file_data:
    if element.tag == "ClinVarSet":
        info_collecting["ClinVarSet"] = element.attrib
        if counter == 0:
            counter += 1
        else:
            print(info_collecting)
            info_collecting = {}
            counter += 1
            if counter > 1000:
                break
    else:
        if element.tag in target_lib.keys():
            if target_lib[element.tag]["text"]:
                info_collecting[element.tag] = element.text
            if target_lib[element.tag]["attrib"] != []:
                for attrib_name in target_lib[element.tag]["attrib"]:
                    attrib_name = element.tag + "_" + attrib_name
                    info_collecting["attrib_name"] = element.attrib
"""
