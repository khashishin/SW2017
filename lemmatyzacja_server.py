import csv
import sys
basic_form_dict = dict()

def open_file(filename):
        f = open(filename, 'r', encoding="utf8") # opens the csv file
        row_list = f.readlines()
        f.close()      # closing
        return row_list

strip_signs_list = [',', '.', '\r', '\n', '-', '"', "'"]
def delete_unallowed_signs(text):
    for ch in strip_signs_list:
        if ch in text:
            text = text.replace(ch, "")
    return text


def prepare_lematization():
    lemmat_filename = 'lemmatization-pl.txt'
    additional_mapping = open_file("sgjp-20170115.tab")
    lematted_rows = open_file(lemmat_filename)

    for row in additional_mapping:
        #The sgjp mapping is as follows
        # aldozie	aldoza	subst:sg:loc:f	nazwa pospolita	chem.
        row = row.lower().split()
        basic_form = row[1].split(":")[0] #sPlit the verb:v1 verb:v2
        grammatical_form = row[0]
        basic_form_dict[grammatical_form] = basic_form

    for row in lematted_rows:
        row = row.lower().split()
        basic_form = row[0]
        grammatical_form = row[1]
        basic_form_dict[grammatical_form] = basic_form

    with open('full_mapping.csv', 'w') as csvfile:
        mapping_writer = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for key,value in basic_form_dict.items():
            try:
                mapping_writer.writerow([key, value])
            except UnicodeEncodeError:
                #Really weird words with weird letters lol
                #print (key,value)
                continue

def read_mapping():
    with open('full_mapping.csv', 'r') as mapping_file:
        lemmat_reader = csv.reader(mapping_file, delimiter=' ')
        for row in lemmat_reader:
            if row != []:
                row = [i.lower() for i in row]
                basic_form = row[1].split(":")[0] #sPlit the verb:v1 verb:v2
                grammatical_form = row[0]
                basic_form_dict[grammatical_form] = basic_form
    print("zakonczono mapowanie")

read_mapping()

while True:
    slowo = raw_input("Slowo:").lower()
    try:
        print (basic_form_dict[slowo])
    except KeyError:
        print slowo
    continue