# SPEC 04 — Correcciones de contenido y traducción a español

> **Estado:** Aprobado
> **Depende de:** SPEC 02
> **Fecha:** 2026-08-26
> **Objetivo:** Corregir el label incorrecto de la variable target en Home, quitar el paso "WOE Encoding" que no se usó en el pipeline real, traducir a español los títulos/subtítulos/captions/labels del frontend que hoy están en inglés, y quitar la sección "Key Information" de Make Prediction.

---

## Por qué existe este spec

Al revisar el dashboard, el usuario detectó 3 errores/mejoras de contenido puntuales: la card "Target Variable" en Home describe el target como "1 = Delincuente, 0 = Bueno" (incorrecto: debe ser "1 = Default, 0 = No Default"); `PREPROCESSING_PIPELINE` y la tarjeta de Feature Engineering en el Project Workflow mencionan "WOE Encoding (WOEClassic)", técnica que no se usó — el pipeline real usa Log-Odds Rolling Smoothing directamente, sin WOE (confirmado por las columnas `*_log_odds` en `artifacts/feature_engineering/vif.csv` y `feature_correlation.csv`); y varias secciones quedaron en inglés desde SPEC 01/02, pero el público del portafolio es de Perú. Además, pidió quitar "Key Information" del panel de resultado de Make Prediction por no aportar al caso de uso principal.

Se agrupan en un spec porque las 4 piezas son correcciones de contenido/presentación sobre archivos ya existentes, sin introducir lógica ni datos nuevos (a diferencia de SPEC 03).

---

## Scope

**In:**

