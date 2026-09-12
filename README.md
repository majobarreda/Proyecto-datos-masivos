# Relación entre condiciones meteorológicas y calidad del aire en ciudades de Latinoamérica

Proyecto semestral del curso de Datos Masivos. Integra un dataset climático diario de Kaggle con datos de calidad del aire obtenidos mediante la Open-Meteo Air Quality API, para analizar la relación entre el clima y los niveles de contaminación en 20 ciudades de Latinoamérica.

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

**¿Qué relación existe entre las condiciones meteorológicas y los niveles de contaminación del aire en distintas ciudades de Latinoamérica?**

### Preguntas secundarias

1. ¿Qué ciudades presentan los mayores y menores niveles promedio de PM2.5 y PM10 en el periodo analizado?
2. ¿Existe una relación negativa entre la precipitación y la concentración de material particulado?
3. ¿La velocidad del viento se asocia con menores concentraciones de contaminantes?
4. ¿La temperatura se relaciona con los niveles de ozono (O₃)?
5. ¿Los patrones observados se repiten entre ciudades o dependen de características locales?

### ¿Qué representa una fila?

Cada registro del dataset integrado representa **la medición diaria de una ciudad**: las condiciones meteorológicas y los niveles promedio de contaminantes de una ciudad específica en una fecha específica.

La unidad de análisis es, por lo tanto, la combinación **ciudad × día**.

---

## Objetivo

Construir un conjunto de datos reproducible que integre información meteorológica y de calidad del aire para 20 ciudades de Latinoamérica, y utilizarlo para identificar y cuantificar la relación entre variables climáticas y niveles de contaminación atmosférica.

Objetivos específicos:

- Obtener mediante código los datos de calidad del aire de la Open-Meteo Air Quality API.
- Homologar la escala temporal, la zona horaria y los identificadores geográficos de ambas fuentes.
- Integrar ambas fuentes en un único dataset validado, sin valores faltantes ni duplicados.
- Analizar correlaciones y diferencias entre ciudades y países.

---

## Usuario o interesado

| Usuario | Decisión que podría tomar con esta información |
|---|---|
| Autoridades ambientales municipales | Identificar en qué condiciones climáticas conviene activar alertas o restricciones vehiculares. |
| Organismos de salud pública | Anticipar días de mayor exposición a material particulado para poblaciones vulnerables. |
| Investigadores y estudiantes | Usar el dataset integrado como base para estudios comparativos regionales. |
| Organizaciones ambientales | Sustentar comparaciones entre ciudades con evidencia cuantitativa. |

---

## Fuentes de datos

El proyecto utiliza **dos fuentes**, una de descarga y una obtenida mediante código.

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

---

## Estructura del repositorio

```
Proyecto-datos-masivos/
├── data/
│   ├── raw/                    # datos crudos (no versionados)
│   ├── interim/                # datos parcialmente transformados
│   ├── processed/              # dataset integrado listo para análisis
│   └── sample/                 # muestra pequeña para ejecutar los notebooks
│
├── docs/
│   ├── project_scope.md        # alcance, unidad de análisis, limitaciones
│   ├── data_dictionary.md      # diccionario de datos de ambas fuentes
│   └── architecture.md         # arquitectura propuesta
│
├── notebooks/
│   ├── 01_exploration.ipynb    # exploración inicial y diagnóstico
│   └── 02_cleaning.ipynb       # limpieza e integración de fuentes
│
├── src/
│   └── ingestion/              # extracción de la Open-Meteo Air Quality API
│
├── .gitignore
├── requirements.txt
└── README.md
```

Los archivos de datos crudos no se versionan en GitHub. El repositorio incluye una muestra en `data/sample/` para poder ejecutar los notebooks sin descargar el dataset completo.

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
python -m src.ingestion.get_air_quality
```

El script consulta la Open-Meteo Air Quality API para las 20 ciudades del dataset climático y guarda el resultado crudo en `data/raw/`.

**La API no requiere credenciales.** Si más adelante se incorpora una fuente que sí las requiera, deberán configurarse mediante variables de entorno y nunca subirse al repositorio.

### 5. Ejecutar los notebooks

```bash
jupyter notebook notebooks/01_exploration.ipynb
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

## Primera evidencia

<!-- COMPLETAR con los valores reales que arroje el notebook 01_exploration.ipynb -->

**Pregunta:** ¿Qué ciudades presentan los mayores niveles promedio de PM2.5 en el periodo analizado?

| Ciudad | País | PM2.5 promedio (µg/m³) |
|---|---|---|
| *(completar)* | | |
| *(completar)* | | |
| *(completar)* | | |

**Interpretación:** *(Redactar 3–4 líneas: qué ciudades encabezan el ranking, si se agrupan por región o altitud, y cómo contrastan con las de menores niveles. Ligarlo a la pregunta principal.)*


---

## Limitaciones

- Las 20 ciudades disponibles no representan a toda Latinoamérica.
- El análisis se limita al periodo 2023-01-01 – 2024-04-20; los datos climáticos anteriores a 2023 no se utilizan.
- Los valores de contaminantes provienen de modelos de calidad del aire, no de mediciones directas de estaciones locales de monitoreo.
- Al promediar los datos horarios a nivel diario se pierden los picos y la variación intradía.
- Kaggle y Open-Meteo pueden usar métodos distintos para generar sus datos, y las coordenadas pueden diferir ligeramente.
- La comparación entre ciudades no controla por altitud, densidad poblacional ni actividad industrial, variables no incluidas en el dataset.
- Una correlación entre variables no implica causalidad.

---

## Control de versiones y colaboración

El trabajo se organiza mediante issues y ramas: cada tarea principal tiene un issue asociado, se desarrolla en una rama propia y se integra a `main` mediante pull request revisado por otro integrante. Esto deja evidencia del proceso y evita modificar directamente contenido ya validado en la rama principal.
