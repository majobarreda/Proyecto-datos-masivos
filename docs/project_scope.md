# Alcance del proyecto

## Contexto del problema

La Ciudad de México registra episodios recurrentes de mala calidad del aire (ozono en temporada cálida-seca, PM2.5 y PM10 en temporada fría) que coinciden con estancamiento atmosférico y variaciones de temperatura. La literatura de salud ambiental documenta que la exposición a contaminantes y a temperaturas extremas no se traduce en un aumento inmediato de la mortalidad, sino con un **rezago (lag) de horas a semanas**, y que ese rezago difiere entre causas respiratorias y cardiovasculares.

El proyecto había construido, en su primera fase, un dataset comparativo de clima y calidad del aire para 20 ciudades de Latinoamérica (ver README, sección "Fuentes de datos"). Esa fase sirve ahora como **antecedente exploratorio**: permitió validar el proceso de adquisición e integración de Open-Meteo, y dejó aislada la serie de la Ciudad de México (`data/CDMX_clima_y_aire_procesado.csv`) como base para esta nueva etapa, en la que se acota el alcance a una sola ciudad para poder incorporar una tercera fuente: mortalidad diaria.

## Pregunta principal

**¿Qué combinaciones de condiciones meteorológicas y niveles de contaminantes en la Ciudad de México, con qué rezago temporal (lag) respecto al evento, están más asociadas con incrementos en la mortalidad diaria por causas respiratorias y cardiovasculares, y qué patrones podrían usarse como señal temprana de días de mayor riesgo?**

### Preguntas secundarias

1. ¿En qué rezago (0 a 14 días) cada contaminante (PM2.5, PM10, O₃, NO₂, SO₂, CO) muestra la asociación más fuerte con la mortalidad respiratoria y con la cardiovascular?
2. ¿El efecto de la temperatura (calor y frío extremos) tiene un patrón de rezago distinto al de los contaminantes?
3. ¿Existen combinaciones de variables (p. ej. temperatura alta + ozono alto) cuya asociación conjunta con la mortalidad sea mayor que la de cada variable por separado?
4. ¿El rezago óptimo difiere entre mortalidad respiratoria y cardiovascular?
5. ¿Qué percentiles de exposición (p. ej. P90/P95 de PM2.5 u ozono) podrían usarse como umbral de una señal de alerta temprana?
6. ¿Los patrones encontrados se mantienen estables entre temporadas (fría-seca, cálida-seca, lluvias) o cambian con la estacionalidad?

## Unidad de análisis

**Día calendario en la Ciudad de México.** El dataset analítico final es una serie de tiempo diaria (CDMX × día): cada fila combina las condiciones meteorológicas y de contaminantes de un día (y sus versiones rezagadas 0–14 días) con el número de defunciones registradas ese mismo día por causa respiratoria, cardiovascular y total.

### ¿Qué representa una fila?

- **Antes de integrar:**
  - Clima y contaminantes (Kaggle + Open-Meteo Air Quality API): una medición diaria agregada de la Ciudad de México (temperatura, precipitación, viento, PM10, PM2.5, CO, NO₂, SO₂, O₃).
  - Mortalidad (INEGI, microdatos de "Estadísticas de Defunciones Registradas"): en la fuente cruda, **una fila = una defunción individual** con fecha y causa de defunción (código CIE-10); tras agregarla por día y capítulo de causa, una fila = el conteo de defunciones de la Ciudad de México en un día para una categoría de causa.
- **Dataset analítico final:** una fila = un día en la Ciudad de México, con sus variables de exposición (y rezagos) y sus conteos de defunciones.

## Alcance

- **Geográfico:** exclusivamente Ciudad de México. La comparación entre 20 ciudades queda como antecedente/motivación, no como pregunta activa de esta etapa.
- **Temporal:** acotado por la intersección de las tres fuentes (clima, contaminantes, mortalidad). Ver `docs/decisions.md` para la discusión sobre por qué la ventana actual es corta y cómo podría extenderse en la siguiente entrega.
- **Analítico:** el objetivo es identificar **asociaciones estadísticas** (correlación cruzada por rezago y regresión con términos rezagados), no establecer causalidad. Se trata de un ejercicio exploratorio de un semestre, no un estudio epidemiológico publicable.

## Limitaciones

- Correlación no implica causalidad; no se controlan confusores individuales (comorbilidades, tabaquismo, acceso a salud).
- La mortalidad se analiza agregada a nivel de toda la Ciudad de México; la fuente de causa detallada no permite desagregar por alcaldía.
- Los contaminantes y variables meteorológicas de Open-Meteo son estimaciones de modelo (reanálisis CAMS), no mediciones directas de estación — ver la decisión sobre SIMAT/RAMA en `docs/decisions.md`.
- La ventana temporal en la que las tres fuentes se traslapan es más corta de lo ideal para separar tendencia, estacionalidad y rezago con solidez estadística.
- Las defunciones registradas de INEGI se publican con un rezago administrativo (~10–14 meses tras el cierre del año), por lo que el año más reciente puede no estar disponible aún al momento del análisis.

## Usuarios o interesados

| Usuario | Decisión que podría tomar con esta información |
|---|---|
| Secretaría de Salud de la Ciudad de México / autoridades de vigilancia epidemiológica | Anticipar días de mayor riesgo respiratorio o cardiovascular y reforzar capacidad hospitalaria o campañas de prevención. |
| Autoridades ambientales (SEDEMA) | Priorizar qué variable meteorológica o contaminante vigilar como señal temprana, más allá del índice de calidad del aire actual. |
| Población vulnerable (adultos mayores, personas con enfermedad respiratoria o cardiovascular crónica) | Ajustar su exposición (evitar exteriores, usar cubrebocas) en los días identificados como de mayor riesgo. |
| Investigadores y estudiantes | Usar el panel diario integrado como base para estudios más rigurosos de salud ambiental en la Ciudad de México. |

## Valor esperado

Un panel de datos diario y reproducible para la Ciudad de México que integre clima, contaminantes y mortalidad por causa, junto con un primer análisis exploratorio de correlación por rezago que identifique qué combinaciones de exposición preceden, con qué demora, incrementos en la mortalidad respiratoria y cardiovascular — como insumo inicial para un futuro sistema de alerta temprana de salud pública.
