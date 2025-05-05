from src.data_ingest import fetch_all_sources
from src.forecast import generate_forecast
import pandas as pd

print("Fetching trend data from multiple sources...")
df = fetch_all_sources()
df.to_csv("data/raw/all_sources.csv", index=False)

print("Generating forecast...")
forecast = generate_forecast(df)
forecast.to_csv("data/raw/forecast.csv", index=False)

print("Writing dashboard...")
html = f"""
<html>
<head><title>Decal AI Forecast</title></head>
<body>
<h1>Trending Decal Ideas</h1>
<p>Last updated: {pd.Timestamp.now()}</p>
<ul>
{''.join(f'<li>{row.keyword} (score: {row.score:.2f})</li>' for row in forecast.itertuples())}
</ul>
</body>
</html>
"""

with open("dashboard.html", "w") as f:
    f.write(html)
