import urllib.parse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib

import time
from tqdm import tqdm
from random import randint
from collections import namedtuple


Paper = namedtuple("Paper", ["title", "link", "cites"])
papers: list[Paper] = []

base_url: str = "https://scholar.google.com/scholar?"

year_from: str = "2020"
search_query: str = "superframe"
# start: int = 0

for start in tqdm(range(0, 10, 10)):
    params = {
        "as_ylo": year_from,
        "start": start,
        "q": search_query
    }

    url = "{}{}".format(base_url, urllib.parse.urlencode(params))
    # print(url)

    response: requests.Response = requests.get(url)

    bs: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

    paper_list = bs.findAll("div", {"class": "gs_or"})

    for i, paper in enumerate(paper_list):
        title: str = paper.find("h3").find("a").text
        link: str = paper.find("h3").find("a").get("href")

        cites_string: str = ""
        for string in paper.findAll("div", {"class": "gs_fl"}):
            cites_string += string.text
        cites = cites_string[cites_string.find("회") - 2 : cites_string.find("회") + 1].strip()

        if len(cites) == 0:
            continue
            # cites = "0회"

        cites = int(cites[:-1])

        papers.append(Paper(title=title, link=link, cites=cites))
        time.sleep(0.1 + randint(0, 5) * 0.1)

papers = sorted(papers, key=lambda x: -x.cites)

with open("./papers.csv", "w", encoding="utf8") as f:
    f.write("cites, title, link\n")
    for paper in papers:
        f.write(str(paper.cites) + ', ')
        f.write(paper.title + ', ')
        f.write(paper.link)
        f.write("\n")
