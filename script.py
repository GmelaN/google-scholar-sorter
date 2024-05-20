import urllib.parse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import argparse
import time
from tqdm import tqdm
from random import randint
from collections import namedtuple

from tabulate import tabulate

def main(year_from, search_query, page_count):
    Paper = namedtuple("Paper", ["title", "link", "cites"])
    papers: list[Paper] = []

    base_url: str = "https://scholar.google.com/scholar?"

    for start in tqdm(range(0, page_count * 10, 10)):
        params = {
            "as_ylo": year_from,
            "start": start,
            "q": search_query
        }

        url = "{}{}".format(base_url, urllib.parse.urlencode(params))
        response = requests.get(url)
        bs = BeautifulSoup(response.text, "html.parser")

        paper_list = bs.findAll("div", {"class": "gs_or"})
        
        for paper in paper_list:
            title = paper.find("h3").find("a").text
            link = paper.find("h3").find("a").get("href")
            cites_string = "".join(string.text for string in paper.findAll("div", {"class": "gs_fl"}))
            cites = cites_string[cites_string.find("회") - 2 : cites_string.find("회") + 1].strip()

            if len(cites) == 0:
                continue

            cites = int(cites[:-1])  # 회 문자 제거하고 숫자 변환

            papers.append(Paper(title=title, link=link, cites=cites))
            time.sleep(randint(1, 5) * 0.1)  # 요청 간의 간격

    papers_sorted = sorted(papers, key=lambda x: -x.cites)
    DATA_TABLE: tuple = tuple((paper.cites, paper.title, paper.link) for paper in papers_sorted)

    # 결과를 CSV 파일과 표준 출력으로 저장
    with open("./papers.csv", "w", encoding="utf8") as f:
        f.write("cites, title, link\n")

        for paper in papers_sorted:
            line = f"{paper.cites}, {paper.title}, {paper.link}\n"
            f.write(line)

    print(tabulate(DATA_TABLE, headers=["cites", "title", "link"], tablefmt="grid"))  # 터미널에 출력

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search and save scholarly papers.")
    parser.add_argument("from_", type=str, help="Year from which to begin the search")
    parser.add_argument("query", type=str, help="Search query for the papers")
    parser.add_argument("page", type=int, help="Number of pages to crawl (each page typically contains 10 items)")

    args = parser.parse_args()

    main(args.from_, args.query, args.page)
