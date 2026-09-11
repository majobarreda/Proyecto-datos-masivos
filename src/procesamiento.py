# src/procesamiento.py
import pandas as pd

def cargar_y_limpiar_datos(ruta_clima="../data/LA_daily_climate.csv", ruta_aire="../data/LA_daily_air_quality.csv"):
    """Carga, limpia espacios en blanco y une los datasets de clima y aire."""
    df_clima = pd.read_csv(ruta_clima)
    df_aire = pd.read_csv(ruta_aire)

    # Limpieza de espacios en cadenas de texto
    if 'city' in df_clima.columns:
        df_clima['city'] = df_clima['city'].astype(str).str.strip()
    if 'country' in df_clima.columns:
        df_clima['country'] = df_clima['country'].astype(str).str.strip()

    # Formato de fechas
    df_clima['date'] = pd.to_datetime(df_clima['date'])
    df_aire['date'] = pd.to_datetime(df_aire['date'])

    # Cruce masivo
    df_completo = pd.merge(df_clima, df_aire, on='date', how='inner', suffixes=('_clima', '_aire')).drop_duplicates()
    return df_completo

def obtener_promedios_por_ciudad(df):
    """Calcula los promedios de temperatura y contaminantes principales por ciudad."""
    columnas_interes = ['temperature_2m_mean', 'pm10', 'pm2_5', 'carbon_monoxide', 'nitrogen_dioxide']
    columnas_presentes = [col for col in columnas_interes if col in df.columns]
    return df.groupby('city')[columnas_presentes].mean()