- `home.py`: card "Target Variable" cambia de `` `SeriousDlqin2yrs` (1 = Delincuente, 0 = Bueno) `` a `` `SeriousDlqin2yrs` (1 = Default, 0 = No Default) ``.
- `home.py`: bullet "Encoding WOE" en la tarjeta "Feature Engineering" de `WORKFLOW_STAGES` → "Log-Odds Rolling Smoothing".
- `dashboard_data.py`: `PREPROCESSING_PIPELINE` pierde la entrada `"WOE Encoding (WOEClassic)"` (queda con 4 pasos: Manejo de outliers, Binning, Log-Odds Rolling Smoothing, Selección de features).
- `make_prediction.py`: se elimina por completo el bloque `key_info_col` ("Key Information" + Model Type/Target/Evaluation Metric/Best AUC/Default Rate/Población); el resultado (`result_col`) pasa a usar el ancho completo de la página.
- Traducción a español de títulos (`st.subheader`/`st.title`), captions (`st.caption`) y labels de tarjeta (`st.markdown("**...**")`) en `layout.py`, `app.py` (títulos de página en el sidebar), `home.py`, `eda.py`, `feature_engineering.py`, `model_training.py`, `model_evaluation.py`, `monitoring.py`, `make_prediction.py` — ver el mapa completo en [Data model](#data-model).
- Traducción de los 10 labels del formulario de predicción (`st.number_input`) y del botón "Predict Probability".
- Se mantienen sin traducir las siglas/jerga técnica estándar: AUC, PSI, IV, SHAP, ROC, VIF, KS, Lift, CatBoost, Optuna, Feature Engineering, Dataset, EDA.

**Out of scope (para futuros specs):**

- Encabezados de columna dentro de `st.dataframe` (llaves de los diccionarios en `dashboard_data.py`, reutilizadas por los gráficos Plotly) — quedan como están, decisión explícita del usuario.
- Cualquier contenido de SPEC 03 (artefactos nuevos, SHAP waterfall) — este spec no toca esas secciones.
- Cambios al backend — la corrección del target y el idioma son puramente de presentación en el frontend.
- Traducción literal de la jerga técnica acordada como estándar (ver Scope In).

---

## Data model

Este spec no introduce estructuras de datos nuevas. Modifica strings existentes (labels, títulos, captions) en `frontend/src/pages/*.py`, `frontend/src/app.py` y `frontend/src/layout.py`, y elimina una entrada de la lista `PREPROCESSING_PIPELINE` en `dashboard_data.py`.

Mapa de traducción (antes → después), para que la implementación no tenga que inventar redacciones:

**`app.py` (títulos de página en el sidebar):**

| Antes | Después |
| --- | --- |
| Home | Inicio |
| EDA | EDA *(sin cambio)* |
| Feature Engineering | Feature Engineering *(sin cambio)* |
| Model Training | Entrenamiento del Modelo |
| Model Evaluation | Evaluación del Modelo |
| Monitoring | Monitoreo |
| Make Prediction | Realizar Predicción |

**`layout.py`:** caption "End-to-End ML System for Credit Risk Prediction" → "Sistema de Machine Learning de extremo a extremo para predicción de riesgo crediticio".

**`home.py`:** "Project Overview" → "Resumen del Proyecto"; "Business Goal" → "Objetivo de Negocio"; "Target Variable" → "Variable Objetivo"; "Models Evaluated" → "Modelos Evaluados"; "Best Model" → "Mejor Modelo"; "Project Workflow – 5 Stages" → "Flujo del Proyecto – 5 Etapas". ("Dataset", "Pipeline de Preprocessing", "Clasificación Económica", "¿Por qué CatBoost?" quedan igual.)

**`eda.py`:** "EDA - Exploratory Data Analysis" → "EDA - Análisis Exploratorio de Datos"; "Overview" → "Resumen General"; "Target Balance" → "Balance del Target"; "Missing Values" → "Valores Faltantes". (Los demás subtítulos de esta página ya están en español.)

**`model_training.py`:** "Model Training" → "Entrenamiento del Modelo"; "Model Performance Summary" → "Resumen de Desempeño del Modelo"; caption "Best Model: ..." → "Mejor Modelo: ..."; "AUC Over Time (OOT)" → "AUC en el Tiempo (OOT)"; caption "Stable performance over time" → "Desempeño estable en el tiempo"; "Feature Importance (Top 10)" → "Importancia de Variables (Top 10)"; "Calibration Curve" → "Curva de Calibración".

**`model_evaluation.py`:** "Model Evaluation" → "Evaluación del Modelo". (Los demás subtítulos ya están en español.)

**`monitoring.py`:** "Monitoring" → "Monitoreo"; "Data Drift (PSI)" → "Drift de Datos (PSI)"; "Target Drift" → "Drift del Target".

**`make_prediction.py`:** "Make Prediction" → "Realizar Predicción"; "Prediction Result" → "Resultado de la Predicción"; "Key Information" → *(sección eliminada, ver Scope)*. Labels del formulario:

| Antes | Después |
| --- | --- |
| Revolving Utilization Of Unsecured Lines | Utilización Rotativa de Líneas No Aseguradas |
| Age | Edad |
| Number Of Time 30-59 Days Past Due Not Worse | N° de Veces con 30-59 Días de Atraso |
| Debt Ratio | Ratio de Endeudamiento |
| Monthly Income | Ingreso Mensual |
| Number Of Open Credit Lines And Loans | N° de Líneas de Crédito y Préstamos Abiertos |
| Number Of Times 90 Days Late | N° de Veces con 90 Días de Atraso |
| Number Real Estate Loans Or Lines | N° de Préstamos o Líneas Hipotecarias |
| Number Of Time 60-89 Days Past Due Not Worse | N° de Veces con 60-89 Días de Atraso |
| Number Of Dependents | N° de Dependientes |
| *(botón)* Predict Probability | Calcular Probabilidad |

---

## Implementation plan

1. `dashboard_data.py`: quitar la entrada `"WOE Encoding (WOEClassic)"` de `PREPROCESSING_PIPELINE` (queda con 4 pasos). Test: `python3 -c "from dashboard_data import PREPROCESSING_PIPELINE; print(len(PREPROCESSING_PIPELINE))"` imprime `4`.
2. `home.py`: corregir la card "Target Variable" y el bullet "Encoding WOE" → "Log-Odds Rolling Smoothing" en `WORKFLOW_STAGES`; traducir los títulos listados en [Data model](#data-model). Test manual visual.
3. `layout.py`: traducir el caption del header. Test manual visual.
4. `app.py`: traducir los títulos de página del `st.navigation` según el mapa. Test manual: el sidebar muestra los 7 nombres nuevos.
5. `eda.py`: traducir los 4 subtítulos listados. Test manual visual.
6. `model_training.py`: traducir título, subtítulos y captions listados. Test manual visual.
7. `model_evaluation.py`: traducir el título de la página. Test manual visual.
8. `monitoring.py`: traducir título y subtítulos listados. Test manual visual.
9. `make_prediction.py`: traducir título, "Prediction Result", los 10 labels del formulario y el botón; eliminar por completo el bloque `key_info_col`, dejando el resultado en el ancho disponible. Test manual: con backend real corriendo, completar el formulario en español y confirmar que "Key Information" ya no aparece.
10. Verificación final: `streamlit run frontend/src/app.py`, recorrer las 7 páginas, confirmar que no queda texto en inglés salvo la jerga técnica acordada, y que "Key Information" ya no existe. Checklist de [Acceptance criteria](#acceptance-criteria).

---

## Acceptance criteria

- [ ] `home.py` muestra "1 = Default, 0 = No Default" en la card "Variable Objetivo".
- [ ] `PREPROCESSING_PIPELINE` tiene 4 pasos (sin "WOE Encoding"); el bullet correspondiente en el Project Workflow dice "Log-Odds Rolling Smoothing".
- [ ] `make_prediction.py` ya no muestra la sección "Key Information" en ningún estado (con o sin predicción realizada).
- [ ] El sidebar de navegación muestra los 7 nombres de página según el mapa de [Data model](#data-model).
- [ ] Los 10 labels del formulario de predicción y el botón están en español según el mapa.
- [ ] Ningún `st.subheader`/`st.title`/`st.caption` visible queda en inglés, excepto AUC, PSI, IV, SHAP, ROC, VIF, KS, Lift, CatBoost, Optuna, Feature Engineering, Dataset, EDA.
- [ ] `streamlit run frontend/src/app.py` levanta sin errores en consola tras estos cambios.
- [ ] Con el backend real corriendo, el flujo completo de Make Prediction (formulario en español → resultado) sigue funcionando end-to-end.

---

## Decisions

- **Sí:** se mantienen sin traducir las siglas/jerga técnica estándar (AUC, PSI, IV, SHAP, ROC, VIF, KS, Lift, CatBoost, Optuna, Feature Engineering, Dataset, EDA) — decisión explícita del usuario, es como se usan en la práctica en español técnico.
- **Sí:** se traduce el sidebar de navegación — decisión explícita del usuario.
- **No:** no se traducen los encabezados de columna de `st.dataframe` — son las llaves de los diccionarios en `dashboard_data.py`, reutilizadas también por los gráficos Plotly; renombrarlas es un cambio más grande que el usuario decidió dejar fuera de esta pasada.
- **Sí:** el bullet "Encoding WOE" en `home.py` se reemplaza por "Log-Odds Rolling Smoothing" en vez de eliminarse sin reemplazo — mantiene 4 bullets en la tarjeta y refleja la técnica real usada, igual que en `PREPROCESSING_PIPELINE`.
- **Sí:** "Key Information" se elimina por completo, no se traduce y se deja — decisión explícita del usuario ("eso no es necesario").
- **No:** no se toca la sección del SHAP waterfall en `make_prediction.py` — es contenido nuevo de SPEC 03; este spec solo quita Key Information y traduce labels existentes.

---

## Risks

| Riesgo | Mitigación |
| --- | --- |
| SPEC 03 y este spec modifican `make_prediction.py` (SPEC 03 agrega el waterfall, este quita Key Information y traduce labels) | No hay dependencia funcional entre ambos cambios; al implementar, aplicar primero el que se apruebe antes y rebasear/mergear el otro sobre esa base |

---

## What is **not** in this spec

- Encabezados de columna en tablas (`st.dataframe`).
- SHAP waterfall y artefactos nuevos de `artifacts/` (SPEC 03).
- Cambios al backend.

Cada uno de estos, si se necesita, va en su propio spec.
