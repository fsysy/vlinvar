#-*- encoding: utf-8 -*-
import xml.etree.ElementTree as et
import gzip
import pandas as pd

class ClinvarSet:
    def __init__(self, element):
        self.element = element
        self.clinvarset_id = self.element.attrib.get("ID")
        self.status = "None"
        self.title = "None"
        self.datecreated = "None"
        self.datelastupdated = "None"
        self.refclinvar_id = "None"
        self.clinvaraccession_acc = "None"
        self.clinvaraccession_version = "None"
        self.clinvaraccession_dateupdated = "None"
        self.clinvarrecordstatus = "None"
        self.clinvarsig_datelastevaluated = "None"
        self.clinvarsig_reviewstatus = "None"
        self.clinvarsig_description = "None"
        self.measureset_id = "None"
        self.measureset_acc = "None"
        self.measureset_verion = "None"
        self.measureset_preferred = ""
        self.measureset_alternate = ""
        self.clinvar_assert_id = ""

    def print_all(self):
        print("clinvarset_id: ",self.clinvarset_id)
        print("status: ", self.status)
        print("title: ", self.title)
        print("datecreated: ", self.datecreated)
        print("datelastupdated: ", self.datelastupdated)
        print("refclinvar_id: ", self.refclinvar_id)
        print("clinvaraccession_acc: ", self.clinvaraccession_acc)
        print("clinvaraccession_version: ", self.clinvaraccession_version)
        print("clinvaraccession_dateupdated: ", self.clinvaraccession_dateupdated)
        print("clinvarrecordstatus: ", self.clinvarrecordstatus)
        print("clinvarsig_datelastevaluated: ", self.clinvarsig_datelastevaluated)
        print("clinvarsig_reviewstatus: ", self.clinvarsig_reviewstatus)
        print("clinvarsig_description: ", self.clinvarsig_description)
        print("measureset_id: ", self.measureset_id)
        print("measureset_acc: ", self.measureset_acc)
        print("measureset_verion: ", self.measureset_verion)
        print("measureset_preferred: ", self.measureset_preferred)
        print("measureset_alternate: ", self.measureset_alternate)
        print("clinvar_assert_id: ", self.clinvar_assert_id)
        print()
        
    
    def check_element(self, element, tag_name):
        elem = element.findall(tag_name)
        if len(elem) == 1:
            return elem[0]
        else:
            return False
            
    def set_status(self):
        status = self.check_element(self.element, "RecordStatus")
        self.status = "None" if status == False else status.text
        
    def set_title(self):
        title = self.check_element(self.element, "Title")
        self.title = "None" if title == False else title.text
    
    def set_datecreated(self, ref_clinvar_assert):
        self.datecreated = ref_clinvar_assert.attrib.get("DateCreated")
        self.datelastupdated = ref_clinvar_assert.attrib.get("DateLastUpdated")
        self.refclinvar_id = ref_clinvar_assert.attrib.get("ID")
    
    def set_clinvaracc(self, clinvar_acc):
        self.clinvaraccession_acc = clinvar_acc.attrib.get("Acc")
        self.clinvaraccession_version = clinvar_acc.attrib.get("Version")
        self.clinvaraccession_dateupdated = clinvar_acc.attrib.get("DateUpdated")
    
    def set_clinvarrecordstatus(self, ref_clinvar_assert):
        clinvarrecordstatus = self.check_element(ref_clinvar_assert, "RecordStatus")
        self.clinvarrecordstatus = "None" if clinvarrecordstatus == False else clinvarrecordstatus.text
    
    def set_clinicalsignificance(self, ref_clinvar_assert):
        clin_sig = ref_clinvar_assert.findall("ClinicalSignificance")
        if len(clin_sig) == 1:
            clin_sig = clin_sig[0]
            self.clinvarsig_datelastevaluated = clin_sig.attrib.get("DateLastEvaluated")
            clinvarsig_reviewstatus = self.check_element(clin_sig, "ReviewStatus")
            self.clinvarsig_reviewstatus = "None" if clinvarsig_reviewstatus == False else clinvarsig_reviewstatus.text
            clinvarsig_description = self.check_element(clin_sig, "Description")
            self.clinvarsig_description = "None" if clinvarsig_description == False else clinvarsig_description.text

    def set_measureset(self, measureset):
        self.measureset_id = measureset.attrib.get("ID")
        self.measureset_acc = measureset.attrib.get("Acc")
        self.measureset_version = measureset.attrib.get("Version")
        measureset_values = measureset.findall("./Measure/Name/ElementValue")
        for measureset_value in measureset_values:
            if measureset_value.attrib.get("Type") == "Preferred":
                ms_value = measureset_value.text if measureset_value.text != None else ""
                self.measureset_preferred += (ms_value + ";")
            if measureset_value.attrib.get("Type") == "Alternate":
                ms_value = measureset_value.text if measureset_value.text != None else ""
                self.measureset_alternate += (ms_value + ";")
            

class Parse_XML:
    def __init__(self, xml_url):
		    self.xml_url = xml_url
		    self.file_data = et.iterparse(gzip.GzipFile(self.xml_url), events = ('end', 'start'))
	
    def run(self):
        counter = 0
        for event, element in self.file_data:
		        print(element.tag, element.text)
		        counter += 1
		        if counter > 10:
		            break
    
    def clinvarset_organize(self):
        counter = 0
        for event, element in self.file_data:
            if element.tag == "ClinVarSet" and event == "end":
                clinvar_set = ClinvarSet(element)
                clinvar_set.set_status()
                clinvar_set.set_title()
                ref_clinvar_assert = element.findall("ReferenceClinVarAssertion")
                if len(ref_clinvar_assert) == 1:
                    ref_clinvar_assert = ref_clinvar_assert[0]
                    clinvar_set.set_datecreated(ref_clinvar_assert)
                    clinvar_acc = ref_clinvar_assert.findall("ClinVarAccession")
                    if len(clinvar_acc) == 1:
                        clinvar_set.set_clinvaracc(clinvar_acc[0])
                    
                    clinvar_set.set_clinvarrecordstatus(ref_clinvar_assert)
                    clinvar_set.set_clinicalsignificance(ref_clinvar_assert)
                    measureset = ref_clinvar_assert.findall("MeasureSet")
					
                    if len(measureset) == 1:
                        clinvar_set.set_measureset(measureset[0])
                clinvar_asserts = element.findall("ClinVarAssertion")
                clinvar_assert_string = []
                for clinvar_assert in clinvar_asserts:
                    clinvar_assert_id = clinvar_assert.attrib.get("ID")
                    clinvar_assert_string.append(clinvar_assert_id)
                clinvar_assert_string = ",".join(clinvar_assert_string)
                clinvar_set.clinvar_assert_id = clinvar_assert_string
                clinvar_set.print_all()
                counter += 1
            else:
                continue
            #if counter > 100:
            #    break
  
	

if __name__ == "__main__":
    parse_xml = Parse_XML("data/ClinVarFullRelease_00-latest.xml.gz")
    #parse_xml.run()
    parse_xml.clinvarset_organize()
