# Diccionario de datos

Este diccionario cubre las tres fuentes usadas en la etapa de análisis de mortalidad de la Ciudad de México, y el panel diario resultante de integrarlas. Para el detalle completo de las 20 ciudades de Latinoamérica (fase exploratoria previa), ver el README.

## 1. Clima y contaminantes — `data/CDMX_clima_y_aire_procesado.csv` (filtrado de `data/LA_clima_y_aire_procesado.csv`)

| Variable | Tipo | Descripción | Unidad | Valores faltantes | Observaciones |
|---|---|---|---|---|---|
| `date` / `fecha` | datetime | Día calendario (UTC) | — | 0% | Llave de unión con mortalidad |
| `city`, `country` | string | Ciudad y país (`Mexico City`, `Mexico`) | — | 0% | Filtrado a una sola ciudad en esta etapa |
| `temperature_2m_mean` | float | Temperatura media diaria a 2 m | °C | 0% | Fuente: Kaggle |
| `apparent_temperature_mean` | float | Sensación térmica media diaria | °C | 0% | Fuente: Kaggle |
| `precipitation_sum` | float | Precipitación acumulada del día | mm | 0% | Fuente: Kaggle |
| `wind_speed_10m_max` | float | Velocidad máxima del viento a 10 m | km/h | 0% | Fuente: Kaggle |
| `pm10` | float | Material particulado ≤ 10 µm (promedio diario) | µg/m³ | 0% en 2023-01 – 2024-04 | Fuente: Open-Meteo Air Quality API |
| `pm2_5` | float | Material particulado ≤ 2.5 µm (promedio diario) | µg/m³ | 0% en 2023-01 – 2024-04 | Fuente: Open-Meteo Air Quality API |
| `carbon_monoxide` | float | Monóxido de carbono (CO) | µg/m³ | 0% | Fuente: Open-Meteo Air Quality API |
| `nitrogen_dioxide` | float | Dióxido de nitrógeno (NO₂) | µg/m³ | 0% | Fuente: Open-Meteo Air Quality API |
| `sulphur_dioxide` | float | Dióxido de azufre (SO₂) | µg/m³ | 0% | Fuente: Open-Meteo Air Quality API |
| `ozone` | float | Ozono (O₃) | µg/m³ | 0% | Fuente: Open-Meteo Air Quality API |

## 2. Mortalidad diaria — `data/CDMX_mortalidad_diaria.csv` (generado por `src/processing/procesar_mortalidad_inegi.py`)

Fuente: INEGI, microdatos de "Estadísticas de Defunciones Registradas" (EDR), filtrados a `entidad de ocurrencia = 09` (Ciudad de México) y agregados por día.

| Variable | Tipo | Descripción | Unidad | Valores faltantes | Observaciones |
|---|---|---|---|---|---|
| `fecha` | date | Día de ocurrencia de la defunción | — | Se descartan registros con día/mes no especificado (código 99 de INEGI) | Construida a partir de `anio_ocur` + `mes_ocurr` + `dia_ocurr` |
| `respiratoria` | int | Defunciones cuya causa básica cae en el capítulo CIE-10 J00–J99 | conteo | 0% | Enfermedades del sistema respiratorio |
| `cardiovascular` | int | Defunciones cuya causa básica cae en el capítulo CIE-10 I00–I99 | conteo | 0% | Enfermedades del sistema circulatorio |
| `otra` | int | Defunciones con causa fuera de los dos capítulos anteriores | conteo | 0% | Se conserva como referencia / control |
| `defunciones_totales` | int | Suma de las tres categorías anteriores | conteo | 0% | Útil para modelos que requieren un denominador |

**Variables crudas relevantes en el microdato original de INEGI** (nombres pueden variar ligeramente entre años):

| Variable cruda | Descripción |
|---|---|
| `ent_ocurr` | Clave de entidad federativa donde ocurrió la defunción (09 = Ciudad de México) |
| `anio_ocur`, `mes_ocurr`, `dia_ocurr` | Año, mes y día de ocurrencia de la defunción |
| `causa_def` | Causa básica de la defunción, código CIE-10 detallado |
| `sexo`, `edad` | Variables demográficas disponibles para análisis futuro (no usadas en esta primera versión) |

**Problemas conocidos:** el archivo se publica un año calendario a la vez (no hay API); el año más reciente puede tardar ~10–14 meses en publicarse; algunos registros no traen día/mes exacto y se excluyen de la serie diaria.

## 3. Panel diario integrado — `data/CDMX_panel_diario.csv` (generado por `src/processing/construir_panel_cdmx.py`)

| Variable | Tipo | Descripción |
|---|---|---|
| `fecha` | date | Llave de unión de las tres fuentes |
| Todas las columnas de la sección 1 | float | Variables de exposición del día `t` |
| `<variable>_lag{0..14}` | float | Valor de cada variable de exposición `n` días antes (0 = mismo día) |
| `respiratoria`, `cardiovascular`, `otra`, `defunciones_totales` | int | Desenlaces del día `t` (sección 2) |

Este panel es la entrada del análisis de correlación por rezago (`src/analysis/analisis_rezago.py`).
