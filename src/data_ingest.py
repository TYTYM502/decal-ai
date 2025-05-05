import pandas as pd
import requests
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
import praw
from googleapiclient.discovery import build
import time


def fetch_google_trends():
    pytrends = TrendReq()
    pytrends.build_payload(["vinyl decal", "car sticker", "wall decal"])
    df = pytrends.interest_over_time()
    df = df.drop(columns=['isPartial'])
    df = df.reset_index().melt(id_vars='date', var_name='keyword', value_name='score')
    return df


def fetch_reddit():
    reddit = praw.Reddit(client_id='XXX', client_secret='XXX', user_agent='decal-ai')
    posts = []
    for post in reddit.subreddit("cricut").search("decal", limit=50):
        posts.append({'date': pd.to_datetime(post.created_utc, unit='s'), 'keyword': post.title, 'score': post.score})
    return pd.DataFrame(posts)


def fetch_youtube():
    yt = build('youtube', 'v3', developerKey='YOUR_YOUTUBE_API_KEY')
    req = yt.search().list(q='vinyl decal', part='snippet', maxResults=25)
    res = req.execute()
    return pd.DataFrame([{'date': pd.Timestamp.now(), 'keyword': i['snippet']['title'], 'score': 1} for i in res['items']])


def fetch_all_sources():
    dfs = [
        fetch_google_trends(),
        fetch_reddit(),
        fetch_youtube(),
    ]
    return pd.concat(dfs, ignore_index=True)
  
