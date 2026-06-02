import pandas as pd

# Leer dataset final
df = pd.read_csv("dataset_final.csv")

# Total de registros
total = len(df)

# Conteo por fuente
fuentes = df["Fuente"].value_counts()

# Crear dataframe
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

# Guardar CSV
estadisticas.to_csv("estadisticas.csv", index=False)

# Mostrar estadísticas
print(estadisticas)

print("Archivo estadisticas.csv creado")