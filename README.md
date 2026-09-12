# Relación entre condiciones meteorológicas y calidad del aire en ciudades de Latinoamérica

## Descripción del proyecto

Este proyecto analiza la relación entre las condiciones meteorológicas y los niveles de contaminación del aire en distintas ciudades de Latinoamérica, integrando dos fuentes de datos independientes.

La primera fuente corresponde al dataset **Latin America Weather and Air Quality Data**, disponible en Kaggle, que contiene información meteorológica diaria de 20 ciudades de América Latina.

La segunda fuente es la **Open-Meteo Air Quality API**, de la cual se extrajeron los niveles de contaminantes atmosféricos para esas mismas 20 ciudades utilizando Python y la librería `requests`.

El propósito es cargar, explorar, limpiar e integrar ambas fuentes en un solo conjunto de datos que permita identificar patrones entre variables meteorológicas (temperatura, precipitación, velocidad del viento, evapotranspiración) y variables de calidad del aire (PM10, PM2.5, CO, NO₂, SO₂ y O₃), así como comparar diferencias entre ciudades y países de la región.

---

## Problema

Las ciudades de Latinoamérica presentan diferencias importantes en sus condiciones meteorológicas debido a factores geográficos, climáticos y regionales.

Variables como la temperatura, la precipitación y la velocidad del viento influyen en la dispersión, acumulación y formación de contaminantes atmosféricos. Sin embargo, la información meteorológica y la de calidad del aire se encuentra distribuida entre distintas fuentes, con diferentes formatos, escalas temporales y zonas horarias.

Por esta razón es necesario un proceso de carga, exploración, limpieza e integración de datos que permita relacionar ambos tipos de variables sobre una misma base temporal y geográfica.

---

## Pregunta de investigación

**¿Qué relación existe entre las condiciones meteorológicas y los niveles de contaminación del aire en distintas ciudades de Latinoamérica?**

De manera particular se busca analizar el comportamiento conjunto de:

**Variables meteorológicas**
- Temperatura máxima, mínima y promedio.
- Temperatura aparente.
- Precipitación acumulada.
- Velocidad máxima del viento.
- Evapotranspiración de referencia.

**Variables de calidad del aire**
- PM10.
- PM2.5.
- Monóxido de carbono (CO).
- Dióxido de nitrógeno (NO₂).
- Dióxido de azufre (SO₂).
- Ozono (O₃).

También se busca identificar diferencias y similitudes entre ciudades y países.

---

## Usuario o interesado

Los resultados del proyecto podrían ser de interés para:

- Autoridades ambientales.
- Organismos gubernamentales.
- Investigadores.
- Estudiantes.
- Organizaciones relacionadas con medio ambiente.
- Personas interesadas en comparar condiciones climáticas y de contaminación entre ciudades de Latinoamérica.

El análisis puede ayudar a identificar patrones meteorológicos regionales, diferencias entre ciudades y posibles relaciones entre el clima y la concentración de contaminantes, como apoyo para análisis ambientales, estudios comparativos y toma de decisiones.

---

# Fuentes de datos

## 1. Latin America Weather and Air Quality Data — Kaggle

Archivo utilizado: `LA_daily_climate.csv`

Contiene información meteorológica diaria de diferentes ciudades de Latinoamérica.

### Dimensiones iniciales

- **31,440 registros**
- **14 variables**
- **20 ciudades**
- **20 países**
- **1,572 fechas diferentes**

### Variables

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

**Fuente:** https://www.kaggle.com/datasets/anycaroliny/latin-america-weather-and-air-quality-data

---

## 2. Open-Meteo Air Quality API

La segunda fuente es la API de Open-Meteo, de la cual se extrajeron los datos de calidad del aire.

La consulta se realizó de manera automatizada con Python (`requests`), iterando sobre las coordenadas de las 20 ciudades presentes en el dataset de Kaggle.

Contaminantes extraídos:

- `pm10`
- `pm2_5`
- `carbon_monoxide` (CO)
- `nitrogen_dioxide` (NO₂)
- `sulphur_dioxide` (SO₂)
- `ozone` (O₃)

**Fuente:** https://open-meteo.com/

### Definición del periodo de análisis

