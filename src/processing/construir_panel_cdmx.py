# src/processing/construir_panel_cdmx.py
"""
Construye el panel diario de la Ciudad de Mexico que integra clima,
contaminantes y mortalidad, y agrega variables rezagadas (lag) de cada
variable de exposicion.

Requiere haber generado antes:
    data/LA_clima_y_aire_procesado.csv   (src/procesamiento.py)
    data/CDMX_mortalidad_diaria.csv      (src/processing/procesar_mortalidad_inegi.py)

Uso:
    python -m src.processing.construir_panel_cdmx
"""
import pandas as pd

CIUDAD = "Mexico City"

RUTA_CLIMA_AIRE = "data/LA_clima_y_aire_procesado.csv"
RUTA_MORTALIDAD = "data/CDMX_mortalidad_diaria.csv"
RUTA_SALIDA = "data/CDMX_panel_diario.csv"

VARIABLES_EXPOSICION = [
    "temperature_2m_mean",
    "apparent_temperature_mean",
    "precipitation_sum",
    "wind_speed_10m_max",
    "pm10",
    "pm2_5",
    "carbon_monoxide",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "ozone",
]

REZAGOS_DIAS = range(0, 15)  # 0 a 14 dias


def cargar_clima_aire_cdmx():
    df = pd.read_csv(RUTA_CLIMA_AIRE)
    df = df[df["city"] == CIUDAD].copy()
    df["fecha"] = pd.to_datetime(df["date"]).dt.tz_localize(None).dt.normalize()
    return df.drop(columns=["date"])


def cargar_mortalidad():
    return pd.read_csv(RUTA_MORTALIDAD, parse_dates=["fecha"])


def agregar_rezagos(df):
    df = df.sort_values("fecha").reset_index(drop=True)
    for variable in VARIABLES_EXPOSICION:
        if variable not in df.columns:
            continue
        for rezago in REZAGOS_DIAS:
            df[f"{variable}_lag{rezago}"] = df[variable].shift(rezago)
    return df


def main():
    clima_aire = cargar_clima_aire_cdmx()
    mortalidad = cargar_mortalidad()

    panel = pd.merge(clima_aire, mortalidad, on="fecha", how="inner")
    panel = agregar_rezagos(panel)

    columnas_clave = VARIABLES_EXPOSICION + [
        "defunciones_totales",
        "respiratoria",
        "cardiovascular",
    ]

    print("========================================")
    print("PANEL DIARIO DE CDMX CONSTRUIDO")
    print("========================================")
    print(f"\nDimensiones: {panel.shape}")
    print(f"Rango de fechas: {panel['fecha'].min()} a {panel['fecha'].max()}")
    print("\nValores faltantes (variables base):")
    print(panel[columnas_clave].isna().sum())
    print("\nDuplicados por fecha:")
    print(panel.duplicated(subset=["fecha"]).sum())

    panel.to_csv(RUTA_SALIDA, index=False)
    print(f"\nDataset guardado en: {RUTA_SALIDA}")


if __name__ == "__main__":
    main()
