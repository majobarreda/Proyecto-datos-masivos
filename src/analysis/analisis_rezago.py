# src/analysis/analisis_rezago.py
"""
Analisis exploratorio de correlacion cruzada (CCF) entre variables de
exposicion (clima y contaminantes, con sus versiones rezagadas) y los
desenlaces de mortalidad diaria en la Ciudad de Mexico.

Requiere haber generado antes:
    data/CDMX_panel_diario.csv   (src/processing/construir_panel_cdmx.py)

Uso:
    python -m src.analysis.analisis_rezago
"""
import pandas as pd

RUTA_PANEL = "data/CDMX_panel_diario.csv"
RUTA_TABLA_COMPLETA = "reports/tables/correlaciones_por_rezago.csv"
RUTA_TABLA_RESUMEN = "reports/tables/mejor_rezago_por_variable.csv"

DESENLACES = ["respiratoria", "cardiovascular", "defunciones_totales"]

VARIABLES_BASE = [
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

REZAGOS_DIAS = range(0, 15)
MINIMO_OBSERVACIONES = 10


def calcular_correlaciones_por_rezago(panel):
    """Para cada variable de exposicion, cada rezago y cada desenlace,
    calcula la correlacion de Spearman entre la variable rezagada y el
    desenlace del dia."""
    filas = []
    for variable in VARIABLES_BASE:
        for rezago in REZAGOS_DIAS:
            columna_rezagada = f"{variable}_lag{rezago}"
            if columna_rezagada not in panel.columns:
                continue
            for desenlace in DESENLACES:
                datos = panel[[columna_rezagada, desenlace]].dropna()
                if len(datos) < MINIMO_OBSERVACIONES:
                    continue
                r = datos[columna_rezagada].corr(datos[desenlace], method="spearman")
                filas.append(
                    {
                        "variable": variable,
                        "rezago_dias": rezago,
                        "desenlace": desenlace,
                        "correlacion_spearman": r,
                        "n_observaciones": len(datos),
                    }
                )
    return pd.DataFrame(filas)


def mejor_rezago_por_variable(tabla_correlaciones):
    """Para cada combinacion variable-desenlace, identifica el rezago con la
    correlacion mas fuerte en valor absoluto (candidato a senal temprana)."""
    tabla = tabla_correlaciones.copy()
    tabla["abs_correlacion"] = tabla["correlacion_spearman"].abs()
    indices = tabla.groupby(["variable", "desenlace"])["abs_correlacion"].idxmax()
    return (
        tabla.loc[indices]
        .drop(columns="abs_correlacion")
        .sort_values("correlacion_spearman", ascending=False)
        .reset_index(drop=True)
    )


def main():
    panel = pd.read_csv(RUTA_PANEL, parse_dates=["fecha"])

    tabla_correlaciones = calcular_correlaciones_por_rezago(panel)
    resumen = mejor_rezago_por_variable(tabla_correlaciones)

    print("========================================")
    print("REZAGO CON MAYOR ASOCIACION POR VARIABLE Y DESENLACE")
    print("========================================")
    print(resumen.to_string(index=False))

    tabla_correlaciones.to_csv(RUTA_TABLA_COMPLETA, index=False)
    resumen.to_csv(RUTA_TABLA_RESUMEN, index=False)

    print(f"\nTabla completa guardada en: {RUTA_TABLA_COMPLETA}")
    print(f"Tabla resumen guardada en: {RUTA_TABLA_RESUMEN}")


if __name__ == "__main__":
    main()
