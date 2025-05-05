import pandas as pd

def generate_forecast(df):
    df['keyword'] = df['keyword'].str.lower()
    top_keywords = df.groupby('keyword')['score'].sum().sort_values(ascending=False).head(20)
    return top_keywords.reset_index().rename(columns={'score': 'score'})
