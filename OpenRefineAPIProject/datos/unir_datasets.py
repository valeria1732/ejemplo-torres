import pandas as pd

# Leer CSVs
github = pd.read_csv("github.csv")
reddit = pd.read_csv("reddit.csv")
noticias = pd.read_csv("noticias.csv")

# Agregar fuente
github["Fuente"] = "GitHub"
reddit["Fuente"] = "Reddit"
noticias["Fuente"] = "HackerNews"

# Cambiar nombre de columna
github = github.rename(columns={
    "Nombre": "Titulo"
})

# Seleccionar columnas
github = github[["Titulo", "Fuente"]]
reddit = reddit[["Titulo", "Fuente"]]
noticias = noticias[["Titulo", "Fuente"]]

# Unir datasets
final = pd.concat([github, reddit, noticias])

# Guardar resultado
final.to_csv("dataset_final.csv", index=False)

print("Dataset final creado")