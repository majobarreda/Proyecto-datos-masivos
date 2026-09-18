# Clima, contaminación y mortalidad respiratoria/cardiovascular en la Ciudad de México

Proyecto semestral del curso de Datos Masivos. Integra un dataset climático diario de Kaggle, datos de calidad del aire obtenidos mediante la Open-Meteo Air Quality API y microdatos de mortalidad de INEGI, para analizar con qué rezago (lag) las condiciones meteorológicas y los contaminantes de la Ciudad de México se asocian con incrementos en la mortalidad diaria por causas respiratorias y cardiovasculares.

---

## Evolución del proyecto

El proyecto inició como una comparación descriptiva de clima y calidad del aire en **20 ciudades de Latinoamérica** (esa fase se conserva íntegra en este README y en `notebooks/`, como antecedente). A partir de esta entrega, la pregunta se acota a la **Ciudad de México** y se agrega una tercera fuente —mortalidad diaria por causa (INEGI)— para pasar de una pregunta comparativa a una pregunta de salud ambiental con rezago temporal. El detalle completo de este cambio de alcance está documentado en `docs/decisions.md` y `docs/project_scope.md`.

---

## Integrantes

<!-- COMPLETAR: nombre completo y usuario de GitHub de cada integrante -->

| Nombre | 
|---|
| María José Barreda | 
| Sofia Villegas | 
| Emiliano Martinez| 

---

## Problema

Las ciudades de Latinoamérica presentan diferencias importantes en sus condiciones meteorológicas debido a factores geográficos, climáticos y regionales.

Variables como la temperatura, la precipitación y la velocidad del viento influyen en la dispersión, acumulación y formación de contaminantes atmosféricos: la lluvia lava partículas suspendidas, el viento dispersa contaminantes y la radiación solar favorece la formación de ozono troposférico.

Sin embargo, la información meteorológica y la de calidad del aire se encuentra distribuida entre distintas fuentes, con diferentes formatos, escalas temporales y zonas horarias. Por esta razón es necesario un proceso de adquisición, limpieza e integración que permita relacionar ambos tipos de variables sobre una misma base temporal y geográfica.

---

## Pregunta principal

**¿Qué combinaciones de condiciones meteorológicas y niveles de contaminantes en la Ciudad de México, con qué rezago temporal (lag) respecto al evento, están más asociadas con incrementos en la mortalidad diaria por causas respiratorias y cardiovasculares, y qué patrones podrían usarse como señal temprana de días de mayor riesgo?**

> Pregunta original de la fase exploratoria (20 ciudades): *¿Qué relación existe entre las condiciones meteorológicas y los niveles de contaminación del aire en distintas ciudades de Latinoamérica?* Ver `docs/decisions.md` para el porqué del cambio de alcance.

### Preguntas secundarias

1. ¿En qué rezago (0 a 14 días) cada contaminante (PM2.5, PM10, O₃, NO₂, SO₂, CO) muestra la asociación más fuerte con la mortalidad respiratoria y con la cardiovascular?
2. ¿El efecto de la temperatura (calor y frío extremos) tiene un patrón de rezago distinto al de los contaminantes?
3. ¿Existen combinaciones de variables (p. ej. temperatura alta + ozono alto) cuya asociación conjunta con la mortalidad sea mayor que la de cada variable por separado?
4. ¿El rezago óptimo difiere entre mortalidad respiratoria y cardiovascular?
5. ¿Qué percentiles de exposición (p. ej. P90/P95 de PM2.5 u ozono) podrían usarse como umbral de una señal de alerta temprana?
6. ¿Los patrones encontrados se mantienen estables entre temporadas o cambian con la estacionalidad?

### ¿Qué representa una fila?

El dataset analítico final (`data/CDMX_panel_diario.csv`) representa **un día en la Ciudad de México**: las condiciones meteorológicas y los niveles promedio de contaminantes de ese día (y de los 14 días previos, como variables rezagadas), junto con el número de defunciones registradas ese día por causa respiratoria, cardiovascular y total.

