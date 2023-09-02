import argparse
from os.path import isfile
from typing import List
from urllib.parse import unquote, urljoin, urlparse
import os

from bs4 import BeautifulSoup
import requests
from tqdm import tqdm


def validate_url(url: str) -> str:
    _ = urlparse(url)
    return url


def validate_output_directory(output_directory: str) -> str:
    if os.path.isdir(output_directory):
        return output_directory
    raise argparse.ArgumentTypeError(
        f"Supplied output directory '{output_directory}' does not exist, aborting!"
    )


def get_parser():
    parser = argparse.ArgumentParser(
        description="Crawls given url for content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("base_url", type=validate_url)
    parser.add_argument("--recurse", "-r", action="store_true")
    parser.add_argument(
        "--output-directory", "-o", type=validate_output_directory, default=os.getcwd()
    )
    parser.add_argument(
        "--extensions", "-e", nargs="+", type=str, default=[".cbr", ".pdf", ".epub"]
    )
    return parser


def download_file_idempotent(url, save_path):
    if os.path.isfile(save_path):
        return
    response = requests.get(url)
    with open(save_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=10**7):
            file.write(chunk)


def make_sub_output_directory(base: str, url: str) -> str:
    parts = urlparse(url)
    output_directory = os.path.join(base, unquote(parts.path.strip("/")))
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    return output_directory


def crawl_site(base_url: str, extensions: List[str], recurse: bool, output_directory: str):
    visited_urls = set()
    to_visit = [base_url]

    while to_visit:
        url = to_visit.pop()
        visited_urls.add(url)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract links to other pages and files
        if recurse:
            for link in soup.find_all("a"):
                href = link.get("href")
                if (
                    href
                    and not href.startswith(".")
                    and href not in visited_urls
                    and not any(href.endswith(ext) for ext in extensions)
                ):
                    to_visit.append(urljoin(url, href))

        # Download files (e.g., PDFs)
        sub_output_directory = make_sub_output_directory(output_directory, url)
        downloadable_links = [
            link
            for link in soup.find_all("a", href=True)
            if any(link["href"].endswith(ext) for ext in extensions)
        ]
        if not downloadable_links:
            continue
        dirparts = sub_output_directory.split(os.path.sep)
        last_folder = None
        while dirparts and last_folder is None:
            if dirparts[-1]:
                last_folder = unquote(dirparts[-1])
            else:
                dirparts.pop()
        for link in tqdm(downloadable_links, dynamic_ncols=True, desc=f"Files from {last_folder}"):
            href = link["href"]
            if any(href.endswith(ext) for ext in extensions):
                file_url = urljoin(url, href)
                file_name = os.path.join(sub_output_directory, unquote(os.path.basename(href)))
                download_file_idempotent(file_url, file_name)


def main():
    parser = get_parser()
    args = parser.parse_args()
    crawl_site(**vars(args))
