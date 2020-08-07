from docx import Document
import csv
import pandas
import json


def readCsvColumns(filename):
    with open('JDD/epkfdcpt.s5_0000121296_20200622_140027', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ';')
        header = next(reader, None)
    header

# Returns header for csv document
def readCsvColumnsPanda(filename):
    data = pandas.read_csv(f'JDD/copy/{filename}', delimiter=";")
    return data.columns

def matchingElements(listA, listB):
    return set(listA).intersection(listB)

def nonMatchingElements(listA, listB):
    return list(set(listA) - set(listB))


def generateHeaderJson(filename):
    data = {
        "$schema": "http://json-schema.org/schema#",
	    "self": {
		"vendor": "laposte.fr",
		"name": filename,
		"format": "jsonschema"
	    },
	    "$metadata": {
            "$datasource": "??",
            "$dataset": "??",
            "$fileFormat": "CSV",
            "$nameFormat": f"{filename}.*\\.csv\\.bz2",
            "$separator": "|",
            "$quote": "\"",
            "$escape": "\\",
            "$ingestionMode": "APPEND",
            "$dataVector": "FILE",
            "$dateFormat": "yyyy-MM-dd",
            "$dateTimeFormat": "MM-dd-yyyy HH:mm:ss"
	    },
        "id": f"json_{filename}.json",
        "title": "Open Hub",
        "description": "??",
        "type": "object",
        "properties": {}
    }
    return data

# Generates a Json from the word table
def generateJson(word_table, filename):
    data = generateHeaderJson(filename)
    fieldsJson = {}

    for item in word_table:
        fieldsJson[item['FIELDNAME']] =  {
                "description": item['LIBELLE'],
                "type": item['TYPE']
            }
    data['properties'] = fieldsJson
    return data

# Dumps the Json generated into a file
def writeJson(filename, word_table):
    data = generateJson(word_table, filename)
    with open(f'generatedJson/json_{filename}.json', 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, ensure_ascii=False, indent=4)


# Function to parse word table 
### TODO : check for badly formatted tables 
def readWordTable(document):
    document = Document(document)
    table = document.tables[0]

    data = []

    keys = None
    for i, row in enumerate(table.rows):
        text = (cell.text for cell in row.cells)

        # Establish the mapping based on the first row
        # headers; these will become the keys of our dictionary
        if i == 0:
            keys = tuple(text)
            continue

        # Construct a dictionary for this row, mapping
        # keys to values for this row
        row_data = dict(zip(keys, text))
        data.append(row_data)

    return data
    

# Loops on the word table dictionary returns a list of all the field names
# Useful for the analysisJddSpec function
def getFieldNameList(word_table):
    # Loop on list and access fieldname
    labelList = []
    for label in word_table:
        labelList.append(label['FIELDNAME'])

    return labelList


# Function to assert differences between JDD and Spec
def analysisJddSpec(word_tables_list):
    for doc_file in word_tables_list:
    
        wordTableFields = getFieldNameList(readWordTable(f"Spec/wordTable{doc_file}.docx"))
        headerJdd = readCsvColumnsPanda(f"{doc_file}")

        print("length spec: ", len(wordTableFields))
        print("length jdd: ", len(headerJdd))

        comparisonSet = matchingElements(wordTableFields, headerJdd)
        print("matching elements : ", len(comparisonSet))
        print("Elements in spec but not in JDD : ", nonMatchingElements(wordTableFields, headerJdd))
        print("Elements in JDD but not in Spec : ", nonMatchingElements(headerJdd, wordTableFields))


if __name__ == "__main__":
    word_tables_list = ['epkfdach', 'epkfdcpt', 'epkfdfac','epkfpppf', 'epkfttpd', 'epkfttva']

    for filename in word_tables_list:
        print("Reading word document ...")
        word_table = readWordTable(f"Spec/wordTable{filename}.docx")
        print("Done, generating JSON")
        writeJson(filename, word_table)
        print("Done !")

    