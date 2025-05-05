import pandas as pd
import requests
from bs4 import BeautifulSoup
import time


def fetch_google_trends_scrape():
    url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "xml")
    items = soup.find_all("item")
    records = [
        {
            "date": pd.Timestamp.now(),
            "keyword": item.title.text,
            "score": 1
        }
        for item in items if "decal" in item.title.text.lower()
    ]
    return pd.DataFrame(records)


def fetch_reddit_scrape():
    url = "https://www.reddit.com/r/cricut/search.json?q=decal&restrict_sr=1&sort=new"
    headers = {'User-agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    posts = r.json().get("data", {}).get("children", [])
    data = [
        {
            "date": pd.Timestamp.fromtimestamp(post['data']['created_utc']),
            "keyword": post['data']['title'],
            "score": post['data']['score']
        }
        for post in posts
    ]
    return pd.DataFrame(data)


def fetch_youtube_scrape():
    url = "https://www.youtube.com/results?search_query=vinyl+decal"
    headers = {'User-agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    titles = soup.find_all("a", attrs={"title": True})
    data = [
        {
            "date": pd.Timestamp.now(),
            "keyword": a['title'],
            "score": 1
        }
        for a in titles if "decal" in a['title'].lower()
    ]
    return pd.DataFrame(data[:20])


def fetch_all_sources():
    dfs = [
        fetch_google_trends_scrape(),
        fetch_reddit_scrape(),
        fetch_youtube_scrape(),
    ]
    return pd.concat(dfs, ignore_index=True)
