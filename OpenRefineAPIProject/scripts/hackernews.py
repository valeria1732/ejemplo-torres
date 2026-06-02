import requests
import pandas as pd

top = requests.get(
    "https://hacker-news.firebaseio.com/v0/topstories.json"
).json()

noticias = []

for story_id in top[:20]:

    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"

    story = requests.get(url).json()

    noticias.append({
        "Titulo": story.get("title"),
        "Score": story.get("score"),
        "Autor": story.get("by"),
        "URL": story.get("url")
    })

df = pd.DataFrame(noticias)

df.to_csv("../datos/noticias.csv", index=False)

print("Noticias guardadas")