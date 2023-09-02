# The Crawler

Web crawling utility for downloading files from an exposed filesystem.

# Installation

## From PyPI

This assumes you have [Python 3.10+](https://www.python.org/downloads/) installed and `pip3` is on
your path:

```bash
~$ pip3 install the-crawler
...
~$ hms-import -h
usage: the-crawler [-h] [--recurse] [--output-directory OUTPUT_DIRECTORY] [--extensions EXTENSIONS [EXTENSIONS ...]] base_url

Crawls given url for content

positional arguments:
  base_url

options:
  -h, --help            show this help message and exit
  --recurse, -r
  --output-directory OUTPUT_DIRECTORY, -o OUTPUT_DIRECTORY
  --extensions EXTENSIONS [EXTENSIONS ...], -e EXTENSIONS [EXTENSIONS ...]
```

## From Source

This assumes you have [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), [Python
3.10+](https://www.python.org/downloads/), and
[poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) installed
already.

```bash
~$ git clone git@gitlab.com:woodforsheep/the-crawler.git
...
~$ cd the-crawler
the-crawler$ poetry install
...
the-crawler$ poetry run the-crawler -h
```
