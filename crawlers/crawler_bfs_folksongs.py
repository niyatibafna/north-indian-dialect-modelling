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
        logging.FileHandler("crawler_folksongs.log"),
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
        html = None
        attempts = 0
        while html is None and attempts < 30:
            attempts += 1
            try:
                html = requests.get(link, timeout=60).text
            except requests.ConnectionError as e:
                print("Connection Error \n")
                print(str(e))
                # raise
            except requests.Timeout as e:
                print("Timeout Error")
                print(str(e))
                # raise
            except requests.RequestException as e:
                print("General Error")
                print(str(e))
                # raise
            except KeyboardInterrupt:
                print("Someone closed the program")
                raise

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
        title = soup.find("h1").find("span")
        poem_text = ""

        if poem:
            poem_text = poem.text

        if not poem and lang and title:
            content = soup.find("div", {"id":"mw-content-text"}).find_all("p")
            for para in content:
                poem_text += para.text
            if poem_text:
                print(poem_text)

        if "फ़िलहाल इस पृष्ठ पर कोई सामग्री नहीं है" in poem_text:
            poem_text = ""

        if poem_text and "लोकगीत" not in title.text:
            poem_idx = len(self.data[lang]) + 1
            self.data[lang][poem_idx]["title"] = title.text if title else ""
            self.data[lang][poem_idx]["text"] = poem_text
            self.data[lang][poem_idx]["lang"] = {"dev":self.LANGS[lang], "rom":lang}
            return list()


        list_tags = {"ul", "ol"}
        neighbours = list()
        logging.info("NEIGHBOURS: \n\n\n")
        for list_tag in list_tags:
            try:
                content = soup.find("div", {"id":"mw-content-text"}).find_all(list_tag)
                if not content:
                    continue
            except:
                continue

            for collection in content:
                for link in collection.find_all('a'):
                    neighbour = self.validate_link(link.get("href"))
                    if neighbour is not None:
                        title = link.get("title")
                        if self.should_visit(neighbour, title, visited, lang):
                            neighbours.append(neighbour)
                            logging.info("{}\t{}".format(title, lang))

        logging.info("\n\n\n")
        return neighbours

    def should_visit(self, link, title, visited, lang):
        '''Returns True if we need to dfs at link'''
        bad_words = {"हाइकु", "श्रेणी", "साहित्य", "लोकगीत", "Lalit", "परिचय"}
        # if lang is not None and title is not None and self.LANGS[lang] not in title:
            # return False
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

    def build_visited(self, home_page, lang_links):

        neighbours = self.process_link(home_page, None, set())
        visited = set(neighbours)
        bad_links = {
        "http://kavitakosh.org/kk/%E0%A4%85%E0%A4%9C%E0%A5%8D%E0%A4%9E%E0%A4%BE%E0%A4%A4_%E0%A4%B0%E0%A4%9A%E0%A4%A8%E0%A4%BE%E0%A4%95%E0%A4%BE%E0%A4%B0#.E0.A4.85.E0.A4.82.E0.A4.97.E0.A4.BF.E0.A4.95.E0.A4.BE_.E0.A4.B0.E0.A4.9A.E0.A4.A8.E0.A4.BE.E0.A4.8F.E0.A4.81", \
        "http://kavitakosh.org/kk/%E0%A4%B9%E0%A4%BF%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A5%80_%E0%A4%B8%E0%A4%BE%E0%A4%B9%E0%A4%BF%E0%A4%A4%E0%A5%8D%E0%A4%AF_%E0%A4%AE%E0%A5%87%E0%A4%82_%E0%A4%B8%E0%A5%8D%E0%A4%A5%E0%A4%BE%E0%A4%A8_%E0%A4%AC%E0%A4%A8%E0%A4%BE%E0%A4%A4%E0%A5%80_%E0%A4%9C%E0%A4%BE%E0%A4%AA%E0%A4%BE%E0%A4%A8%E0%A5%80_%E0%A4%B5%E0%A4%BF%E0%A4%A7%E0%A4%BE%E0%A4%90%E0%A4%82", \
        }

        visited.add(home_page)
        visited.add("http://kavitakosh.org/kk/%E0%A4%95%E0%A4%B5%E0%A4%BF%E0%A4%A4%E0%A4%BE_%E0%A4%95%E0%A5%8B%E0%A4%B6_%E0%A4%AE%E0%A5%87%E0%A4%82_%E0%A4%AD%E0%A4%BE%E0%A4%B7%E0%A4%BE%E0%A4%8F%E0%A4%81")
        visited = visited.union(lang_links.values())
        return visited

    def save_bfs_variables(self, bfs_variables_path, visited, current_neighbours, collected, last_seen_lang):

        logging.info("Dumping bfs variables")

        if not os.path.exists(bfs_variables_path):
            os.mkdir(bfs_variables_path)

        filepath = bfs_variables_path+"visited.json"
        with open(filepath, "w") as f:
            json.dump(list(visited), f)

        filepath = bfs_variables_path+"current_neighbours.json"
        with open(filepath, "w") as f:
            json.dump(current_neighbours, f)

        filepath = bfs_variables_path+"collected.json"
        with open(filepath, "w") as f:
            json.dump(collected, f)

        filepath = bfs_variables_path+"last_seen_lang.json"
        with open(filepath, "w") as f:
            json.dump({"last_seen_lang": last_seen_lang}, f)

        logging.info("Done!")


    def intialize_bfs_variables(self, bfs_variables_path, lang_links):

        filepath = bfs_variables_path+"visited.json"
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                visited = set(json.load(f))
        else:
            visited = self.build_visited("http://kavitakosh.org/kk/कविता कोश में भाषाएँ", lang_links)
        with open(bfs_variables_path + "visited.json", "r") as f:
            poetry_visited = set(json.load(f))
        visited = visited.union(poetry_visited)

        filepath = bfs_variables_path+"current_neighbours.json"
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                current_neighbours = json.load(f)
        else:
            current_neighbours = {key:[val] for key, val in lang_links.items()}

        filepath = bfs_variables_path+"collected.json"
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                collected = json.load(f)
        else:
            collected = {key:0 for key in self.LANGS}

        filepath = bfs_variables_path+"last_seen_lang.json"
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                last_seen_lang = json.load(f)["last_seen_lang"]
        else:
            last_seen_lang = None

        return visited, current_neighbours, collected, last_seen_lang


    def bfs_and_save(self, lang_links, OUTDIR, bfs_variables_path):

        visited, current_neighbours, collected, last_seen_lang = self.intialize_bfs_variables(bfs_variables_path, lang_links)

        resuming = last_seen_lang != None
        level = 1

        while level < 4:
            level += 1
            logging.info("STARTING LEVEL {}".format(level))
            if not any([links for lang, links in current_neighbours.items()]):
                break
            for lang, neighbours in current_neighbours.items():
                if not neighbours:
                    logging.info("No neigbours for {}".format(lang))
                    continue
                if resuming:
                    if last_seen_lang == lang:
                        resuming = False
                    continue

                logging.info("LANG: {} \n\n\n".format(lang))
                current_neighbours[lang] = self.bfs_at_links(neighbours, lang, visited)

                if len(self.data[lang]) > 0:
                    self.save_lang(OUTDIR, lang, collected)
                self.save_bfs_variables(bfs_variables_path, visited, current_neighbours, collected, lang)

            self.save_bfs_variables(bfs_variables_path, visited, current_neighbours, collected, lang)



    def save_lang(self, OUTDIR, lang, collected):

        logging.info("Dumping {} files for lang {}".format(len(self.data[lang]), lang))
        if not os.path.isdir(OUTDIR):
            os.mkdir(OUTDIR)
        # for lang, lang_data in self.data.items():
        lang_dir = OUTDIR + "/" + lang + "/"
        if not os.path.isdir(lang_dir):
            os.mkdir(lang_dir)

        for idx, text_info in self.data[lang].items():
            # try:
            #     assert self.LANGS[lang] in text_info["title"]
            # except:
            #     print(text_info)
            #     print(self.LANGS[lang])
            #     raise
            collected[lang] += 1
            outpath = lang_dir + str(collected[lang]) + ".json"
            with open(outpath, "w") as f:
                json.dump(text_info, f, indent = 2, ensure_ascii = False)

        for idx in range(1, len(self.data[lang])+1):
            del self.data[lang][idx]

        logging.info("COLLECTED for lang {}: {}".format(lang, collected[lang]))


    def driver(self, lang_links, OUTDIR, bfs_variables_path):
        self.bfs_and_save(lang_links, OUTDIR, bfs_variables_path)

