import urllib2
from bs4 import BeautifulSoup as soup
url = "http://www.naszemiasto.pl/lista_miejscowosci/"
web_soup = soup(urllib2.urlopen(url))
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

for wojewodztwo in sub_sites.iteritems():
    print wojewodztwo