La unidad de análisis es, por lo tanto, **Ciudad de México × día**. Detalle completo en `docs/project_scope.md`.

---

## Objetivo

Construir un panel diario reproducible para la Ciudad de México que integre clima, contaminantes y mortalidad por causa, y usarlo para identificar con qué rezago las condiciones ambientales se asocian con incrementos en la mortalidad respiratoria y cardiovascular.

Objetivos específicos:

- Obtener mediante código los datos de calidad del aire de la Open-Meteo Air Quality API.
- Procesar los microdatos anuales de mortalidad de INEGI para obtener conteos diarios de defunciones de la Ciudad de México por causa (respiratoria, cardiovascular, otra).
- Integrar las tres fuentes en un único panel diario validado, con variables rezagadas de 0 a 14 días.
- Identificar, mediante correlación cruzada, el rezago con mayor asociación entre cada variable de exposición y cada desenlace de mortalidad.

---

## Usuario o interesado

| Usuario | Decisión que podría tomar con esta información |
|---|---|
| Secretaría de Salud de la Ciudad de México / vigilancia epidemiológica | Anticipar días de mayor riesgo respiratorio o cardiovascular y reforzar capacidad hospitalaria o campañas de prevención. |
| Autoridades ambientales (SEDEMA) | Priorizar qué variable vigilar como señal temprana, más allá del índice de calidad del aire actual. |
| Población vulnerable (adultos mayores, personas con enfermedad crónica) | Ajustar su exposición en los días identificados como de mayor riesgo. |
| Investigadores y estudiantes | Usar el panel diario integrado como base para estudios de salud ambiental en la Ciudad de México. |

---

## Fuentes de datos

El proyecto utiliza **tres fuentes**: dos de descarga documentada y una obtenida mediante código.

### 1. Latin America Weather and Air Quality Data (Kaggle)

| Campo | Detalle |
|---|---|
| Origen | Kaggle — https://www.kaggle.com/datasets/anycaroliny/latin-america-weather-and-air-quality-data |
| Propietario | Usuario `anycaroliny` (dataset público) |
| Método de acceso | Descarga manual del archivo `LA_daily_climate.csv` |
| Formato | CSV |
| Volumen | 31,440 registros × 14 variables |
| Periodo disponible | 2020-01-01 a 2024-04-20 (1,572 fechas) |
| Cobertura | 20 ciudades, 20 países |
| Frecuencia de actualización | Estática (no se actualiza) |
| Restricciones de uso | Licencia abierta del dataset en Kaggle |
| Problemas conocidos | `date` viene como texto; posibles espacios en nombres de ciudad; no incluye variables de contaminación pese al nombre del dataset |

**Variables principales**

| Variable | Tipo | Descripción | Unidad |
|---|---|---|---|
| `country` | string | País | — |
| `city` | string | Ciudad | — |
| `date` | date | Fecha del registro | — |
| `latitude` / `longitude` | float | Coordenadas de la ciudad | grados |
| `temperature_2m_max` / `_min` / `_mean` | float | Temperatura a 2 m | °C |
| `apparent_temperature_max` / `_min` / `_mean` | float | Temperatura aparente | °C |
| `precipitation_sum` | float | Precipitación acumulada del día | mm |
| `wind_speed_10m_max` | float | Velocidad máxima del viento a 10 m | km/h |
| `et0_fao_evapotranspiration` | float | Evapotranspiración de referencia FAO | mm |

### 2. Open-Meteo Air Quality API

| Campo | Detalle |
|---|---|
| Origen | Open-Meteo — https://open-meteo.com/ |
| Propietario | Open-Meteo |
| Método de acceso | **Obtenida mediante código**: peticiones HTTP con `requests` desde `src/ingestion/` |
| Formato | JSON (respuesta) → CSV (almacenamiento) |
| Granularidad original | Horaria |
| Periodo extraído | 2023-01-01 a 2024-04-20 |
| Cobertura | Las mismas 20 ciudades, consultadas por coordenadas |
| Credenciales | **No requiere API key** para uso no comercial |
| Restricciones de uso | Límite de peticiones diarias en el plan gratuito; uso no comercial |
| Problemas conocidos | Valores faltantes en algunos contaminantes para consultas de 2022 |

