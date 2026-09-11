# Análisis del clima y calidad del aire en ciudades de Latinoamérica

## Descripción del proyecto

Este proyecto tiene como objetivo analizar las condiciones meteorológicas y su posible relación con la calidad del aire en distintas ciudades de Latinoamérica mediante la integración de dos fuentes de datos.

La primera fuente corresponde al dataset **Latin America Weather and Air Quality Data**, disponible en Kaggle, que contiene información de diferentes ciudades de América Latina.

La segunda fuente será la **Open-Meteo API**, mediante la cual se obtendrán datos meteorológicos históricos para las mismas ciudades utilizando Python.

El propósito es cargar, explorar, limpiar e integrar ambas fuentes de información para identificar patrones relacionados con variables como temperatura, precipitación, velocidad del viento y otras variables meteorológicas, así como comparar diferencias entre ciudades y países de Latinoamérica.

---

## Problema

Las ciudades de Latinoamérica presentan diferencias importantes en sus condiciones meteorológicas debido a factores geográficos, climáticos y regionales.

Variables como la temperatura, la precipitación, la velocidad del viento y la evapotranspiración pueden presentar comportamientos distintos entre ciudades y también pueden relacionarse con cambios en la calidad del aire.

Sin embargo, la información necesaria para realizar este tipo de análisis se encuentra distribuida entre diferentes fuentes y formatos.

Por esta razón, es necesario realizar un proceso de carga, exploración, limpieza e integración de datos que permita comparar las condiciones meteorológicas entre diferentes ciudades de Latinoamérica.

---

## Pregunta de investigación

**¿Cómo varían las condiciones meteorológicas y la calidad del aire entre distintas ciudades de Latinoamérica y qué relaciones existen entre estas variables?**

De manera particular, se busca analizar el comportamiento de variables como:

- Temperatura máxima.
- Temperatura mínima.
- Temperatura promedio.
- Temperatura aparente.
- Precipitación.
- Velocidad del viento.
- Evapotranspiración.
- Variables relacionadas con calidad del aire.

También se buscará identificar diferencias y similitudes entre ciudades y países.

---

## Usuario o interesado

Los resultados del proyecto podrían ser de interés para:

- Autoridades ambientales.
- Organismos gubernamentales.
- Investigadores.
- Estudiantes.
- Organizaciones relacionadas con medio ambiente.
- Personas interesadas en comparar condiciones climáticas entre ciudades de Latinoamérica.

El análisis podría ayudar a identificar patrones meteorológicos regionales, diferencias entre ciudades y posibles relaciones entre las condiciones del clima y la calidad del aire.

Esta información podría utilizarse como apoyo para análisis ambientales, estudios comparativos y toma de decisiones.

---

# Fuentes de datos

## 1. Latin America Weather and Air Quality Data - Kaggle

La primera fuente utilizada corresponde al dataset:

**Latin America Weather and Air Quality Data**

Disponible en Kaggle.

El archivo utilizado inicialmente es:

`LA_daily_climate.csv`

El dataset contiene información meteorológica diaria de diferentes ciudades de Latinoamérica.

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

Para este proyecto se utilizarán las coordenadas de las diferentes ciudades incluidas en el dataset de Kaggle.

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

df_kaggle = pd.read_csv("../data/LA_daily_climate.csv")
## 2. Exploración inicial

Después de cargar el dataset se realizó una exploración inicial para conocer su estructura.

Se revisaron:

- Primeras filas.
- Número de registros.
- Número de columnas.
- Nombre de las variables.
- Tipos de datos.
- Valores faltantes.
- Registros duplicados.
- Estadísticas descriptivas.
- Valores únicos de las variables.
- Número de ciudades.
- Número de países.

El dataset inicial contiene **31,440 filas y 14 columnas**.

También se identificaron **20 ciudades y 20 países**.

Las variables `country`, `city` y `date` se encuentran inicialmente como texto, mientras que las variables meteorológicas y las coordenadas se encuentran almacenadas como valores numéricos.

---

## 3. Limpieza de datos

En la exploración inicial se encontró que:

- No existen valores faltantes.
- No existen registros completamente duplicados.

Por lo tanto, el dataset presenta inicialmente una buena calidad de información.

Sin embargo, todavía será necesario realizar algunas transformaciones.

Entre ellas:

- Convertir la variable `date` de texto a formato de fecha.
- Eliminar posibles espacios adicionales en los nombres de las ciudades.
- Estandarizar nombres de ciudades y países.
- Verificar que las fechas utilizadas coincidan con las disponibles en Open-Meteo.
- Verificar las coordenadas geográficas de cada ciudad.
- Estandarizar nombres de variables antes de realizar la integración.

---

## 4. Análisis exploratorio

