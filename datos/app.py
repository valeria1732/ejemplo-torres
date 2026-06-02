# DASHBOARD PROFESIONAL EN PYTHON (ESTILO DATA SCIENCE PRO)

import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

# ==========================================================
# CONFIGURACION VISUAL PROFESIONAL
# ==========================================================

plt.style.use("dark_background")

# ==========================================================
# TITULO
# ==========================================================

print("\n" + "="*70)
print("      DASHBOARD PROFESIONAL OPENREFINE + APIs")
print("="*70)

# ==========================================================
# GITHUB API
# ==========================================================

print("\nObteniendo datos de GitHub...")

github_url = "https://api.github.com/search/repositories?q=AI&sort=stars"

github_response = requests.get(github_url)

github_data = github_response.json()

github_repos = []

for repo in github_data["items"][:40]:

    github_repos.append({
        "Titulo": repo["name"],
        "Fuente": "GitHub",
        "Popularidad": repo["stargazers_count"],
        "URL": repo["html_url"]
    })

github_df = pd.DataFrame(github_repos)

print("GitHub OK")

# ==========================================================
# HACKER NEWS API
# ==========================================================

print("\nObteniendo noticias HackerNews...")

top = requests.get(
    "https://hacker-news.firebaseio.com/v0/topstories.json"
).json()

news = []

for story_id in top[:40]:

    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"

    story = requests.get(story_url).json()

    news.append({
        "Titulo": story.get("title"),
        "Fuente": "HackerNews",
        "Popularidad": story.get("score", 0),
        "URL": story.get("url")
    })

news_df = pd.DataFrame(news)

print("HackerNews OK")

# ==========================================================
# UNIR DATASETS
# ==========================================================

print("\nUniendo datasets...")

final_df = pd.concat([
    github_df,
    news_df
])

# ==========================================================
# LIMPIEZA
# ==========================================================

final_df.dropna(inplace=True)

final_df.drop_duplicates(inplace=True)

final_df["Popularidad"] = pd.to_numeric(
    final_df["Popularidad"],
    errors="coerce"
)

# ==========================================================
# ESTADISTICAS
# ==========================================================

total = len(final_df)

promedio = final_df["Popularidad"].mean()

maximo = final_df["Popularidad"].max()

minimo = final_df["Popularidad"].min()

mediana = final_df["Popularidad"].median()

desviacion = final_df["Popularidad"].std()

fuentes = final_df["Fuente"].value_counts()

# ==========================================================
# IMPRIMIR ESTADISTICAS PRO
# ==========================================================

print("\n" + "="*70)
print("               ESTADISTICAS PROFESIONALES")
print("="*70)

print(f"\nTotal registros: {total}")

print(f"Promedio popularidad: {promedio:.2f}")

print(f"Máxima popularidad: {maximo}")

print(f"Mínima popularidad: {minimo}")

print(f"Mediana: {mediana}")

print(f"Desviación estándar: {desviacion:.2f}")

print("\nDistribución de fuentes:")
print(fuentes)

# ==========================================================
# TOP 15
# ==========================================================

top15 = final_df.sort_values(
    by="Popularidad",
    ascending=False
).head(15)

print("\nTOP 15 MÁS POPULARES")
print(top15[[
    "Titulo",
    "Fuente",
    "Popularidad"
]])

# ==========================================================
# FIGURA MASTER
# ==========================================================

fig = plt.figure(
    figsize=(22, 14)
)

fig.suptitle(
    "DASHBOARD PROFESIONAL APIs + OpenRefine",
    fontsize=28,
    fontweight='bold'
)

# ==========================================================
# GRAFICA 1
# ==========================================================

ax1 = plt.subplot2grid((2,2), (0,0))

colors = cm.plasma(
    np.linspace(0, 1, len(top15))
)

ax1.barh(
    top15["Titulo"],
    top15["Popularidad"],
    color=colors
)

ax1.invert_yaxis()

ax1.set_title(
    "TOP 15 MÁS POPULARES",
    fontsize=18,
    fontweight='bold'
)

ax1.grid(alpha=0.3)

# ==========================================================
# GRAFICA 2
# ==========================================================

ax2 = plt.subplot2grid((2,2), (0,1))

ax2.pie(
    fuentes,
    labels=fuentes.index,
    autopct='%1.1f%%',
    startangle=90
)

ax2.set_title(
    "DISTRIBUCIÓN DE FUENTES",
    fontsize=18,
    fontweight='bold'
)

# ==========================================================
# GRAFICA 3
# ==========================================================

ax3 = plt.subplot2grid((2,2), (1,0), colspan=2)

ax3.hist(
    final_df["Popularidad"],
    bins=20
)

ax3.set_title(
    "DISTRIBUCIÓN DE POPULARIDAD",
    fontsize=18,
    fontweight='bold'
)

ax3.set_xlabel("Popularidad")

ax3.set_ylabel("Frecuencia")

ax3.grid(alpha=0.3)

# ==========================================================
# AJUSTE
# ==========================================================

plt.tight_layout()

# ==========================================================
# GUARDAR IMAGEN
# ==========================================================

plt.savefig(
    "dashboard_profesional.png",
    dpi=300,
    bbox_inches='tight'
)

# ==========================================================
# MOSTRAR DASHBOARD EN PANTALLA
# ==========================================================

plt.show()

# ==========================================================
# EXPORTAR CSV
# ==========================================================

final_df.to_csv(
    "dataset_final.csv",
    index=False
)

top15.to_csv(
    "top15.csv",
    index=False
)

# ==========================================================
# FINAL
# ==========================================================

print("\n" + "="*70)
print("ARCHIVOS GENERADOS")
print("="*70)

print("\n✔ dataset_final.csv")
print("✔ top15.csv")
print("✔ dashboard_profesional.png")

print("\nDASHBOARD MOSTRADO EN PANTALLA")
print("="*70)
