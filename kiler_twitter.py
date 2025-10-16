from bs4 import BeautifulSoup
from requests import get
import tweepy
import os
from dotenv import load_dotenv

def get_movie_message(url):
    
    headers = {
    "Accept-Language" : "en-US,en;q=0.5",
    "User-Agent": "Defined",
    }
    
    page = get(url, headers=headers)
    movie = BeautifulSoup(page.content, 'html.parser')
    title_tag = movie.find('h1', class_='title', itemprop='name')
    title = title_tag.get_text(strip=True) if title_tag else "Film"
    sched_section = movie.find('div', id='show-sched')
    
    if not sched_section:
        return None
    table = sched_section.find('table')
    if not table:
        return None
    for row in table.find('tbody').find_all('tr'):
        tds = row.find_all('td')
        if len(tds) < 3:
            continue
        today_text = tds[0].find('div').get_text(strip=True)
        time = tds[1].find('span').get_text(strip=True)
        channel = tds[2].find('a').get_text(strip=True)
        
        if today_text == "dziś":
            return f"{title} na {channel}, o godzinie {time}."
    return None

def authentication(status):

    api_key_secret = os.getenv('API_KEY_SECRET')
    api_key = os.getenv('API_KEY')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

    Client = tweepy.Client(consumer_key=api_key, consumer_secret=api_key_secret, access_token=access_token, access_token_secret=access_token_secret)
    Client.create_tweet(text=status)
    print("Message Sent.")
    
def send_message():
    URLS = [
        'https://www.teleman.pl/tv/Kiler-708394',
        'https://www.teleman.pl/tv/Kiler-Ow-2-Och-182289'
    ]
    messages = [get_movie_message(url) for url in URLS]
    filtered = [msg for msg in messages if msg]
    if not filtered:
        status = "Dzisiaj nie leci."
        authentication(status)
    else:
        status = ("Tak, dzisiaj leci.\n\n" + "\n".join(filtered))
        authentication(status)

if __name__ == "__main__":
    load_dotenv()
    send_message()