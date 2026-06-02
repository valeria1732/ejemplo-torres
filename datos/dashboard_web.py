import requests
import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# =========================================================
# FUNCIÓN DE ESTILO
# =========================================================

def card_style(color):
    return {
        "backgroundColor": "#161b22",
        "padding": "20px",
        "borderRadius": "15px",
        "width": "22%",
        "textAlign": "center",
        "boxShadow": f"0px 0px 15px {color}",
        "color": "white"
    }

# =========================================================
# INICIO
# =========================================================

print("🚀 Iniciando dashboard...")

# =========================================================
# GITHUB API
# =========================================================

github_repos = []

try:
    print("📡 GitHub...")

    github_url = "https://api.github.com/search/repositories?q=AI&sort=stars"
    github_data = requests.get(github_url, timeout=10).json()

    for repo in github_data.get("items", [])[:40]:
        github_repos.append({
            "Titulo": repo.get("name", "N/A"),
            "Fuente": "GitHub",
            "Popularidad": repo.get("stargazers_count", 0),
        })

except Exception as e:
    print("❌ GitHub error:", e)

github_df = pd.DataFrame(github_repos)

# =========================================================
# HACKER NEWS API
# =========================================================

news = []

try:
    print("📰 HackerNews...")

    top = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json",
        timeout=10
    ).json()

    for story_id in top[:40]:
        try:
            story = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                timeout=10
            ).json()

            if story and story.get("title"):
                news.append({
                    "Titulo": story.get("title"),
                    "Fuente": "HackerNews",
                    "Popularidad": story.get("score", 0),
                })
        except:
            continue

except Exception as e:
    print("❌ HackerNews error:", e)

news_df = pd.DataFrame(news)

# =========================================================
# DATASET FINAL
# =========================================================

final_df = pd.concat([github_df, news_df], ignore_index=True)

# 🔥 EVITAR ERRORES DE GRAFICAS
if final_df.empty:
    final_df = pd.DataFrame({
        "Titulo": ["Sin datos"],
        "Fuente": ["N/A"],
        "Popularidad": [0]
    })

final_df["Popularidad"] = pd.to_numeric(final_df["Popularidad"], errors="coerce")
final_df.dropna(inplace=True)

# =========================================================
# ESTADÍSTICAS
# =========================================================

total = len(final_df)
promedio = round(final_df["Popularidad"].mean(), 2)
maximo = final_df["Popularidad"].max()
minimo = final_df["Popularidad"].min()

# =========================================================
# TOP 15
# =========================================================

top15 = final_df.sort_values(by="Popularidad", ascending=False).head(15)

# =========================================================
# GRÁFICAS
# =========================================================

fig_bar = px.bar(
    top15,
    x="Popularidad",
    y="Titulo",
    color="Fuente",
    orientation="h",
    title="🔥 TOP 15 MÁS POPULARES"
)

fig_bar.update_layout(template="plotly_dark", yaxis=dict(autorange="reversed"))

fig_pie = px.pie(
    final_df,
    names="Fuente",
    title="📊 DISTRIBUCIÓN DE FUENTES"
)

fig_pie.update_layout(template="plotly_dark")

fig_hist = px.histogram(
    final_df,
    x="Popularidad",
    nbins=20,
    title="📈 DISTRIBUCIÓN DE POPULARIDAD"
)

fig_hist.update_layout(template="plotly_dark")

# =========================================================
# DASH APP
# =========================================================

app = Dash(__name__)

app.layout = html.Div(
    style={
        "backgroundColor": "#0d1117",
        "padding": "20px",
        "fontFamily": "Arial"
    },
    children=[

        html.H1(
            "🚀 DASHBOARD PROFESIONAL APIs",
            style={"textAlign": "center", "color": "white"}
        ),

        # ================= TARJETAS =================
        html.Div(
            style={"display": "flex", "justifyContent": "space-between"},
            children=[

                html.Div([
                    html.H3("TOTAL"),
                    html.H2(total)
                ], style=card_style("#58a6ff")),

                html.Div([
                    html.H3("PROMEDIO"),
                    html.H2(promedio)
                ], style=card_style("#3fb950")),

                html.Div([
                    html.H3("MÁXIMO"),
                    html.H2(maximo)
                ], style=card_style("#d29922")),

                html.Div([
                    html.H3("MÍNIMO"),
                    html.H2(minimo)
                ], style=card_style("#f85149"))

            ]
        ),

        html.Br(),

        # ================= GRÁFICAS =================
        dcc.Graph(figure=fig_bar),

        html.Div(
            style={"display": "flex"},
            children=[
                html.Div(dcc.Graph(figure=fig_pie), style={"width": "50%"}),
                html.Div(dcc.Graph(figure=fig_hist), style={"width": "50%"})
            ]
        )
    ]
)

# =========================================================
# EXPORTAR CSV
# =========================================================

final_df.to_csv("dataset_final.csv", index=False)
top15.to_csv("top15.csv", index=False)

# =========================================================
# EJECUCIÓN FINAL (ARREGLADA)
# =========================================================

print("\n🌐 Dashboard listo en: http://127.0.0.1:8050")

app.run(debug=False, host="127.0.0.1", port=8050)