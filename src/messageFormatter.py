from typing import Tuple
import requests
from bs4 import BeautifulSoup

def _get_libby_details(url: str) -> Tuple[str, str]:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    book_name = soup.select_one('header h1').text
    author = soup.select_one('table tbody tr td').text
    return book_name, author

podcast_to_tag = {
    'יחסינו לאן': '@ranlevi',
    'סייברסייבר': '@ohcybermycyber',
    'מדברימדע': '@MadaGadol',
    'ניהול מוצר - גרסת הבמאי': '@pm_edition',
    'הסדנא בשיחה‎': '@hasadna',
    'עושים תוכנה עם חן פלדמן ועמית בן דור Osim Tochna‎': '@ranlevi @chenosfeldman @amit_bend @ETL_Diner',
    'רברס עם פלטפורמה‎': '@reversim @rantav @orilahav',
    'מפתחים חסרי תרבות‎': '@notarbut',
    'בגוף ראשון': '#מרכז_יהל #בגוף_ראשון',
    'נקודה IL - הפודקאסט של איגוד האינטרנט הישראלי': '@ISOCIL',
    'קצרים על מסילת ישרים עם הרב הלל רוטקוף‎': '#הישיבה_הגבוהה_בני_נצרים',
    'חיות כיס Hayot Kiss‎': '@amsterdamski2 @TzlilAvraham #חיותכיס',
    'אלביט מדברים טכנולוגיה‎': '@ElbitSystemsLtd',
    'כגודל הציפייה‎': '@SivanAmitFranko',
    'גדי טאוב: שומר סף': '@GadiTaub1',
    'פרונטאנד לנד': '@nirbenya @eladlevy @FrontendLandIO',
    'קצרים: על מיתוג אישי, יצירת קשרים וקהילות‎': '@morad',
    'צרות בהייטק - הפודקאסט‎': '@Arbel2025 @eranyac @hitechproblems'
}

def _get_podcast_details(url: str) -> Tuple[str, str]:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    podcast = soup.select_one('.ik7nMd').text.strip()
    episode = soup.select_one('.wv3SK').text.strip()

    return podcast, episode

def _get_merkaz_yahel(url: str) -> Tuple[str, str]:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    podcast = 'בגוף ראשון'
    episode = soup.title.string.replace(' - מרכז יהל', '')

    return podcast, episode


def format(source: str) -> str:
    if 'share.libbyapp.com' in source:
        name, author = _get_libby_details(source)
        return f"קורא עכשיו:\n{name} ({author})\n{source}\n\nעם #ליבי #הספריה_הדיגיטלית_הישראלית @LibbyApp\n\n#פיד_קריאה #telegram2twitter"
    
    if 'podcasts.google.com' in source or 'merkazyahel.org.il' in source:
        podcast, episode = _get_podcast_details(source) if 'podcasts.google.com' in source else _get_merkaz_yahel(source)
        tag = podcast_to_tag.get(podcast, '')
        return f"מאזין עכשיו:\n{episode}\nמתוך הפודקאסט \"{podcast}\"\n{source}\n\n{tag} #פודקאסט #telegram2twitter"

    return None
