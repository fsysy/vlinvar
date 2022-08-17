import xml.etree.ElementTree as et
import gzip

file_name = "data/ClinVarFullRelease_00-latest.xml.gz"

file_data = et.iterparse(gzip.GzipFile(file_name), events = ('end', 'start'))
print(file_data)
for event, element in file_data:
    print(element.text)
    print(element.tag)
    

