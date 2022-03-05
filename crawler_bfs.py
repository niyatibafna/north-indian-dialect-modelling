#!/usr/bin/env python3
import logging
import json
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import os
import sys


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.FileHandler("crawler.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

class Crawler():

    def __init__(self, DOMAIN, LANGS):
        self.DOMAIN = DOMAIN
        self.data = defaultdict(lambda:defaultdict(dict))
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

    def process_link(self, link, lang, visited):
        # if contains poem, add poem to self.data[lang]
        # if not, return valid link per child (i.e. if it's a relative link, make
        # it absolute)

        html_text = self.crawl_link(link)
        # print("Obtained text!")
        soup = BeautifulSoup(html_text, 'html.parser')
        # print("Parsed HTML")

        poem = soup.find(attrs={"class":"poem"})

        if poem:
            title = soup.find("h1").find("span")
            poem_idx = len(self.data[lang]) + 1
            self.data[lang][poem_idx]["title"] = title.text if title else ""
            self.data[lang][poem_idx]["text"] = poem.text
            self.data[lang][poem_idx]["lang"] = {"dev":self.LANGS[lang], "rom":lang}
            return list()

        list_tags = {"ul", "ol"}
        neighbours = list()
        logging.info("NEIGHBOURS: \n\n\n")
        for list_tag in list_tags:
            content = soup.find("div", {"id":"mw-content-text"}).find_all(list_tag)
            if not content:
                continue

            for collection in content:
                for link in collection.find_all('a'):
                    neighbour = self.validate_link(link.get("href"))
                    if neighbour is not None:
                        title = link.get("title")
                        if self.should_visit(neighbour, title, visited):
                            neighbours.append(neighbour)
                            logging.info("{}\t{}".format(title, lang))

        logging.info("\n\n\n")
        return neighbours

    def should_visit(self, link, title, visited):
        '''Returns True if we need to dfs at link'''
        bad_words = {"हाइकु", "श्रेणी", "साहित्य"}
        if link in visited or "otherapps" in link:
            return False
        for key, val in self.LANGS.items():
            if val in link:
                return False
        if title:
            for bad_word in bad_words:
                if bad_word in title:
                    return False
        return True


    def bfs_at_links(self, neighbours, lang, visited):

        new_neighbours = list()
        for link in neighbours:
            logging.info("SEARCHING AT : {}".format(link))
            new_neighbours += self.process_link(link, lang, visited)
        visited = visited.union(set(new_neighbours))

        return new_neighbours

    def build_visited(self, home_page):

        neighbours = self.process_link(home_page, None, set())
        visited = set(neighbours)
        bad_links = {
        "http://kavitakosh.org/kk/%E0%A4%85%E0%A4%9C%E0%A5%8D%E0%A4%9E%E0%A4%BE%E0%A4%A4_%E0%A4%B0%E0%A4%9A%E0%A4%A8%E0%A4%BE%E0%A4%95%E0%A4%BE%E0%A4%B0#.E0.A4.85.E0.A4.82.E0.A4.97.E0.A4.BF.E0.A4.95.E0.A4.BE_.E0.A4.B0.E0.A4.9A.E0.A4.A8.E0.A4.BE.E0.A4.8F.E0.A4.81", \
        "http://kavitakosh.org/kk/%E0%A4%B9%E0%A4%BF%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A5%80_%E0%A4%B8%E0%A4%BE%E0%A4%B9%E0%A4%BF%E0%A4%A4%E0%A5%8D%E0%A4%AF_%E0%A4%AE%E0%A5%87%E0%A4%82_%E0%A4%B8%E0%A5%8D%E0%A4%A5%E0%A4%BE%E0%A4%A8_%E0%A4%AC%E0%A4%A8%E0%A4%BE%E0%A4%A4%E0%A5%80_%E0%A4%9C%E0%A4%BE%E0%A4%AA%E0%A4%BE%E0%A4%A8%E0%A5%80_%E0%A4%B5%E0%A4%BF%E0%A4%A7%E0%A4%BE%E0%A4%90%E0%A4%82", \
        }

        visited.add(home_page)
        visited.add("http://kavitakosh.org/kk/%E0%A4%95%E0%A4%B5%E0%A4%BF%E0%A4%A4%E0%A4%BE_%E0%A4%95%E0%A5%8B%E0%A4%B6_%E0%A4%AE%E0%A5%87%E0%A4%82_%E0%A4%AD%E0%A4%BE%E0%A4%B7%E0%A4%BE%E0%A4%8F%E0%A4%81")
        return visited


    def bfs_and_save(self, lang_links, OUTDIR):

        visited = self.build_visited("http://kavitakosh.org/kk/कविता कोश में भाषाएँ")
        visited = visited.union(lang_links.values())

        current_neighbours = {key:[val] for key, val in lang_links.items()}
        saved = set()

        while True:
            for lang, neighbours in current_neighbours.items():
                if not neighbours and lang not in saved:
                    self.save_lang(OUTDIR, lang)
                    saved.add(lang)
                    continue
                logging.info("LANG: {} \n\n\n".format(lang))
                current_neighbours[lang] = self.bfs_at_links(neighbours, lang, visited)
                logging.info("COLLECTED: {}".format(len(self.data[lang])))

            if not any([links for lang, links in current_neighbours.items()]):
                break

    def save_lang(self, OUTDIR, lang):

        if not os.path.isdir(OUTDIR):
            os.mkdir(OUTDIR)
        # for lang, lang_data in self.data.items():
        lang_dir = OUTDIR + "/" + lang + "/"
        if not os.path.isdir(lang_dir):
            os.mkdir(lang_dir)
        for file_idx, text_info in self.data[lang].items():
            outpath = lang_dir + str(file_idx) + ".json"
            with open(outpath, "w") as f:
                json.dump(text_info, f, indent = 2, ensure_ascii = False)

    def driver(self, lang_links, OUTDIR):
        self.bfs_and_save(lang_links, OUTDIR)

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
    "hindi-urdu": "http://kavitakosh.org/kk/रचनाकारों की सूची"
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
    "hindi-urdu": "हिंदी-उर्दू"
    }

    # lang_links = {key:val for key, val in lang_links.items() if key == "pali"}

    OUTDIR = "data/crawled/"
    crawler = Crawler("http://kavitakosh.org", LANGS)
    crawler.driver(lang_links, OUTDIR)


if __name__ == "__main__":
    main()
