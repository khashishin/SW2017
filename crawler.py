import urllib2
from bs4 import BeautifulSoup as soup
url = "http://www.naszemiasto.pl/lista_miejscowosci/"
web_soup = soup(urllib2.urlopen(url), "html.parser")
sub_sites = dict()

# ze stron danego wojewodztwa pobrac informacje
# wybrac tylko te informacje ktore w tresci lub tytule maja miasto
# lematyzowac
# Wspolrzedne miast - http://astronomia.zagan.pl/art/wspolrzedne.html
# mapowac miasto do zbioru info jezeli sa relewantne do zapytania
# rel
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
        if ii == 2:
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
                    if len(a["href"]) >1:
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
        dol = web_soup.findAll(name="section", class_="aktualnosciLista poleSrodek")[0]
        lista_dol = dol.findAll(name="a")
        for a in lista_dol:
            if a["href"][0:9] == "/artykul/":
                articles.append(elem+a["href"])


print len(articles),  len(set(articles))
for e in set(articles):
    print e










"""
    title = models.CharField(max_length=350)
    city = models.CharField(max_length=100)
    tags = models.CharField(max_length=350)
    link = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    geom = PointField()
"""
