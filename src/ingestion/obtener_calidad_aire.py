import requests
import pandas as pd

URL_API = "https://air-quality-api.open-meteo.com/v1/air-quality"

df_clima = pd.read_csv("data/LA_daily_climate.csv")

# Limpieza preventiva de espacios en blanco
df_clima['city'] = df_clima['city'].astype(str).str.strip()
df_clima['country'] = df_clima['country'].astype(str).str.strip()

# Obtener las ciudades del dataset
ciudades = (
    df_clima[
        ["city", "country", "latitude", "longitude"]
    ]
    .drop_duplicates()
    .reset_index(drop=True)
)

print("Ciudades encontradas:")
print(ciudades)

print("\nNúmero de ciudades:")
print(len(ciudades))

# Definir periodo
fecha_inicio = "2023-01-01"
fecha_fin = "2024-04-20"

columnas_contaminantes = [
    "pm10",
    "pm2_5",
    "carbon_monoxide",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "ozone"
]

resultados = []

# Consultar la API para cada ciudad
for _, fila in ciudades.iterrows():

    ciudad = fila["city"]
    pais = fila["country"]
    latitud = fila["latitude"]
    longitud = fila["longitude"]

    print(f"\nConsultando: {ciudad}, {pais}")

    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "hourly": (
            "pm10,"
            "pm2_5,"
            "carbon_monoxide,"
            "nitrogen_dioxide,"
            "sulphur_dioxide,"
            "ozone"
        ),
        "start_date": fecha_inicio,
        "end_date": fecha_fin,
        "timezone": "GMT",
        "domains": "cams_global"
    }

    respuesta = requests.get(
        URL_API,
        params=parametros,
        timeout=60
    )

    respuesta.raise_for_status()

    datos = respuesta.json()

    df_aire = pd.DataFrame(datos["hourly"])

    # Agregar información de la ciudad
    df_aire["city"] = ciudad
    df_aire["country"] = pais
    df_aire["latitude"] = latitud
    df_aire["longitude"] = longitud

    # Convertir contaminantes a números
    for columna in columnas_contaminantes:
        df_aire[columna] = pd.to_numeric(
            df_aire[columna],
            errors="coerce"
        )

    # Convertir fecha y hora
    df_aire["time"] = pd.to_datetime(
        df_aire["time"]
    )

    # Crear una columna con solo la fecha
    df_aire["date"] = df_aire["time"].dt.date

    # Obtener el promedio diario
    df_diario = (
        df_aire
        .groupby(
            [
                "date",
                "city",
                "country",
                "latitude",
                "longitude"
            ],
            as_index=False
        )[columnas_contaminantes]
        .mean()
    )

    resultados.append(df_diario)

# Unir los resultados de todas las ciudades
df_aire_completo = pd.concat(
    resultados,
    ignore_index=True
)

df_aire_completo["date"] = pd.to_datetime(
    df_aire_completo["date"]
)

df_aire_completo = (
    df_aire_completo
    .sort_values(["city", "date"])
    .reset_index(drop=True)
)

# Revisar los datos obtenidos
print("\n========================================")
print("EXTRACCIÓN COMPLETADA")
print("========================================")

print("\nPrimeras filas:")
print(df_aire_completo.head())

print("\nDimensiones:")
print(df_aire_completo.shape)

print("\nTipos de datos:")
print(df_aire_completo.dtypes)

print("\nValores faltantes:")
print(df_aire_completo.isna().sum())

print("\nNúmero de ciudades:")
print(df_aire_completo["city"].nunique())

print("\nFecha inicial:")
print(df_aire_completo["date"].min())

print("\nFecha final:")
print(df_aire_completo["date"].max())

print("\nDuplicados:")
print(
    df_aire_completo.duplicated(
        subset=["date", "city"]
    ).sum()
)

# Guardar el dataset
ruta_salida = "data/LA_daily_air_quality.csv"

df_aire_completo.to_csv(
    ruta_salida,
    index=False
)

print(f"\nDataset guardado en: {ruta_salida}")