**Variables principales**

| Variable | Tipo | Descripción | Unidad |
|---|---|---|---|
| `pm10` | float | Material particulado ≤ 10 µm | µg/m³ |
| `pm2_5` | float | Material particulado ≤ 2.5 µm | µg/m³ |
| `carbon_monoxide` | float | Monóxido de carbono (CO) | µg/m³ |
| `nitrogen_dioxide` | float | Dióxido de nitrógeno (NO₂) | µg/m³ |
| `sulphur_dioxide` | float | Dióxido de azufre (SO₂) | µg/m³ |
| `ozone` | float | Ozono (O₃) | µg/m³ |

#### Definición del periodo de análisis

El dataset de Kaggle contiene información desde 2020, pero para la calidad del aire se trabajó con el periodo que podía obtenerse de manera consistente mediante la API.

Durante las pruebas de extracción se detectó que en consultas correspondientes a 2022 aparecían valores faltantes en los contaminantes. Por esa razón el análisis se limitó al periodo **2023-01-01 – 2024-04-20**, donde la extracción devolvió las 20 ciudades sin valores faltantes. La fecha final corresponde al último registro disponible en el dataset de Kaggle.

### 3. Estadísticas de Defunciones Registradas — INEGI

| Campo | Detalle |
|---|---|
| Origen | INEGI — https://www.inegi.org.mx/programas/mortalidad/?ps=microdatos |
| Propietario | INEGI (información pública) |
| Método de acceso | Descarga manual de microdatos anuales (no hay URL estable de descarga directa por año) |
| Formato | CSV, un archivo por año |
| Volumen aproximado | Cientos de miles de registros nacionales por año; unos cuantos miles corresponden a la Ciudad de México |
| Periodo disponible | Serie anual 1990–2024 (el año más reciente se publica con ~10–14 meses de rezago) |
| Frecuencia de actualización | Anual |
| Restricciones de uso | Información pública de INEGI, sin restricción de uso no comercial |
| Problemas conocidos | Nombres de columna ligeramente distintos entre años; algunos registros no traen día/mes exacto de defunción |

**Variables principales usadas**

| Variable | Tipo | Descripción | Observaciones |
|---|---|---|---|
| `ent_ocurr` | int | Entidad federativa de ocurrencia de la defunción | Se filtra a `09` (Ciudad de México) |
| `anio_ocur`, `mes_ocurr`, `dia_ocurr` | int | Año, mes y día de ocurrencia | Se combinan en una fecha |
| `causa_def` | string | Causa básica de defunción, código CIE-10 | Se agrupa en respiratoria (J00–J99), cardiovascular (I00–I99) u otra |

El procesamiento de esta fuente se documenta en `docs/data_dictionary.md` y se implementa en `src/processing/procesar_mortalidad_inegi.py`. Se evaluó también el dataset "Actas de defunción del Registro Civil de la CDMX" (portal de datos abiertos de la CDMX) como fuente complementaria de validación del total diario de defunciones — ver `docs/decisions.md`.

---

## Estructura del repositorio

