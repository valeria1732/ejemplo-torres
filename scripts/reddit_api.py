import requests
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0"
}

url = "https://www.reddit.com/r/technology/top.json?limit=20"

response = requests.get(url, headers=headers)

data = response.json()

posts = []

for post in data["data"]["children"]:
    p = post["data"]

    posts.append({
        "Titulo": p["title"],
        "Autor": p["author"],
        "Upvotes": p["ups"],
        "Comentarios": p["num_comments"],
        "URL": p["url"]
    })

df = pd.DataFrame(posts)

df.to_csv("../datos/reddit.csv", index=False)

print("Datos Reddit guardados")