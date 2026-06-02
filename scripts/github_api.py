import requests
import pandas as pd

url = "https://api.github.com/search/repositories?q=AI&sort=stars"

response = requests.get(url)

data = response.json()

repos = []

for repo in data["items"]:
    repos.append({
        "Nombre": repo["name"],
        "Lenguaje": repo["language"],
        "Stars": repo["stargazers_count"],
        "Forks": repo["forks_count"],
        "URL": repo["html_url"]
    })

df = pd.DataFrame(repos)

df.to_csv("../datos/github.csv", index=False)

print("Datos GitHub guardados")