```
Proyecto-datos-masivos/
├── data/
│   ├── raw/                          # datos crudos (no versionados): CSV de INEGI por año, etc.
│   ├── LA_daily_climate.csv          # Kaggle, 20 ciudades (fase exploratoria)
│   ├── LA_daily_air_quality.csv      # Open-Meteo, 20 ciudades (fase exploratoria)
│   ├── LA_clima_y_aire_procesado.csv # clima + aire integrados, 20 ciudades
│   ├── CDMX_clima_y_aire_procesado.csv # clima + aire filtrados a la Ciudad de México
│   ├── CDMX_mortalidad_diaria.csv    # defunciones diarias por causa (generado)
│   └── CDMX_panel_diario.csv         # panel final: exposición + rezagos + mortalidad (generado)
│
├── docs/
│   ├── project_scope.md        # alcance, unidad de análisis, limitaciones
│   ├── data_dictionary.md      # diccionario de datos de las tres fuentes
│   ├── architecture.md         # arquitectura del pipeline
│   └── decisions.md            # decisiones técnicas y su justificación
│
├── notebooks/
│   ├── 01_exploracion_inicial.ipynb   # exploración de las 20 ciudades (fase exploratoria)
│   ├── 02_limpieza_y_union.ipynb      # limpieza e integración de clima + aire
│   ├── 03_analisis_y_graficas.ipynb   # análisis descriptivo de las 20 ciudades
│   ├── 04_diccionario_de_datos.ipynb  # diccionario de datos en notebook
│   └── 05_mortalidad_rezago_cdmx.ipynb # correlación por rezago: clima+aire vs. mortalidad CDMX
│
├── src/
│   ├── ingestion/
│   │   └── obtener_calidad_aire.py    # extracción de la Open-Meteo Air Quality API
│   ├── processing/
│   │   ├── procesar_mortalidad_inegi.py  # filtra CDMX, clasifica CIE-10, agrega por día
│   │   └── construir_panel_cdmx.py       # une clima+aire+mortalidad y crea rezagos
│   ├── analysis/
│   │   └── analisis_rezago.py            # correlación cruzada por rezago
│   └── procesamiento.py                  # une clima + aire de las 20 ciudades
│
├── reports/
│   ├── tables/                 # tablas de correlación por rezago
│   └── figures/
│
├── .gitignore
├── requirements.txt
└── README.md
```

Los archivos de datos crudos (CSV de INEGI por año, descargas de Kaggle) no se versionan en GitHub. Los datasets ya agregados y de tamaño manejable (`LA_clima_y_aire_procesado.csv`, `CDMX_*`) sí se incluyen para poder ejecutar los notebooks y scripts sin depender de descargas externas.

---

## Instrucciones iniciales de ejecución

### Requisitos

- Python 3.10 o superior
- Las dependencias listadas en `requirements.txt`

### 1. Clonar el repositorio

```bash
git clone https://github.com/majobarreda/Proyecto-datos-masivos.git
cd Proyecto-datos-masivos
```

### 2. Crear el entorno e instalar dependencias

