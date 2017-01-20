import urllib2
from bs4 import BeautifulSoup as soup
import lemmatization_python as lemma
url = "http://www.naszemiasto.pl/lista_miejscowosci/"
coords_url = "http://astronomia.zagan.pl/art/wspolrzedne.html"

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

def get_articles():
    web_soup = soup(urllib2.urlopen(url), "html.parser")
    sub_sites = dict()

    categories = ["/wydarzenia/urzad-miasta/","/wydarzenia/regionalne/", "/wydarzenia/kryminalne/",
                  "/wydarzenia/rozmaitosci/", "/zmieniamy-miasto/", "/moto/wypadki/"]

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

    target_wojewodztwo = "wielkopolskie"

    # for wojewodztwo in sub_sites.iteritems():
    #     print wojewodztwo
    articles = []
    for i, elem in enumerate(sub_sites[target_wojewodztwo]):
        if i == 1:
            break
        for ii, category in enumerate(categories):
            if ii == 1:
                break
            final_url = elem+category
            print final_url


            web_soup = soup(urllib2.urlopen(final_url), "html.parser")
            # web_soup = soup(open("view-source_chodziez.naszemiasto.pl_wydarzenia_urzad-miasta_.html"), "html.parser")
            # print web_soup

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

news_list = get_articles()

news_lemma_dict = dict()  # Mapping news title to {big_letter_words:[], small_letter_words:[]}
for article in news_list:
    print article
    news_lemma_dict[article] = {"upper_case": [], "lower_case": []}
    title = soup(urllib2.urlopen(article), "html.parser").findAll(name="h1", class_="matTytul")[0].string
    print title
    content = soup(urllib2.urlopen(article), "html.parser").findAll(name="div", id="tresc")
    print content
    break










"""
    title = models.CharField(max_length=350)
    city = models.CharField(max_length=100)
    tags = models.CharField(max_length=350)
    link = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    geom = PointField()
"""
