from docx import Document
import csv
import pandas


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


    # Loop on list and access fieldname
    labelList = []
    for label in data:
        labelList.append(label['FIELDNAME'])

    return labelList


if __name__ == "__main__":
    word_tables_list = ['epkfdach', 'epkfdcpt', 'epkfdfac','epkfpppf', 'epkfttpd', 'epkfttva']

    for doc_file in word_tables_list:
        wordTableFields = readWordTable(f"Spec/wordTable{doc_file}.docx")
        headerJdd = readCsvColumnsPanda(f"{doc_file}")

        print("length spec: ", len(wordTableFields))
        print("length jdd: ", len(headerJdd))

        comparisonSet = matchingElements(wordTableFields, headerJdd)
        print("matching elements : ", len(comparisonSet))
        print("Elements in spec but not in JDD : ", nonMatchingElements(wordTableFields, headerJdd))
        print("Elements in JDD but not in Spec : ", nonMatchingElements(headerJdd, wordTableFields))