El dataset de Kaggle contiene información desde 2020, pero para la calidad del aire se trabajó con el periodo que podía obtenerse de manera consistente mediante la API.

Durante las pruebas de extracción se detectó que en algunas consultas correspondientes a 2022 aparecían valores faltantes en los contaminantes. Por esta razón se decidió limitar el análisis al periodo:

**1 de enero de 2023 — 20 de abril de 2024**

La fecha final corresponde al último registro disponible en el dataset de Kaggle. Con este recorte se logró obtener la información de las 20 ciudades sin valores faltantes en la extracción utilizada.

---

# Metodología

## 1. Carga de datos

El archivo de Kaggle se carga con `pandas`:

```python
df_kaggle = pd.read_csv("../data/LA_daily_climate.csv")
```

Los datos de calidad del aire se obtienen ejecutando los scripts de extracción ubicados en `src/ingestion/`.

---

## 2. Exploración inicial

Después de cargar el dataset se revisaron:

- Primeras filas.
- Número de registros y columnas.
- Nombre de las variables y tipos de datos.
- Valores faltantes y registros duplicados.
- Estadísticas descriptivas.
- Valores únicos, número de ciudades y de países.

El dataset inicial contiene **31,440 filas y 14 columnas**, con **20 ciudades y 20 países**.

Las variables `country`, `city` y `date` se encontraban originalmente como texto, mientras que las variables meteorológicas y las coordenadas estaban almacenadas como valores numéricos.

---

## 3. Limpieza y transformación de datos

En la exploración inicial se confirmó que el dataset de Kaggle no presentaba valores faltantes ni registros completamente duplicados.

Las transformaciones aplicadas a ambas fuentes fueron las siguientes:

**a) Fechas y zona horaria**

- Se convirtió la variable `date` de texto a formato de fecha.
- Como las dos fuentes manejaban las fechas de forma distinta, se unificó el formato y se estandarizó todo a **UTC**, trabajando con horas de 24 en lugar de am/pm. Esto evitó desfases al momento de unir los conjuntos de datos.

**b) Agregación temporal de la API**

- La Open-Meteo Air Quality API entrega los datos por **hora**, mientras que la base climática es **diaria**.
- Se calculó el **promedio diario de cada contaminante** (PM10, PM2.5, CO, NO₂, SO₂ y O₃) para trabajar con la misma escala temporal que el dataset climático.

**c) Identificación geográfica de los registros de la API**

- La respuesta de la API no incluye el nombre de la ciudad ni del país, únicamente los datos asociados a unas coordenadas.
- Se agregaron las columnas de **ciudad, país, latitud y longitud** a cada registro extraído, de modo que cada observación quedara identificada con su ubicación correspondiente.

**d) Estandarización previa a la integración**

- Se eliminaron espacios adicionales en los nombres de ciudades y países.
- Se estandarizaron nombres de ciudades, países y de las variables.
- Se verificó que las coordenadas de ambas fuentes fueran compatibles.
- Se recortó el dataset de Kaggle al periodo 2023-01-01 – 2024-04-20 para que coincidiera con la extracción de la API.

---

## 4. Integración de los datasets

La integración se realizó mediante un `merge` entre el dataset climático y el de calidad del aire.

**Problema encontrado:** en un primer intento se utilizó únicamente la fecha como llave, pero cada fecha aparece 20 veces (una por ciudad), lo que generaba combinaciones incorrectas entre ciudades.

**Solución:** la unión se hizo utilizando una llave compuesta:

```
fecha + ciudad + país + latitud + longitud
```

Con esto se garantizó que los datos climáticos y los de calidad del aire correspondieran siempre a la misma ubicación y al mismo día.

Después de la extracción y nuevamente después de la integración se revisaron valores faltantes y registros duplicados, para comprobar la consistencia del conjunto antes de continuar con el análisis.

Estructura del DataFrame integrado:

| date | country | city | latitude | longitude | temperature_2m_mean | precipitation_sum | wind_speed_10m_max | pm10 | pm2_5 | carbon_monoxide | nitrogen_dioxide | sulphur_dioxide | ozone |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|

---

## 5. Análisis exploratorio

Sobre el dataset integrado se analiza el comportamiento conjunto de las variables meteorológicas y de calidad del aire:

