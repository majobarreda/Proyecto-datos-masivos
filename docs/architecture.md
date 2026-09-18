# Arquitectura

## Diagrama general

```
Fuentes
  Kaggle (clima, descarga manual)
  Open-Meteo Air Quality API (código, src/ingestion/obtener_calidad_aire.py)
  INEGI - Estadísticas de Defunciones Registradas (mortalidad, descarga manual)
        |
        v
Adquisición (src/ingestion/)
        |
        v
Datos crudos (data/raw/): clima, contaminantes por ciudad, defunciones por año
        |
        v
Procesamiento (src/processing/)
  - procesamiento.py                    -> une clima + aire de las 20 ciudades (fase previa)
  - procesar_mortalidad_inegi.py         -> filtra CDMX, clasifica CIE-10, agrega conteo diario
  - construir_panel_cdmx.py              -> filtra CDMX de clima+aire, une con mortalidad,
                                             crea variables rezagadas (lag 0-14 días)
        |
        v
Datos preparados
  data/CDMX_mortalidad_diaria.csv
  data/CDMX_panel_diario.csv
        |
        v
Análisis (src/analysis/analisis_rezago.py)
  - Correlación cruzada (Spearman) por variable, desenlace y rezago
  - Identificación del rezago con mayor asociación por combinación
  - (Siguiente etapa) regresión Poisson/quasi-Poisson con términos rezagados
        |
        v
Resultados (reports/tables/, reports/figures/)
```

## Dónde se almacenan los datos

- `data/raw/`: archivos originales sin modificar (CSV de Kaggle, CSV anuales de INEGI). No se versionan en GitHub por su tamaño; el README documenta cómo obtenerlos.
- `data/`: en esta fase intermedia, los datasets ya agregados (por ciudad-día o CDMX-día) se mantienen en la raíz de `data/` para mantener compatibilidad con el trabajo ya construido (`LA_clima_y_aire_procesado.csv`, `CDMX_clima_y_aire_procesado.csv`). La migración a la estructura `raw/ → interim/ → processed/` completa se hará en el segundo parcial.
- `reports/tables/` y `reports/figures/`: salidas del análisis (tablas de correlación por rezago, gráficas).

## Cómo se obtienen

- **Clima:** descarga manual del CSV de Kaggle (ver README).
- **Contaminantes:** `python -m src.ingestion.obtener_calidad_aire`, vía Open-Meteo Air Quality API (sin credenciales).
- **Mortalidad:** descarga manual de los microdatos anuales de INEGI (EDR) desde `https://www.inegi.org.mx/programas/mortalidad/?ps=microdatos`, guardados como `data/raw/defunciones_<año>.csv`. No existe una URL de descarga directa estable por año (el portal requiere navegar el catálogo), por lo que —igual que con Kaggle— se documenta como descarga pública en vez de automatizarse por código.

## Transformaciones necesarias

1. Filtrar clima y aire a la ciudad de interés (`city == "Mexico City"`).
2. Filtrar mortalidad a la entidad de ocurrencia 09 (Ciudad de México) y clasificar la causa básica de defunción (`causa_def`) en capítulos CIE-10: respiratorio (J00–J99) y cardiovascular (I00–I99).
3. Construir la fecha de defunción a partir de año/mes/día y agregar conteos diarios por categoría de causa.
4. Unir clima+aire con mortalidad por fecha.
5. Generar variables rezagadas (lag 0 a 14 días) de cada variable de exposición.

## Herramientas consideradas

- `pandas` para todas las transformaciones (volumen manejable a nivel diario de una sola ciudad).
- `requests` para la API de Open-Meteo.
- Sin necesidad, por ahora, de herramientas distribuidas (Spark/Dask): el panel final es de a lo sumo unos cuantos miles de filas (una por día).

## Qué podría dejar de funcionar al crecer el volumen

- Los microdatos de INEGI son nacionales (varios millones de registros por año); si en el futuro se analizan múltiples entidades o rangos de años más amplios, leer los CSV completos con `pandas.read_csv` sin filtrar por chunks podría agotar memoria. La solución prevista es filtrar por `entidad_ocurr` usando lectura por bloques (`chunksize`) o `duckdb`/`polars` antes de cargar todo en memoria.
- Si se agrega la fuente SIMAT/RAMA (mediciones por estación, ver `docs/decisions.md`), el volumen horario por estación desde 1986 es considerablemente mayor que el de Open-Meteo agregado; requeriría una etapa de agregación por estación antes de unir con el resto del panel.
