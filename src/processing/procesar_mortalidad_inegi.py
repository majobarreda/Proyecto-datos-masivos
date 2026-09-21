# src/processing/procesar_mortalidad_inegi.py
"""
Procesa los microdatos anuales de "Estadisticas de Defunciones Registradas"
(EDR) del INEGI y construye un conteo diario de defunciones de la Ciudad de
Mexico por grupo de causa (respiratoria, cardiovascular, otra).

Los microdatos se descargan manualmente (no existe una URL de descarga
directa estable por anio) desde:
    https://www.inegi.org.mx/programas/edr/#microdatos
Un archivo por anio, en formato DBF (el que distribuye INEGI) o CSV, por
ejemplo:
    data/raw/defunciones_2023.dbf
    data/raw/defunciones_2024.dbf

Uso:
    python -m src.processing.procesar_mortalidad_inegi data/raw/defunciones_2023.dbf data/raw/defunciones_2024.dbf
"""
import sys
from pathlib import Path

import pandas as pd
from dbfread import DBF

CLAVE_ENTIDAD_CDMX = 9  # Ciudad de Mexico en el catalogo de entidades de INEGI

RUTA_SALIDA = "data/CDMX_mortalidad_diaria.csv"

# INEGI ha usado nombres de columna ligeramente distintos entre anios de la EDR.
CANDIDATOS_COLUMNAS = {
    "entidad_ocurrencia": ["ent_ocurr", "ent_ocur", "entidad_ocurr"],
    "anio": ["anio_ocur", "anio_ocurr"],
    "mes": ["mes_ocurr"],
    "dia": ["dia_ocurr"],
    "causa": ["causa_def", "causa_defu"],
}


def _resolver_columna(df, candidatos):
    for nombre in candidatos:
        if nombre in df.columns:
            return nombre
    raise ValueError(
        f"Ninguna de las columnas esperadas {candidatos} existe en el archivo. "
        f"Columnas disponibles: {list(df.columns)}"
    )


def clasificar_causa(codigo_cie10):
    """Agrupa un codigo CIE-10 de causa basica de defuncion en capitulo
    respiratorio (J00-J99), cardiovascular (I00-I99) u otra causa."""
    if not isinstance(codigo_cie10, str) or len(codigo_cie10) < 3:
        return "otra"

    capitulo = codigo_cie10[0].upper()
    numero = codigo_cie10[1:3]

    if not numero.isdigit():
        return "otra"

    if capitulo == "J":
        return "respiratoria"
    if capitulo == "I":
        return "cardiovascular"
    return "otra"


def cargar_defunciones(ruta):
    """Carga un archivo de defunciones de INEGI, ya sea en formato DBF
    (el que distribuye INEGI) o CSV, segun la extension del archivo."""
    extension = Path(ruta).suffix.lower()

    if extension == ".dbf":
        tabla = DBF(ruta, encoding="latin-1", ignore_missing_memofile=True)
        return pd.DataFrame(iter(tabla))

    return pd.read_csv(ruta, low_memory=False)


def procesar_archivo(ruta_csv):
    df = cargar_defunciones(ruta_csv)
    df.columns = df.columns.str.lower()  # DBF suele traer los nombres en mayusculas

    col_entidad = _resolver_columna(df, CANDIDATOS_COLUMNAS["entidad_ocurrencia"])
    col_anio = _resolver_columna(df, CANDIDATOS_COLUMNAS["anio"])
    col_mes = _resolver_columna(df, CANDIDATOS_COLUMNAS["mes"])
    col_dia = _resolver_columna(df, CANDIDATOS_COLUMNAS["dia"])
    col_causa = _resolver_columna(df, CANDIDATOS_COLUMNAS["causa"])

    df[col_entidad] = pd.to_numeric(df[col_entidad], errors="coerce")
    df_cdmx = df[df[col_entidad] == CLAVE_ENTIDAD_CDMX].copy()

    df_cdmx["fecha"] = pd.to_datetime(
        dict(
            year=pd.to_numeric(df_cdmx[col_anio], errors="coerce"),
            month=pd.to_numeric(df_cdmx[col_mes], errors="coerce"),
            day=pd.to_numeric(df_cdmx[col_dia], errors="coerce"),
        ),
        errors="coerce",
    )

    filas_sin_fecha = int(df_cdmx["fecha"].isna().sum())
    if filas_sin_fecha:
        print(
            f"Aviso: {filas_sin_fecha} defunciones sin fecha valida "
            "(dia/mes no especificado) se excluyen de la serie diaria."
        )
    df_cdmx = df_cdmx.dropna(subset=["fecha"])

    df_cdmx["grupo_causa"] = df_cdmx[col_causa].astype(str).apply(clasificar_causa)

    conteo_diario = (
        df_cdmx.groupby(["fecha", "grupo_causa"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=["respiratoria", "cardiovascular", "otra"], fill_value=0)
    )
    conteo_diario["defunciones_totales"] = conteo_diario.sum(axis=1)

    return conteo_diario.reset_index()


def main(rutas_csv):
    tablas = [procesar_archivo(ruta) for ruta in rutas_csv]
    resultado = (
        pd.concat(tablas, ignore_index=True)
        .groupby("fecha", as_index=False)
        .sum()
        .sort_values("fecha")
    )

    print("========================================")
    print("PROCESAMIENTO DE MORTALIDAD COMPLETADO")
    print("========================================")
    print(f"\nDimensiones: {resultado.shape}")
    print(f"Rango de fechas: {resultado['fecha'].min()} a {resultado['fecha'].max()}")
    print("\nPrimeras filas:")
    print(resultado.head())
    print("\nDuplicados por fecha:")
    print(resultado.duplicated(subset=["fecha"]).sum())

    resultado.to_csv(RUTA_SALIDA, index=False)
    print(f"\nDataset guardado en: {RUTA_SALIDA}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(
            "Uso: python -m src.processing.procesar_mortalidad_inegi "
            "<ruta_archivo_anio_1> [<ruta_archivo_anio_2> ...]"
        )
    main(sys.argv[1:])
