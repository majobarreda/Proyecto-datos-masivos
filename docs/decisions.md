# Decisiones técnicas

## Decisión: acotar el alcance geográfico a la Ciudad de México

**Razón:** la nueva pregunta requiere una fuente de mortalidad diaria por causa, y la única fuente confiable identificada (INEGI) permite construir series diarias por entidad federativa, no por las 20 ciudades de Latinoamérica del análisis previo (que no comparten una fuente de mortalidad homologada entre países).

**Alternativas consideradas:** mantener las 20 ciudades y buscar una fuente de mortalidad por país para cada una — descartada por la carga de trabajo de homologar fuentes de mortalidad de 20 países distintos en el tiempo disponible del curso.

**Consecuencias:** la comparación regional deja de ser la pregunta activa, pero se conserva como antecedente/motivación en el README, y el dataset `CDMX_clima_y_aire_procesado.csv` ya generado en esa fase se reutiliza como una de las tres fuentes de esta etapa.

---

## Decisión: usar INEGI "Estadísticas de Defunciones Registradas" (EDR) como fuente de mortalidad

**Razón:** son microdatos públicos y gratuitos, con fecha exacta de ocurrencia de la defunción y causa clasificada con código CIE-10 detallado, lo que permite construir un conteo diario por capítulo de causa (respiratorio J00–J99, cardiovascular I00–I99) para la Ciudad de México.

**Alternativas consideradas:** "Actas de defunción en el Registro Civil de la Ciudad de México" (portal de datos abiertos de la CDMX) — se actualiza con mayor frecuencia y se usó para el monitoreo de exceso de mortalidad por COVID, pero no trae la causa clasificada con el detalle de CIE-10 necesario para separar respiratorio de cardiovascular. Se documenta como fuente complementaria para validar el total diario de defunciones, no como fuente principal de causa.

**Consecuencias:** al ser archivos anuales sin API estable, la adquisición de esta fuente es una descarga manual documentada (igual que Kaggle en la fase previa), no un proceso automatizado por código. Además, el año más reciente puede no estar disponible aún por el rezago de publicación de INEGI (~10-14 meses).

---

## Decisión: mantener Open-Meteo (datos modelados) para clima y contaminantes en esta primera versión, y dejar pendiente la evaluación de SIMAT/RAMA-REDMET

**Razón:** Open-Meteo ya está integrado y validado desde la fase previa, lo que permite entregar una primera versión funcional del panel CDMX sin trabajo adicional de ingestión.

**Alternativa considerada:** SEDEMA opera el Sistema de Monitoreo Atmosférico (SIMAT) de la Ciudad de México, con redes de estaciones (RAMA para contaminantes, REDMET para variables meteorológicas) que miden directamente desde 1986, en vez de usar un modelo de reanálisis. Para un estudio de salud, mediciones directas de estación son preferibles a estimaciones de modelo, y su ventana histórica más larga permitiría una serie con más años de traslape con la mortalidad de INEGI.

**Consecuencias:** se documenta como mejora pendiente para el segundo parcial: requiere una nueva ingestión (descarga de series por estación desde `aire.cdmx.gob.mx` o el portal de datos abiertos de la CDMX) y una etapa de agregación por estación/ciudad que hoy no existe en el pipeline. No bloquea esta entrega porque Open-Meteo ya cubre las mismas variables para la Ciudad de México.

---

## Decisión: usar una ventana de rezago (lag) de 0 a 14 días en el análisis

**Razón:** en series de tiempo de salud ambiental, los efectos agudos de contaminantes gaseosos (O₃, NO₂, SO₂, CO) suelen concentrarse en los primeros 0-5 días, mientras que el material particulado (PM10, PM2.5) y las temperaturas extremas pueden mostrar efectos hasta 2-3 semanas después. Una ventana de 0 a 14 días cubre ambos casos sin exigir una serie histórica más larga de la disponible.

**Alternativas consideradas:** ventanas más cortas (0-7 días) subestimarían efectos tardíos de partículas finas y frío extremo; ventanas más largas (0-28 días) requerirían una serie histórica considerablemente más extensa de la que se dispone hoy (ver limitación de ventana temporal en `docs/project_scope.md`).

**Consecuencias:** el número de rezagos es un parámetro (`REZAGOS_DIAS`) en `src/processing/construir_panel_cdmx.py` y `src/analysis/analisis_rezago.py`, fácil de ajustar si se amplía la ventana temporal de las fuentes.
