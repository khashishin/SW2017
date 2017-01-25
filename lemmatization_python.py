# -*- coding: utf-8 -*-

def open_file(filename):
        f = open(filename, 'r')  # opens the csv file
        row_list = f.readlines()
        f.close()      # closing
        return row_list

def get_lemma_dict():
    lemma_filename = 'full_mapping.csv'
    basic_form_dict = dict()
    lematted_rows = open_file(lemma_filename)
    for row in lematted_rows:
        row = row.lower().split()
        basic_form = row[1].decode("utf-8")
        grammatical_form = row[0]
        basic_form_dict[grammatical_form] = basic_form
    return basic_form_dict

def get_lemma_for_city_name_derivatives():
    lemma_filename = 'lemmat_add.txt'
    basic_form_dict = dict()
    lematted_rows = open_file(lemma_filename)
    for row in lematted_rows:
        row = row.lower().split()
        basic_form = row[1].decode("utf-8")
        grammatical_form = row[0].decode("utf-8")
        basic_form_dict[grammatical_form] = basic_form
    return basic_form_dict

def get_city_derivative_to_city_name_mapping():
    lemma_filename = 'synonyms.txt'
    basic_form_dict = dict()
    lematted_rows = open_file(lemma_filename)
    for row in lematted_rows:
        row = row.lower().split()
        basic_form = row[1].decode("utf-8")[1:-1]
        grammatical_form = row[0].decode("utf-8")
        basic_form_dict[grammatical_form] = basic_form
    return basic_form_dict


# Remember all words are parsed to lower case!!!
# print (basic_form_dict["gniezna"])

# t1= "helskimi".decode("utf-8")
#
# m1 = get_lemma_for_city_name_derivatives()
# m2 = get_city_derivative_to_city_name_mapping()
#
# res = ""
# if t1 in m1.keys():
#     res = m1[t1]
# if t1 in m1.values():
#     res = t1
#
# print m2[res]
