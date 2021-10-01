import requests
from bs4 import BeautifulSoup
from typing import Tuple

def google_podcast(url: str) -> Tuple[str, str]:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    podcast = soup.select_one('.ik7nMd').text.strip()
    episode = soup.select_one('.wv3SK').text.strip()

    return podcast, episode

def podcast_addict(url: str) -> Tuple[str, str]:
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(page.content, 'html.parser')

    f = open('podcast_addict.html', 'w')
    f.write(str(soup))
    f.close()

    podcast = soup.select_one('.titlestack h1').text.strip()
    episode = soup.select_one('.titlestack h4').text.strip()

    return podcast, episode

def merkaz_yahel(url: str) -> Tuple[str, str]:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    podcast = 'בגוף ראשון'
    episode = soup.title.string.replace(' - מרכז יהל', '')

    return podcast, episode

def libby(url: str) -> Tuple[str, str]:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    book_name = soup.select_one('header h1').text
    author = soup.select_one('table tbody tr td').text
    return book_name, author
