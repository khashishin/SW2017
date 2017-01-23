# -*- coding: utf-8 -*-
import csv
import codecs
import sys
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

class News:

    def __init__(self, link,published_date, title, lemmatized_words, tags):
        self.link = link
        self.published_date = published_date
        self.title = title
        self.lemmatized_words = lemmatized_words
        self.tags = tags

    def __str__(self):
        return self.link + ' '.join([word for word in self.lemmatized_words])

def get_cities_names_and_coords():
    cities_coords = dict()
    cities_to_news = dict()
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
            city_name = row_as_list[0].decode("utf-8")
            # Mapping city name to coords in format like this: ((19,42), (49,42))
            cities_coords[city_name] = ((row_as_list[1][0:2], row_as_list[1][4:6]), (row_as_list[2][0:2],row_as_list[2][4:6]))
            cities_to_news[city_name] = []
            # print row_as_list[0],  cities_coords[row_as_list[0]]

            # fmt = u'{:<15}'*len(row_as_list)
            # print fmt.format(*[s.decode('utf-8') for s in row_as_list])
    return cities_coords, cities_to_news

def get_tags_from_article(article_parser):
    tags = article_parser.findAll("meta", property="article:tag")[0]
    tags_list = []
    result = tags
    while result: # They have nested tags, need to do it "recursively".
        # print result["content"]
        tags_list.append(result["content"])
        try:
            result = result.findAll("meta", property="article:tag")[0]
        except IndexError:
            break
    # print tags.prettify()
    return tags_list

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


def most_common_in_list(lst):
    return max(set(lst), key=lst.count)

def get_published_date(article_parser):
    publish_date = article_parser.findAll("meta", property="article:published_time")[0]
    return publish_date["content"]

news_list = get_articles()





news_lemma_dict = dict()  # Mapping news title to {big_letter_words:[], small_letter_words:[]}

# LEMMATIZATION
lemma_dict = lemma.get_lemma_dict()

# City names, news and coordinates mapping.
city_to_coord_mapping, city_to_news_mapping = get_cities_names_and_coords()
# print repr([x.encode("utf-8") for x in city_to_news_mapping]).decode('string-escape')
# print repr([x.encode("utf-8") for x in city_to_coord_mapping]).decode('string-escape')
# print city_to_coord_mapping["chodzież"]

# print lemma_dict["przynajmowaną"]
# print lemma_dict["chodzieży"]

for article_link in news_list:
    print article_link

    article_parser = soup(urllib2.urlopen(article_link), "html.parser")

    # TITLE
    title = article_parser.findAll(name="h1", class_="matTytul")[0].string

    # DATE
    date_of_publishing = get_published_date(article_parser)
    # print date_of_publishing

    # TAGS
    tags = get_tags_from_article(article_parser)
    # print repr([x.encode("utf-8") for x in tags]).decode('string-escape')

    # CONTENT
    cities_names_mentioned_list = []
    word_collection= []
    content = article_parser.findAll(name="div", id="tresc")
    content = delete_unallowed_signs(replace_br_with_spaces(content[0]))
    for word in content.split():

        if word[0].isupper():
            try:
                base_form = lemma_dict[word.lower().encode('utf-8')]
                word_collection.append(base_form)
                # print word , "->", base_form
                base_form_with_upper_start = base_form.title()
                if base_form_with_upper_start in city_to_coord_mapping:
                    cities_names_mentioned_list.append(base_form_with_upper_start)
            except KeyError:
                word_collection.append(word)
                # print "Can't find base word for", word
    if len(cities_names_mentioned_list) > 0:
        news_origin_city = most_common_in_list(cities_names_mentioned_list)
        print "news jest z miasta:", news_origin_city
        city_to_news_mapping[news_origin_city].append(News(article_link,date_of_publishing, title, word_collection, tags))


    break

# for city, elem in city_to_news_mapping.iteritems():
#     if elem:
#         print city, [(x.link, x.lemmatized_words) for x in city_to_news_mapping[city]]




"""
    title = models.CharField(max_length=350)
    city = models.CharField(max_length=100)
    tags = models.CharField(max_length=350)
    link = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    geom = PointField()
"""
