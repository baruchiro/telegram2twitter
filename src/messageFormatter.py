from typing import Tuple
import requests
from bs4 import BeautifulSoup

def _get_libby_detailes(url: str) -> Tuple[str, str]:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    book_name = soup.select_one('header h1').text
    author = soup.select_one('table tbody tr td').text
    return book_name, author


def format(source: str) -> str:
    if 'share.libbyapp.com' in source:
        name, author = _get_libby_detailes(source)
        return f"קורא עכשיו:\n{name} ({author})\n{source}\n\nעם #ליבי #הספריה_הדיגיטלית_הישראלית @LibbyApp"
    return None