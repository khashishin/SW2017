import csv

def open_file(filename):
        f = open(filename, 'r')  # opens the csv file
        row_list = f.readlines()
        f.close()      # closing
        return row_list

def get_lemma_dict():
    lemma_filename = 'lemmatization-pl.txt'
    basic_form_dict = dict()
    lematted_rows = open_file(lemma_filename)
    for row in lematted_rows:
        row = row.lower().split()
        basic_form = row[0]
        grammatical_form = row[1]
        basic_form_dict[grammatical_form] = basic_form
    return basic_form_dict


# Remember all words are parsed to lower case!!!
# print (basic_form_dict["gniezna"])