from typing import Tuple
import requests
from bs4 import BeautifulSoup
from fetcher import google_podcast, libby, podcast_addict, merkaz_yahel

podcast_to_tag = {
    'יחסינו לאן': '@ranlevi',
    'סייברסייבר': '@ohcybermycyber',
    'מדברימדע': '@MadaGadol',
    'ניהול מוצר - גרסת הבמאי': '@pm_edition',
    'הסדנא בשיחה‎': '@hasadna',
    'עושים תוכנה עם חן פלדמן ועמית בן דור Osim Tochna‎': '@ranlevi @chenosfeldman @amit_bend @ETL_Diner',
    'עושים היסטוריה עם רן לוי Osim Historia With Ran Levi‎': '@ranlevi',
    'רברס עם פלטפורמה‎': '@reversim @rantav @orilahav',
    'מפתחים חסרי תרבות‎': '@notarbut',
    'בגוף ראשון': '#מרכז_יהל #בגוף_ראשון',
    'נקודה IL - הפודקאסט של איגוד האינטרנט הישראלי': '@ISOCIL',
    'קצרים על מסילת ישרים עם הרב הלל רוטקוף‎': '#הישיבה_הגבוהה_בני_נצרים',
    'חיות כיס Hayot Kiss‎': '@amsterdamski2 @TzlilAvraham #חיותכיס',
    'אלביט מדברים טכנולוגיה‎': '@ElbitSystemsLtd',
    'כגודל הציפייה‎': '@SivanAmitFranko',
    'גדי טאוב: שומר סף': '@GadiTaub1',
    'פרונטאנד לנד\u200e': '@nirbenya @eladlevy @FrontendLandIO',
    'קצרים: על מיתוג אישי, יצירת קשרים וקהילות‎': '@morad',
    'צרות בהייטק - הפודקאסט‎': '@Arbel2025 @eranyac @hitechproblems',
    'ברווזגומי': '@BarvazG @VickiToVictory1',
    'מתמטיקה שמתמטיקה‎': '@ShirPeled',
    'לאן הלכת?‎': '@OfirUriel',
    'עגלה ריקה‎': '@ruth_elbaz @WeissInbar',
    'לא סופי Not Final‎': '@ymalchi @UshiShk @kann',
    'התמונה הגדולה‎': '@therealnirs @aviadby'
}

def _format_book(name: str, author: str, source: str) -> str:
    return f"קורא עכשיו:\n{name} ({author})\n{source}\n\nעם #ליבי #הספריה_הדיגיטלית_הישראלית @LibbyApp\n\n#פיד_קריאה #telegram2twitter"

def _format_podcast(podcast: str, episode: str, source: str) -> str:
    tag = podcast_to_tag.get(podcast, '')
    return f"מאזין עכשיו:\n{episode}\nמתוך הפודקאסט \"{podcast}\"\n{source}\n\n{tag} #פודקאסט #telegram2twitter"

def format(source: str) -> str:
    if 'share.libbyapp.com' in source:
        name, author = libby(source)
        return _format_book(name, author, source)
    
    if 'podcasts.google.com' in source:
        podcast, episode = google_podcast(source)
        return _format_podcast(podcast, episode, source)
    
    if 'merkazyahel.org.il' in source:
        podcast, episode = merkaz_yahel(source)
        return _format_podcast(podcast, episode, source)
    
    if 'podcastaddict.com' in source:
        podcast, episode = podcast_addict(source)
        return _format_podcast(podcast, episode, source)

    return None
