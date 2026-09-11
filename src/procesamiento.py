# src/procesamiento.py
import pandas as pd

def cargar_y_limpiar_datos(ruta_clima="../data/LA_daily_climate.csv", ruta_aire="../data/LA_daily_air_quality.csv"):
    """Carga, limpia espacios en blanco y une los datasets de clima y aire."""
    df_clima = pd.read_csv(ruta_clima)
    df_aire = pd.read_csv(ruta_aire)

    # Limpieza de espacios en blanco en ambos DataFrames
    for df in [df_clima, df_aire]:
        for col in ['city', 'country']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()

    # Formato de fechas estandarizado a UTC
    df_clima['date'] = pd.to_datetime(df_clima['date'], utc=True)
    df_aire['date'] = pd.to_datetime(df_aire['date'], utc=True)

    # Cruce completo por fecha y ubicacion para evitar columnas duplicadas
    llaves_union = ['date', 'city', 'country', 'latitude', 'longitude']
    df_completo = pd.merge(
        df_clima,
        df_aire,
        on=llaves_union,
        how='inner'
    ).drop_duplicates()

    return df_completo
