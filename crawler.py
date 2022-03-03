#!/usr/bin/env python3
import json
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

class Crawler():

    def __init__(self, DOMAIN, LANGS):
        self.DOMAIN = DOMAIN
        self.data = defaultdict(lambda:list())
        self.LANGS = LANGS

    def validate_link(self, link):
        # Make relative link absolute
        if link is None:
            return None
        if not link.startswith("/kk") and not link.startswith(self.DOMAIN):
            return None
        if not link.startswith(self.DOMAIN):
            link = self.DOMAIN + link
        # try:
        #     response = requests.get(link)
        # except:
        #     print("Link couldn't be followed: {}", link)
        #     return None
        return link

    def crawl_link(self, link):
        '''Reads URL link and returns data'''
        html = requests.get(link).text

        return html

    def process_link(self, link, lang):
        # if contains poem, add poem to self.data[lang]
        # if not, return valid link per child (i.e. if it's a relative link, make
        # it absolute)

        html_text = self.crawl_link(link)
        # print("Obtained text!")
        soup = BeautifulSoup(html_text, 'html.parser')
        # print("Parsed HTML")

        poem = soup.find(attrs={"class":"poem"})

        if poem:
            self.data[lang].append(poem.text)
            return list()


        content = soup.find("div", {"id":"mw-content-text"}).find_all("ul")
        if not content:
            return list()

        neighbours = list()
        for unordered_list in content:
            for link in unordered_list.find_all('a'):
                neighbour = self.validate_link(link.get("href"))
                if neighbour:
                    neighbours.append(neighbour)
                    print(link.get("title"), lang)

        # print("Got neighbours")
        return neighbours

    def should_visit(self, link, visited):
        '''Returns True if we need to dfs at link'''
        if link in visited or "otherapps" in link:
            return False
        for key, val in self.LANGS.items():
            if val in link:
                return False
        return True


    def dfs_at_link(self, link, lang, visited):
        # If poem not found, DFS at all non-visited neighbours
        # print(link, lang)
        neighbours = self.process_link(link, lang)
        visited.add(link)
        print("PARENT: ", link)
        for neighbour in neighbours:
            if self.should_visit(neighbour, visited):
                self.dfs_at_link(neighbour, lang, visited)


    def dfs(self, lang_links):

        visited = set(lang_links.values())
        for lang, link in lang_links.items():
            self.dfs_at_link(link, lang, visited)
            print("COLLECTED: ", len(self.data[lang]))

    def save(self, outpath):
        # Save self.data as JSON file
        # TODO
        with open(outpath, "w") as f:
            json.dump(self.data, f, indent = 2)

    def driver(self, lang_links):
        self.dfs(lang_links)
        self.save("data/poetry.json")



def main():
    lang_links = {"angika":"http://kavitakosh.org/kk/अंगिका", \
    "awadhi": "http://kavitakosh.org/kk/अवधी", \
    "garwali": "http://kavitakosh.org/kk/गढ़वाली", \
    "gujarati": "http://kavitakosh.org/kk/गुजराती", \
    "chattisgarhi": "http://kavitakosh.org/kk/छत्तीसगढ़ी", \
    "nepali": "http://kavitakosh.org/kk/नेपाली", \
    "pali": "http://kavitakosh.org/kk/पालि", \
    "braj": "http://kavitakosh.org/kk/ब्रज भाषा", \
    "marathi": "http://kavitakosh.org/kk/मराठी", \
    "maithili": "http://kavitakosh.org/kk/मैथिली", \
    "rajasthani": "http://kavitakosh.org/kk/राजस्थानी", \
    "sanskrit": "http://kavitakosh.org/kk/संस्कृतम्‌", \
    "sindhi": "http://kavitakosh.org/kk/सिन्धी", \
    "hariyanvi": "http://kavitakosh.org/kk/हरियाणवी", \
    "bhojpuri": "http://kavitakosh.org/kk/भोजपुरी", \
    "magahi": "http://kavitakosh.org/kk/मगही", \
    "bajjika": "http://kavitakosh.org/kk/बज्जिका", \
    }
    LANGS = {
    "angika":"अंगिका", \
    "awadhi": "अवधी", \
    "garwali": "गढ़वाली", \
    "gujarati": "गुजराती", \
    "chattisgarhi": "छत्तीसगढ़ी", \
    "nepali": "नेपाली", \
    "pali": "पालि", \
    "braj": "ब्रज भाषा", \
    "marathi": "मराठी", \
    "maithili": "मैथिली", \
    "rajasthani": "राजस्थानी", \
    "sanskrit": "संस्कृतम्‌", \
    "sindhi": "सिन्धी", \
    "hariyanvi": "हरियाणवी", \
    "bhojpuri": "भोजपुरी", \
    "magahi": "मगही", \
    "bajjika": "बज्जिका", \
    }
    crawler = Crawler("http://kavitakosh.org", LANGS)
    crawler.driver(lang_links)


if __name__ == "__main__":
    main()
