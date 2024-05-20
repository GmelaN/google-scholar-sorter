# Sort Google Scholar search result by cite count
## Requirements

- python >= 3.9
- tabulate >= 0.9.0
- BeautifulSoup >= 4.12.3
- requests >= 2.31.0
- urllib3 >= 2.2.1

to install all requirements run this:
```
$ pip install tabulate bs4 requests urllib
```
## How to use

to learn how to use this program, type this:
```
$ python script.py -h
positional arguments:
  from_       Year from which to begin the search
  query       Search query for the papers
  page        Number of pages to crawl (each page typically contains 10 items)

options:
  -h, --help  show this help message and exit
```

for example, if you want to search "TDMA" published after 2021, 5 pages from result type this:

```
$ python script.py 2021 TDMA 5
```