```bash
python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Obtener los datos climáticos (Kaggle)

Descargar `LA_daily_climate.csv` desde el enlace del dataset y colocarlo en:

```
data/raw/LA_daily_climate.csv
```

### 4. Obtener los datos de calidad del aire (API)

```bash
python -m src.ingestion.obtener_calidad_aire
```

El script consulta la Open-Meteo Air Quality API para las 20 ciudades del dataset climático y guarda el resultado crudo en `data/raw/`.

**La API no requiere credenciales.** Si más adelante se incorpora una fuente que sí las requiera, deberán configurarse mediante variables de entorno y nunca subirse al repositorio.

### 5. Obtener los datos de mortalidad (INEGI)

Descargar los microdatos anuales de "Estadísticas de Defunciones Registradas" desde https://www.inegi.org.mx/programas/mortalidad/?ps=microdatos y colocarlos en:

```
data/raw/defunciones_<año>.csv
```

Procesarlos con:

```bash
python -m src.processing.procesar_mortalidad_inegi data/raw/defunciones_2023.csv data/raw/defunciones_2024.csv
```

### 6. Construir el panel diario de la Ciudad de México y analizarlo

```bash
python -m src.processing.construir_panel_cdmx
python -m src.analysis.analisis_rezago
```

### 7. Ejecutar los notebooks

```bash
jupyter notebook notebooks/01_exploracion_inicial.ipynb
```

Todas las rutas del proyecto son relativas a la raíz del repositorio; no dependen de la computadora de ningún integrante.

---

## Metodología

### Carga y exploración inicial

Se revisaron dimensiones, tipos de datos, valores faltantes, duplicados, estadísticas descriptivas y valores únicos. El dataset de Kaggle contiene **31,440 filas y 14 columnas**, con 20 ciudades y 20 países, **sin valores faltantes ni registros duplicados**.

### Limpieza y transformación

**a) Fechas y zona horaria.** Se convirtió `date` de texto a formato fecha. Como las dos fuentes manejaban las fechas de forma distinta, se unificó el formato y se estandarizó todo a **UTC**, trabajando con horas de 24 en lugar de am/pm, para evitar desfases al unir los conjuntos.

**b) Agregación temporal.** La API entrega datos **horarios** y la base climática es **diaria**. Se calculó el **promedio diario de cada contaminante** (PM10, PM2.5, CO, NO₂, SO₂ y O₃) para trabajar en la misma escala temporal.

**c) Identificación geográfica.** La respuesta de la API solo devuelve datos asociados a coordenadas, sin nombre de ciudad ni país. Se agregaron las columnas de **ciudad, país, latitud y longitud** a cada registro extraído.

**d) Estandarización.** Se eliminaron espacios adicionales en nombres de ciudades y países, se homologaron nombres de variables, se verificó la compatibilidad de coordenadas y se recortó el dataset de Kaggle al periodo 2023-01-01 – 2024-04-20.

### Integración

**Problema encontrado:** en un primer intento se usó únicamente la fecha como llave, pero cada fecha aparece 20 veces (una por ciudad), lo que generaba combinaciones incorrectas entre ciudades.

**Solución:** la unión se realizó con una llave compuesta.

```
fecha + ciudad + país + latitud + longitud
```

Así se garantiza que los datos climáticos y los de calidad del aire correspondan siempre a la misma ubicación y al mismo día.

Se revisaron valores faltantes y duplicados **después de la extracción** y nuevamente **después de la integración**, para comprobar la consistencia antes de continuar con el análisis.

---

## Diagnóstico inicial

| Revisión | Resultado |
|---|---|
| Valores faltantes en el dataset de Kaggle | Ninguno |
| Duplicados completos en el dataset de Kaggle | Ninguno |
| Valores faltantes en la extracción de la API (2023–2024) | Ninguno |
| Valores faltantes en pruebas con 2022 | Presentes en varios contaminantes → motivó el recorte del periodo |
| Duplicados tras la integración | Ninguno |
| Tipos de datos | `date` requería conversión desde texto; el resto numérico |

**Transformaciones que se anticipan para la siguiente etapa:** conversión del dataset procesado a Parquet, particionamiento por ciudad o por mes, y creación de variables derivadas (mes, estación del año, indicador de día lluvioso).

---


## Limitaciones

- Las 20 ciudades disponibles no representan a toda Latinoamérica (relevante solo para la fase exploratoria previa).
- El análisis de la Ciudad de México se limita a la ventana temporal en la que traslapan clima, contaminantes y mortalidad, más corta de lo ideal para un modelo epidemiológico robusto.
- Los valores de contaminantes y clima provienen de modelos (Open-Meteo/CAMS), no de mediciones directas de estaciones locales (SIMAT); ver `docs/decisions.md` sobre esta decisión pendiente.
- La mortalidad se agrega a nivel de toda la Ciudad de México; no hay desagregación por alcaldía en la fuente de causa detallada.
- Los microdatos de INEGI se publican con ~10–14 meses de rezago administrativo; el año más reciente puede no estar disponible aún.
- Al promediar los datos horarios a nivel diario se pierden los picos y la variación intradía.
- Una correlación entre variables (o entre exposición rezagada y mortalidad) no implica causalidad; no se controla por comorbilidades individuales, tabaquismo ni acceso a salud.

Detalle completo de alcance y limitaciones en `docs/project_scope.md`.

---

## Control de versiones y colaboración

El trabajo se organiza mediante issues y ramas: cada tarea principal tiene un issue asociado, se desarrolla en una rama propia y se integra a `main` mediante pull request revisado por otro integrante. Esto deja evidencia del proceso y evita modificar directamente contenido ya validado en la rama principal.
