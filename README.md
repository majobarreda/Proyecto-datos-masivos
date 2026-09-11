# Análisis del clima y calidad del aire en Ciudad de México

## Descripción del proyecto

Este proyecto tiene como objetivo analizar las condiciones meteorológicas y su posible relación con la calidad del aire en Ciudad de México mediante la integración de dos fuentes de datos.

La primera fuente corresponde al dataset **Latin America Weather and Air Quality Data**, disponible en Kaggle. Para este proyecto se utilizarán principalmente los registros correspondientes a Ciudad de México.

La segunda fuente será la **Open-Meteo API**, mediante la cual se obtendrán datos meteorológicos históricos de Ciudad de México utilizando Python.

El propósito es cargar, explorar, limpiar e integrar ambas fuentes de información para identificar patrones relacionados con variables como temperatura, precipitación, velocidad del viento y, posteriormente, variables relacionadas con calidad del aire.

---

## Problema

La Ciudad de México presenta variaciones importantes en sus condiciones meteorológicas y en la calidad del aire.

Variables como la temperatura, la precipitación y la velocidad del viento pueden presentar relaciones con el comportamiento de los contaminantes atmosféricos.

Sin embargo, la información necesaria para analizar estas relaciones puede encontrarse distribuida entre diferentes fuentes y formatos.

Por esta razón, es necesario realizar un proceso de carga, exploración, limpieza e integración de datos antes de poder obtener conclusiones.

---

## Pregunta de investigación

**¿Qué relación existe entre las condiciones meteorológicas y los niveles de calidad del aire en Ciudad de México?**

De manera particular, se busca analizar el comportamiento de variables meteorológicas como:

- Temperatura.
- Temperatura aparente.
- Precipitación.
- Velocidad del viento.
- Evapotranspiración.

Posteriormente, estas variables podrán compararse con información relacionada con la calidad del aire.

---

## Usuario o interesado

Los resultados del proyecto podrían ser de interés para:

- Autoridades ambientales.
- Investigadores.
- Estudiantes.
- Organizaciones relacionadas con medio ambiente.
- Habitantes de Ciudad de México.

El análisis podría ayudar a identificar patrones meteorológicos y relaciones entre las condiciones del clima y la calidad del aire.

Esta información podría utilizarse como apoyo para el análisis ambiental y la toma de decisiones.

---

# Fuentes de datos

## 1. Latin America Weather and Air Quality Data - Kaggle

La primera fuente utilizada corresponde al dataset:

**Latin America Weather and Air Quality Data**

Disponible en Kaggle.

El archivo utilizado inicialmente es:

`LA_daily_climate.csv`

El dataset contiene información meteorológica diaria de diferentes ciudades de América Latina.

### Dimensiones iniciales

El archivo contiene:

- **31,440 registros**
- **14 variables**
- **20 ciudades**
- **20 países**
- **1,572 fechas diferentes**

### Variables

Las variables disponibles son:

- `country`: país.
- `city`: ciudad.
- `date`: fecha del registro.
- `latitude`: latitud.
- `longitude`: longitud.
- `temperature_2m_max`: temperatura máxima a 2 metros.
- `temperature_2m_min`: temperatura mínima a 2 metros.
- `temperature_2m_mean`: temperatura promedio a 2 metros.
- `apparent_temperature_max`: temperatura aparente máxima.
- `apparent_temperature_min`: temperatura aparente mínima.
- `apparent_temperature_mean`: temperatura aparente promedio.
- `precipitation_sum`: precipitación acumulada.
- `wind_speed_10m_max`: velocidad máxima del viento a 10 metros.
- `et0_fao_evapotranspiration`: evapotranspiración de referencia.

**Fuente:** Kaggle

https://www.kaggle.com/datasets/anycaroliny/latin-america-weather-and-air-quality-data

---

## 2. Open-Meteo API

La segunda fuente de información será la API de Open-Meteo.

Open-Meteo permite obtener datos meteorológicos históricos mediante consultas realizadas a partir de coordenadas geográficas y periodos específicos.

Para este proyecto se utilizarán las coordenadas correspondientes a Ciudad de México.

Los datos serán obtenidos automáticamente mediante Python utilizando la librería `requests`.

Algunas de las variables que se utilizarán serán:

- Temperatura.
- Precipitación.
- Velocidad del viento.
- Otras variables meteorológicas compatibles con el dataset de Kaggle.

El uso de esta API permitirá contar con una segunda fuente de datos y posteriormente realizar la integración de ambos conjuntos.

**Fuente:** Open-Meteo

https://open-meteo.com/

---

# Metodología

## 1. Carga de datos

El archivo de Kaggle se carga utilizando la librería `pandas`.

```python
df_kaggle = pd.read_csv("../data/LA_daily_climate.csv")
