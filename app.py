import requests
import pandas as pd

print("=" * 50)
print("PROYECTO OPENREFINE + APIs + PYTHON")
print("=" * 50)

# =========================================
# GITHUB API
# =========================================

print("\nObteniendo datos de GitHub...")

github_url = "https://api.github.com/search/repositories?q=AI&sort=stars"

github_response = requests.get(github_url)

github_data = github_response.json()

github_repos = []

for repo in github_data["items"]:

    github_repos.append({
        "Titulo": repo["name"],
        "Fuente": "GitHub",
        "Lenguaje": repo["language"],
        "Popularidad": repo["stargazers_count"],
        "URL": repo["html_url"]
    })

github_df = pd.DataFrame(github_repos)

print("GitHub OK")


# =========================================
# REDDIT API
# =========================================

print("\nObteniendo datos de Reddit...")

headers = {
    "User-Agent": "Mozilla/5.0"
}

reddit_url = "https://www.reddit.com/r/technology/top.json?limit=20"

reddit_response = requests.get(
    reddit_url,
    headers=headers
)

reddit_data = reddit_response.json()

reddit_posts = []

for post in reddit_data["data"]["children"]:

    p = post["data"]

    reddit_posts.append({
        "Titulo": p["title"],
        "Fuente": "Reddit",
        "Lenguaje": "N/A",
        "Popularidad": p["ups"],
        "URL": p["url"]
    })

reddit_df = pd.DataFrame(reddit_posts)

print("Reddit OK")


# =========================================
# HACKER NEWS API
# =========================================

print("\nObteniendo noticias HackerNews...")

top = requests.get(
    "https://hacker-news.firebaseio.com/v0/topstories.json"
).json()

news = []

for story_id in top[:20]:

    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"

    story = requests.get(story_url).json()

    news.append({
        "Titulo": story.get("title"),
        "Fuente": "HackerNews",
        "Lenguaje": "N/A",
        "Popularidad": story.get("score"),
        "URL": story.get("url")
    })

news_df = pd.DataFrame(news)

print("HackerNews OK")


# =========================================
# UNIR TODOS LOS DATASETS
# =========================================

print("\nUniendo datasets...")

final_df = pd.concat([
    github_df,
    reddit_df,
    news_df
])

# Guardar dataset completo
final_df.to_csv(
    "dataset_final.csv",
    index=False
)

print("Dataset final guardado")


# =========================================
# ESTADISTICAS
# =========================================

print("\nCalculando estadísticas...")

total = len(final_df)

fuentes = final_df["Fuente"].value_counts()

estadisticas = pd.DataFrame({
    "Metrica": [
        "Total registros",
        "GitHub",
        "Reddit",
        "HackerNews"
    ],
    "Valor": [
        total,
        fuentes.get("GitHub", 0),
        fuentes.get("Reddit", 0),
        fuentes.get("HackerNews", 0)
    ]
})

# Guardar estadísticas
estadisticas.to_csv(
    "estadisticas.csv",
    index=False
)

print("\nESTADISTICAS")
print(estadisticas)

print("\nArchivos creados:")
print("- dataset_final.csv")
print("- estadisticas.csv")


# =========================================
# VISTA PREVIA
# =========================================

print("\nVISTA PREVIA DATASET")
print(final_df.head())

print("\nPROYECTO TERMINADO")
print("=" * 50)