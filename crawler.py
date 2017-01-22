# -*- coding: utf-8 -*-
import csv
import codecs
import urllib2
from bs4 import BeautifulSoup as soup
import lemmatization_python as lemma
url = "http://www.naszemiasto.pl/lista_miejscowosci/"
coords_url = "http://astronomia.zagan.pl/art/wspolrzedne.html"
strip_signs_list = [',', '.', '\r', '\n', '-', '"', "'", ":", "(", ")", "#", "^", "&", "!", "?", "[", "]"]
categories = ["/wydarzenia/urzad-miasta/","/wydarzenia/regionalne/", "/wydarzenia/kryminalne/",
                  "/wydarzenia/rozmaitosci/", "/zmieniamy-miasto/", "/moto/wypadki/"]
target_wojewodztwo = "wielkopolskie"
# ze stron danego wojewodztwa pobrac informacje
# lematyzowac informacje
#     osobno zapisac wyrazy z duzymy literami,
#        jezeli po zlematyzowaniu sa w zbiorze z coords to to sa miasto
#     osobno zwykle wyrazy - posluza do liczenia relewancji
# wybrac tylko te informacje ktore w tresci lub tytule maja miasto
# przypisac wiadomosc do tego miasta, ktore najczesciej jest wspominane w wiadomosci

# Wspolrzedne miast - http://astronomia.zagan.pl/art/wspolrzedne.html
# mapowac miasto do zbioru info jezeli sa relewantne do zapytania
# rel

def get_cities_names_and_coords():
    cities_coords = dict()
    # f = codecs.open("cities_coords.csv", encoding='utf-8')
    # for line in f:
    #     print unicode(line).encode('utf8'), type(unicode(line).encode('utf8'))

    # with open("cities_coords.csv", 'r') as in_file:
    #     reader = csv.reader(in_file, delimiter=",", encoding='utf-8')
    #     for row in reader:
    #         print [ unicode(x).encode('utf8') for x in row]
    with open("cities_coords.csv", 'r') as in_file:
        reader = csv.reader(in_file, delimiter=",")
        for row in reader:
            row_as_list = list(row)
            # Mapping city name to coords in format like this: ((19,42), (49,42))
            cities_coords[row_as_list[0]] = ((row_as_list[1][0:2], row_as_list[1][4:6]), (row_as_list[2][0:2],row_as_list[2][4:6]))
            # print row_as_list[0],  cities_coords[row_as_list[0]]

            # fmt = u'{:<15}'*len(row_as_list)
            # print fmt.format(*[s.decode('utf-8') for s in row_as_list])
    return cities_coords
def get_articles():
    web_soup = soup(urllib2.urlopen(url), "html.parser")
    sub_sites = dict()
    my_div = web_soup.find_all(name="ul", attrs={'class': "region"})
    for elem in my_div:
        for li_region in elem.findChildren():
            wojewodzka_strona = ""
            h3_elem = li_region.find_all(name="h3")
            for h3 in h3_elem:
                wojewodzka_strona = h3.find_all(name="a")[0]["href"].split("//")[1].split(".")[0]
                # removing http and '.naszemiasto.pl'
                sub_sites[wojewodzka_strona] = []

            ul_elems = li_region.find_all(name="ul")
            for ul in ul_elems:
                li_elems = ul.find_all(name="li")
                for li in li_elems:
                    a_elem = li.find(name="a")
                    sub_sites[wojewodzka_strona].append( a_elem['href'])

    articles = []
    for i, elem in enumerate(sub_sites[target_wojewodztwo]):
        if i == 1:
            break
        for ii, category in enumerate(categories):
            if ii == 1:
                break
            final_url = elem+category

            web_soup = soup(urllib2.urlopen(final_url), "html.parser")
            # Najwiekszy news na gorze
            top_section = web_soup.findAll(name="section", id="rotator-sb")
            for element in top_section:
                for a in element.findAll(name="a"):
                    try:
                        if len(a["href"]) > 1:
                            articles.append(elem+a["href"])
                    except:
                        pass
            # Glowna lista pionowa
            srodek = web_soup.findAll(name="div", id="kol-srodek")
            for kol in srodek:
                clearfix_section = kol.findAll(name="article", class_="clearfix")
                for clearfix in clearfix_section:
                    for a in clearfix.findAll(name="a"):
                        if a["href"][0:9] == "/artykul/":
                            articles.append(elem+a["href"])

            # Dolne 3 newsy
            dol = web_soup.findAll(name="section", class_="aktualnosciLista poleSrodek")
            for dolny_wiersz in dol:
                lista_dol = dolny_wiersz.findAll(name="a")
                for a in lista_dol:
                    if a["href"][0:9] == "/artykul/":
                        articles.append(elem+a["href"])
    return list(set(articles))

def replace_br_with_spaces(elem):
    text = ''
    for e in elem.recursiveChildGenerator():
        if isinstance(e, basestring):
            text += e.strip()
        elif e.name == 'br':
            text += ' '
    return text

def delete_unallowed_signs(text):
    for ch in strip_signs_list:
        if ch in text:
            text = text.replace(ch, "")
    return text

news_list = get_articles()

news_lemma_dict = dict()  # Mapping news title to {big_letter_words:[], small_letter_words:[]}
# LEMMATIZATION
# lemma_dict = lemma.get_lemma_dict()

# City names and coordinates mapping.
city_to_coord_mapping = get_cities_names_and_coords()


# city_to_news_mapping = dict()
# cities_list = []
# # print lemma_dict["poznania"]
#
# for article in news_list:
#     print article
#     news_lemma_dict[article] = {"upper_case": [], "lower_case": []}
#     article_parser = soup(urllib2.urlopen(article), "html.parser")
#     title = article_parser.findAll(name="h1", class_="matTytul")[0].string
#     print title
#     content = article_parser.findAll(name="div", id="tresc")
#     content = delete_unallowed_signs(replace_br_with_spaces(content[0]))
#     for word in content.split():
#         print word
#     break













"""
    title = models.CharField(max_length=350)
    city = models.CharField(max_length=100)
    tags = models.CharField(max_length=350)
    link = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    geom = PointField()
"""