Después de limpiar los datos se realizará un análisis exploratorio considerando todas las ciudades disponibles en el dataset.

Se analizarán variables como:

- Temperatura máxima.
- Temperatura mínima.
- Temperatura promedio.
- Temperatura aparente.
- Precipitación.
- Velocidad del viento.
- Evapotranspiración.

También se observará el comportamiento de estas variables a través del tiempo y entre diferentes ciudades.

Se podrán calcular:

- Promedios por ciudad.
- Promedios por país.
- Valores mínimos y máximos.
- Variaciones mensuales.
- Diferencias entre ciudades.
- Correlaciones entre variables.
- Rankings de ciudades según determinadas variables meteorológicas.

---

## 5. Integración de datasets

Posteriormente se integrarán los datos de Kaggle con los obtenidos mediante Open-Meteo.

Las principales variables que permitirán realizar la integración serán:

- Fecha.
- Ciudad.
- País.
- Latitud.
- Longitud.

Antes de realizar el `merge`, será necesario verificar que las fechas, ciudades y coordenadas tengan formatos compatibles.

La integración permitirá comparar la información de ambas fuentes dentro de un solo DataFrame.

Una posible estructura final será:

| date | country | city | temperature_kaggle | temperature_openmeteo | precipitation | wind_speed |
|---|---|---|---:|---:|---:|---:|
| 2024-01-01 | Mexico | Mexico City | 15.2 | 15.0 | 0.0 | 12.3 |
| 2024-01-01 | Argentina | Buenos Aires | 24.7 | 24.5 | 0.6 | 24.3 |

Esto permitirá realizar comparaciones entre los datos obtenidos de Kaggle y los datos obtenidos mediante API para las diferentes ciudades.

---

## 6. Visualización

Después de integrar los datos se realizarán gráficas para facilitar su análisis.

Entre las visualizaciones consideradas se encuentran:

- Temperatura promedio por ciudad.
- Temperatura máxima y mínima por ciudad.
- Precipitación promedio por ciudad.
- Velocidad del viento por ciudad.
- Comparación entre países.
- Comparación de temperaturas entre Kaggle y Open-Meteo.
- Evolución temporal de variables meteorológicas.
- Relación entre diferentes variables.
- Matriz de correlación.
- Ranking de ciudades según temperatura o precipitación.

Las gráficas se realizarán principalmente utilizando `matplotlib`.

---

# Resultados principales

Hasta esta primera etapa se identificó que el dataset de Kaggle contiene **31,440 registros y 14 variables** correspondientes a diferentes ciudades de Latinoamérica.

La exploración inicial mostró que el dataset no presenta valores faltantes ni registros duplicados.

También se identificaron **20 ciudades y 20 países**, así como variables meteorológicas relacionadas con temperatura, temperatura aparente, precipitación, viento y evapotranspiración.

En las siguientes etapas se limpiarán y estandarizarán los datos de las diferentes ciudades y posteriormente se integrarán con información obtenida mediante Open-Meteo.

Los resultados definitivos se actualizarán después de completar la integración y el análisis exploratorio.

---

# Limitaciones

Hasta el momento se consideran las siguientes limitaciones:

- Las ciudades analizadas representan únicamente las ciudades disponibles en el dataset y no todas las ciudades de Latinoamérica.
- Las fechas se encuentran inicialmente almacenadas como texto.
- Kaggle y Open-Meteo pueden utilizar diferentes métodos para generar o estimar los datos meteorológicos.
- Las coordenadas utilizadas por ambas fuentes podrían presentar pequeñas diferencias.
- Los periodos disponibles en ambas fuentes pueden no coincidir completamente.
- Será necesario trabajar únicamente con las fechas presentes en ambas fuentes para realizar una comparación correcta.
- La comparación entre ciudades debe considerar que existen diferencias geográficas, de altitud y ubicación.
- Una correlación entre variables no necesariamente representa una relación causal.

---

# Conclusiones

La primera exploración permitió comprobar que el dataset de Kaggle tiene una estructura adecuada para continuar con el proyecto.

El conjunto cuenta con **31,440 registros, 20 ciudades, 20 países y múltiples variables meteorológicas**, lo que permite realizar un análisis comparativo entre diferentes regiones de Latinoamérica.

Además, no se identificaron valores faltantes ni registros duplicados, por lo que la cantidad de limpieza inicial necesaria es relativamente baja.

El siguiente paso será transformar correctamente la variable de fecha, limpiar los nombres de las ciudades y realizar la extracción de datos meteorológicos mediante Open-Meteo para cada una de las ubicaciones.

Posteriormente, ambos datasets serán integrados para realizar comparaciones entre ciudades, identificar patrones meteorológicos y responder la pregunta de investigación.
