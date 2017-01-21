# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
from urllib2 import urlopen
import csv
import time
strip_signs_list = ['.', '\r', '\n', '-', '"', "'", '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '<', '>', '/', '|']

def return_file_contents(filename):
        f = open(filename, 'r')  # opens the csv file
        row_list = f.readlines()
        f.close()      # closing
        return row_list

def delete_unallowed_signs(text):
    for ch in strip_signs_list:
        if ch in text:
            text = text.replace(ch, "")
    return text

def save_dict_to_csv(filename,dictionary, split_values=False):
    with open(filename+'.csv', 'w') as csvfile:
        mapping_writer = csv.writer(csvfile, delimiter=' ')
        for key,value in dictionary.items():
            if split_values:
                for val in value:
                    try:
                        mapping_writer.writerow([key.lower(), val.lower()])
                    except UnicodeEncodeError:
                        continue
            else:
                try:
                    mapping_writer.writerow([key.lower(), value.lower()])
                except UnicodeEncodeError:
                    continue

def save_synonyms_dict(filename,dictionary):
    new_dict = dict()
    for key,value in dictionary.items():
        #value is a set
        for val in value:
            new_dict[val] = key
    save_dict_to_csv(filename,new_dict)

def find_adjectives_and_nouns(word):
    try:
        adjective_list = set()
        try:
            wikipedia_url = "https://pl.wiktionary.org/wiki/{}".format(word)
            soup = BeautifulSoup(urlopen(wikipedia_url).read(), "html.parser")
        except TypeError:
            return
        except UnicodeEncodeError:
            return
        similar_words_result = soup.findAll('dd')
        for results in similar_words_result:
            try:
                text_splitted = results.text.split()
                if u'przym.' in text_splitted or u'rzecz.' in text_splitted: #Look for adjectives and similar nouns
                                for phrase in text_splitted[1:]:
                                    if len(phrase) > 3:
                                        adjective_list.add(delete_unallowed_signs(phrase).replace(',',''))
                                        # print delete_unallowed_signs(phrase).replace(',','')
            except TypeError:
                continue
        global_adjective_dict[word]=adjective_list
        time.sleep(0.1)
    except urllib2.HTTPError:
        return

def EXPERIMENTAL_find_synonyms_in_sjp(word):
    #Works only for some adjectives from town names like "poznański", "gnienieński", "pleszewski"
    #althogh the information is too unstructured to be usable besides use cases
    #Find similar words on SJP based on word form, altho its user created so a lot of stuff needs to be done to read the description
    word = delete_unallowed_signs(word)
    try:
        sjp_url = "http://sjp.pl/{}".format(word)
        soup = BeautifulSoup(urlopen(sjp_url).read(), "html.parser")
    except UnicodeEncodeError:
        return
    except urllib2.HTTPError:
        return
    test = soup.find('p', style="margin: .5em 0; font-size: medium; max-width: 32em; ")
    words_to_search = []
    text = ''
    try:
        for similar_word in test.contents:
            try:
                text = str(delete_unallowed_signs(similar_word).encode('utf-8', 'ignore')).replace(';',',').replace(':',',').split(",")
            except TypeError:
                text = delete_unallowed_signs(str(similar_word)).encode('utf-8', 'ignore').replace(';',',').replace(':',',').split(",")
            for found_word in text:
                    if found_word =="przymiotnik od":
                        continue
                    if found_word[0] == ' ':
                        words_to_search.append(found_word[1:])
                        print found_word[1:]
                    else:
                        words_to_search.append(found_word)
                        print found_word
    except AttributeError:
        pass

def declension_of_term(term):
    try:
        wikipedia_url = "https://pl.wiktionary.org/wiki/{}".format(term)
        # print wikipedia_url
    except UnicodeEncodeError:
        return
    try:
        soup = BeautifulSoup(urlopen(wikipedia_url).read(), "html.parser")
    except urllib2.HTTPError:
        return

    #Znajdz odmiany przez przypadki
    test_tags_type2 =  soup.find_all('table')
    for table in test_tags_type2:
        table_rows = table.find_all('td')
        for row in table_rows:
            if row.a == None:
                    print row.text, type(row.text)
                    lemat_dict[row.text] = term
    time.sleep(0.05)

global_adjective_dict = {} # Poznań : set(poznański, poznaniak ...)
lemat_dict={} #poznański : poznan
town_names = return_file_contents("miasta.txt")

for town in town_names:
    try:
        find_adjectives_and_nouns(town)

        declension_of_term(town)
        for adj_and_noun in global_adjective_dict[town]:
            print "ADJ/NOUN", adj_and_noun
            declension_of_term(adj_and_noun)
    except KeyError:
        continue

save_synonyms_dict("synonyms",global_adjective_dict)
save_dict_to_csv("lematization",lemat_dict)
# experimental_synonym_list= ["kaliski","pleszewski","poznański"]
# for word in experimental_synonym_list:
#     EXPERIMENTAL_find_synonyms_in_sjp(word)

def make_mapping(words):
    base_form_dict = {}
    for word in words:
        #Find similar words on SJP based on word form, altho its user created so a lot of stuff needs to be done to read the description
        word = delete_unallowed_signs(word)
        sjp_url = "http://sjp.pl/{}".format(word)
        soup = BeautifulSoup(urlopen(sjp_url).read(), "html.parser")
        test = soup.find('p', style="margin: .5em 0; font-size: medium; max-width: 32em; ")
        words_to_search = []
        text = ''
        for similar_word in test.contents:
            try:
                text = str(delete_unallowed_signs(similar_word).encode('utf-8', 'ignore')).replace(';',',').replace(':',',').split(",")
            except TypeError:
                text = delete_unallowed_signs(str(similar_word)).encode('utf-8', 'ignore').replace(';',',').replace(':',',').split(",")
            for found_word in text:
                if found_word != "br" and found_word != "przymiotnik od" and found_word !='':
                    print found_word[1:]
                    if found_word[0] == ' ':
                        words_to_search.append(found_word[1:])
                    else:
                        words_to_search.append(found_word)

        #Found the synonymous words like poznanskiego
        for synonymous_word in words_to_search:
            base_form_dict[synonymous_word] = word
            wikipedia_url = "https://pl.wiktionary.org/wiki/{}".format(synonymous_word)
            print wikipedia_url
            try:
                soup = BeautifulSoup(urlopen(wikipedia_url).read(), "html.parser")
            except urllib2.HTTPError:
                continue

            #Znajdz odmiany przez przypadki
            test_tags_type2 =  soup.find_all('table')
            for table in test_tags_type2:
                table_rows = table.find_all('td')
                for row in table_rows:
                    if row.a == None:
                            print row.text, type(row.text)
                            lemat_dict[row.text] = synonymous_word