def main():
    lang_links = {
    "awadhi": "http://kavitakosh.org/kk/अवधी_लोकगीत", \
    "kannauji": "http://kavitakosh.org/kk/कन्नौजी_लोकगीत", \
    "kashmiri": "http://kavitakosh.org/kk/कश्मीरी_लोकगीत", \
    "kumaoni": "http://kavitakosh.org/kk/कुमाँऊनी_लोकगीत", \
    "khadi_boli": "http://kavitakosh.org/kk/खड़ी_बोली_लोकगीत", \
    "garwali": "http://kavitakosh.org/kk/गढ़वाली_लोकगीत", \
    "gujarati": "http://kavitakosh.org/kk/गुजराती_लोकगीत", \
    "chattisgarhi": "http://kavitakosh.org/kk/छत्तीसगढ़ी_लोकगीत", \
    "nimaadi": "http://kavitakosh.org/kk/निमाड़ी_लोकगीत", \
    "punjabi": "http://kavitakosh.org/kk/पंजाबी_लोकगीत", \
    "bangla": "http://kavitakosh.org/kk/बांग्ला_लोकगीत", \
    "bundeli": "http://kavitakosh.org/kk/बुन्देली_लोकगीत", \
    "brajbhasha": "http://kavitakosh.org/kk/ब्रजभाषा_लोकगीत", \
    "bhadavari": "http://kavitakosh.org/kk/भदावरी_लोकगीत", \
    "bhojpuri": "http://kavitakosh.org/kk/भोजपुरी_लोकगीत", \
    "magahi": "http://kavitakosh.org/kk/मगही_लोकगीत", \
    "marathi": "http://kavitakosh.org/kk/मराठी_लोकगीत", \
    "madiya": "http://kavitakosh.org/kk/माड़िया_लोकगीत", \
    "malwi": "http://kavitakosh.org/kk/मालवी_लोकगीत", \
    "maithili": "http://kavitakosh.org/kk/मैथिली_लोकगीत", \
    "rajasthani": "http://kavitakosh.org/kk/राजस्थानी_लोकगीत", \
    "hariyanvi": "http://kavitakosh.org/kk/हरियाणवी_लोकगीत", \
    "hindi-urdu": "http://kavitakosh.org/kk/हिन्दी_लोकगीत", \
    "himachali": "http://kavitakosh.org/kk/हिमाचली_लोकगीत", \
    "sanskrit": "http://kavitakosh.org/kk/संस्कृत_लोकगीत", \
    "koraku": "http://kavitakosh.org/kk/कोरकू_लोकगीत", \
    "bhil": "http://kavitakosh.org/kk/भील_लोकगीत", \
    "baiga": "http://kavitakosh.org/kk/बैगा_लोकगीत", \
    "angika":"http://kavitakosh.org/kk/अंगिका_लोकगीत", \
    }
    LANGS = {
    "bhil": "भील", \
    "baiga": "बैगा", \
    "koraku": "कोरक", \
    "angika": "अंगिका", \
    "awadhi": "अवधी", \
    "kannauji": "कन्नोजी", \
    "kashmiri": "कश्मीरी", \
    "kumaoni": "कुमाँऊनी", \
    "khadi_boli": "खड़ी बोली", \
    "garwali": "गढ़वाली", \
    "gujarati": "गुजरात", \
    "chattisgarhi": "छत्तीसगढ", \
    "nimaadi": "निमाड़ी", \
    "punjabi": "पंजाबी", \
    "bangla": "बांग्ला", \
    "bundeli": "बुन्देली", \
    "brajbhasha": "ब्रजभाषा", \
    "bhadavari": "भदावरी", \
    "bhojpuri": "भोजपुरी", \
    "magahi": "मगही", \
    "marathi": "मराठी", \
    "madiya": "माड़िया", \
    "malwi": "मालवी", \
    "maithili": "मैथिली", \
    "rajasthani": "राजस्थानी", \
    "hariyanvi": "हरियाणवी", \
    "hindi": "हिंदी-उर्दू", \
    "himachali": "हिमाचली", \
    "sanskrit": "संस्कृत", \
    }

    # lang_links = {key:val for key, val in lang_links.items() if key == "pali"}

    OUTDIR = "../data/crawled/folksongs/"
    bfs_variables_path = "crawl_variables/bfs_variables_folksongs/bfs_variables/"
    crawler = Crawler("http://kavitakosh.org", LANGS)

    crawler.driver(lang_links, OUTDIR, bfs_variables_path)


if __name__ == "__main__":
    main()