- Promedios por ciudad y por país.
- Valores mínimos y máximos.
- Variaciones mensuales y estacionales.
- Correlaciones entre variables meteorológicas y contaminantes.
- Rankings de ciudades según niveles de contaminación.
- Diferencias entre ciudades con condiciones climáticas distintas.

---

## 6. Visualización

Las gráficas se elaboran principalmente con `matplotlib`:

- Concentración promedio de cada contaminante por ciudad.
- Temperatura promedio por ciudad.
- Precipitación y velocidad del viento por ciudad.
- Evolución temporal de contaminantes y de variables meteorológicas.
- Relación entre precipitación / viento y niveles de PM10 y PM2.5.
- Matriz de correlación entre variables meteorológicas y contaminantes.
- Comparación entre países.
- Rankings de ciudades.

---

# Organización del repositorio

```
proyecto/
├── data/                 # datos crudos e integrados
├── notebooks/            # exploración, limpieza, integración y análisis
├── src/
│   └── ingestion/        # scripts de extracción de la API de Open-Meteo
└── README.md
```

El proceso de extracción se desarrolló mediante prueba y error dentro de `src/`. El código final de extracción quedó registrado en **`src/ingestion/`**, de manera que no solo exista la evidencia del proceso en el notebook, sino que la obtención de los datos pueda volver a ejecutarse.

## Control de versiones

Los cambios correspondientes a la integración de la API se trabajaron en un **branch separado** y posteriormente se integraron a `main`. Esto permitió dejar evidencia del proceso y evitar modificar o borrar accidentalmente contenido ya validado en la rama principal.

---

# Resultados principales

- Se confirmó que el dataset de Kaggle contiene **31,440 registros y 14 variables** de 20 ciudades y 20 países, sin valores faltantes ni duplicados.
- Se logró extraer de la Open-Meteo Air Quality API los seis contaminantes (PM10, PM2.5, CO, NO₂, SO₂ y O₃) para las **20 ciudades**, en el periodo **2023-01-01 a 2024-04-20**, sin valores faltantes.
- Los datos horarios de la API se agregaron a promedios diarios, quedando en la misma escala temporal que el dataset climático.
- La integración mediante la llave compuesta *fecha + ciudad + país + latitud + longitud* permitió unir correctamente ambas fuentes, corrigiendo el problema de duplicación que se presentaba al unir únicamente por fecha.
- El dataset integrado quedó validado sin valores faltantes ni duplicados, listo para el análisis exploratorio y la construcción de visualizaciones.

---

# Limitaciones

- Las ciudades analizadas son únicamente las 20 disponibles en el dataset y no representan a toda Latinoamérica.
- El análisis se limita al periodo 2023-01-01 – 2024-04-20 por la disponibilidad consistente de datos en la API; los datos climáticos anteriores a 2023 no se utilizan.
- En pruebas con consultas de 2022 se detectaron valores faltantes en los contaminantes, lo que motivó el recorte del periodo.
- Kaggle y Open-Meteo pueden utilizar métodos distintos para generar o estimar sus datos, y las coordenadas pueden presentar pequeñas diferencias.
- Los valores de contaminantes corresponden a modelos de calidad del aire y no a mediciones directas de estaciones locales de monitoreo.
- Al promediar los datos horarios a nivel diario se pierden los picos y la variación intradía de los contaminantes.
- La comparación entre ciudades debe considerar diferencias de altitud, geografía, densidad poblacional y actividad industrial, que no están incluidas en el dataset.
- Una correlación entre variables no implica necesariamente una relación causal.

---

# Conclusiones

La corrección de la integración con la API permitió consolidar un dataset único que combina información meteorológica y de calidad del aire para 20 ciudades de Latinoamérica en el periodo 2023-2024.

Los principales aprendizajes de esta etapa fueron la importancia de **homologar la escala temporal** entre fuentes (horaria contra diaria), **unificar la zona horaria y el formato de fechas** (UTC), y **definir una llave de unión compuesta** que incluya la ubicación y no solamente la fecha, ya que una misma fecha se repite para las 20 ciudades.

Con el dataset integrado y validado, el siguiente paso es desarrollar el análisis exploratorio y las visualizaciones para responder la pregunta de investigación sobre la relación entre las condiciones meteorológicas y los niveles de contaminación del aire entre las distintas ciudades.
