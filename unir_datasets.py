import pandas as pd

print("Leyendo archivos...")

github = pd.read_csv("github.csv")
reddit = pd.read_csv("reddit.csv")
noticias = pd.read_csv("noticias.csv")

print("Archivos cargados")

github["Fuente"] = "GitHub"
reddit["Fuente"] = "Reddit"
noticias["Fuente"] = "HackerNews"

github = github.rename(columns={
    "Nombre": "Titulo"
})

github = github[["Titulo", "Fuente"]]
reddit = reddit[["Titulo", "Fuente"]]
noticias = noticias[["Titulo", "Fuente"]]

final = pd.concat([
    github,
    reddit,
    noticias
])

final.to_csv(
    "dataset_final.csv",
    index=False
)

print("Dataset final creado correctamente")
print(final.head())