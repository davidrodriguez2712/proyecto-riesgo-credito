# SPEC 02 — Multi-page real y enriquecimiento del Overview

> **Estado:** Implementado
> **Depende de:** SPEC 01
> **Fecha:** 2026-08-25
> **Objetivo:** Reestructurar el frontend Streamlit a multi-page real (`st.navigation`) con sidebar clickeable, y enriquecer el Overview con la clasificación económica (gestión de portafolio), el pipeline de preprocessing (WOE + log-odds rolling) y la nota de selección de modelo, quitando el branding de Kaggle y corrigiendo las tarjetas truncadas.

---

## Por qué existe este spec

SPEC 01 dejó una app Streamlit de una sola vista scrolleable, con el sidebar mayormente informativo (decisión explícita: "sin `st.navigation`/carpeta `pages/`"). Al usarla, surgieron 4 pedidos de mejora sobre esa base ya implementada:

1. El sidebar debe ser clickeable de verdad (navegación real, no solo scroll), lo que reabre esa decisión de SPEC 01.
2. El Overview debe destacar dos piezas de trabajo real que hoy no se ven: la gestión de portafolio con la que se validaron los thresholds de riesgo (`clasificar_cliente()` en el backend) y el pipeline de preprocessing (WOE + log-odds rolling smoothing).
3. El Overview debe explicar por qué LogisticRegression (AUC CV 0.825) no fue el modelo elegido.
4. Las tarjetas superiores del Overview truncan texto largo (evidenciado en captura de pantalla) y el branding menciona "Kaggle" de más.

Se agrupan en un solo spec porque las 4 piezas modifican el mismo conjunto de archivos (`frontend/src/app.py` y lo que hoy vive ahí).

---

## Scope

**In:**

- Migración de `frontend/src/app.py` de una sola vista a multi-page real con `st.navigation`, con 7 páginas: Home (Overview), EDA, Feature Engineering, Model Training, Model Evaluation, Monitoring, Make Prediction.
- Nuevas constantes reales en `frontend/src/dashboard_data.py`: `DECILE_KS_LIFT`, `PORTFOLIO_MANAGEMENT`, `PREPROCESSING_PIPELINE`, `MODEL_SELECTION_NOTE`.
- Página "Model Evaluation" con la tabla completa de gestión de portafolio (`PORTFOLIO_MANAGEMENT`) y la tabla de deciles/KS/Lift por banda (`DECILE_KS_LIFT`).
- Página "Feature Engineering" con el detalle del pipeline de preprocessing (`PREPROCESSING_PIPELINE`), incluyendo la explicación de Log-Odds Rolling Smoothing.
- Página "EDA" narrativa/descriptiva (sin datos exportados todavía).
- Overview (Home) rediseñado: tarjetas multi-línea sin truncar, sin mencionar "Kaggle", más 3 highlights: resumen del pipeline de preprocessing, resumen de gestión de portafolio, y `MODEL_SELECTION_NOTE`.
- Migración de las secciones ya existentes de SPEC 01 (Model Performance Summary, AUC Over Time, Feature Importance/Score Distribution placeholders, Data Drift PSI, Target Drift, Make Prediction) a sus páginas correspondientes, sin cambiar su comportamiento.
- `frontend/src/layout.py` con un helper de header compartido entre páginas.

**Out of scope (para futuros specs):**

- Datos reales de EDA (missings, outliers, IV) — la página EDA sigue siendo narrativa, no de datos.
- Cambios al backend o a los thresholds de `clasificar_cliente()` — este spec solo muestra los datos que ya sustentan esos thresholds, no los recalcula ni los modifica.
- Diagrama visual del pipeline de preprocessing — se muestra como texto/tabla, no como diagrama gráfico.
- Feature Importance Top 10 y Score Distribution con datos reales — siguen como placeholder (ver SPEC 01).
- TLS, dominio, docker-compose — sigue fuera de alcance (ver SPEC 01).
- Predicción batch, reportes PDF reales — sigue fuera de alcance (ver SPEC 01).

---

## Data model

Cuatro constantes nuevas en `frontend/src/dashboard_data.py`, con datos reales extraídos de `notebooks/03_training_model.ipynb` y `notebooks/04_model_evaluation.ipynb`:

```python
DECILE_KS_LIFT = [
    {"banda": "Bajo Riesgo", "bad_rate_pct": 0.6, "lift": 0.1, "ks_pct": 29.4},
    {"banda": "Medio Riesgo", "bad_rate_pct": 1.9, "lift": 0.3, "ks_pct": 52.2},
    {"banda": "Alto Riesgo", "bad_rate_pct": 7.3, "lift": 1.1, "ks_pct": 49.1},
    {"banda": "Muy Alto Riesgo", "bad_rate_pct": 37.3, "lift": 5.6, "ks_pct": 0.0},
]  # fuente: notebooks/04_model_evaluation.ipynb, tanteo_deciles() — mismas bandas que clasificar_cliente() en el backend

PORTFOLIO_MANAGEMENT = [
    {"segmento": "Bajo Riesgo", "saldo": "S/282.6M", "participacion_pct": 32.6, "tasa_activa_pct": 14.0,
     "spread_pct": 7.5, "provisiones": "S/2.1M", "provisiones_margen_pct": 9.9, "gastos": "S/0.16M",
     "utilidad_neta": "S/13.3M", "roa_pct": 4.7},
    {"segmento": "Medio Riesgo", "saldo": "S/261.3M", "participacion_pct": 30.1, "tasa_activa_pct": 18.0,
     "spread_pct": 11.5, "provisiones": "S/2.3M", "provisiones_margen_pct": 7.6, "gastos": "S/0.15M",
     "utilidad_neta": "S/19.3M", "roa_pct": 7.4},
    {"segmento": "Alto Riesgo", "saldo": "S/251.3M", "participacion_pct": 28.9, "tasa_activa_pct": 28.0,
     "spread_pct": 21.5, "provisiones": "S/7.5M", "provisiones_margen_pct": 13.9, "gastos": "S/0.14M",
     "utilidad_neta": "S/32.5M", "roa_pct": 12.9},
    {"segmento": "Muy Alto Riesgo", "saldo": "S/73.0M", "participacion_pct": 8.4, "tasa_activa_pct": 35.0,
     "spread_pct": 28.5, "provisiones": "S/24.8M", "provisiones_margen_pct": 119.2, "gastos": "S/0.04M",
     "utilidad_neta": "S/-2.8M", "roa_pct": -3.9},
]  # fuente: notebooks/04_model_evaluation.ipynb, gestion_portafolio() — con este análisis se validaron los thresholds de banda del backend

PREPROCESSING_PIPELINE = [
    {"paso": "Manejo de outliers", "detalle": "Capado IQR/percentil por variable numérica antes del binning."},
    {"paso": "Binning", "detalle": "Discretización de cada variable en bins monotónicos respecto al target."},
    {"paso": "WOE Encoding (WOEClassic)", "detalle": "Cada bin se reemplaza por su Weight of Evidence respecto a SeriousDlqin2yrs."},
    {"paso": "Log-Odds Rolling Smoothing", "detalle": "Suavizado por rolling window del log-odds en bins con pocas observaciones, para estabilizar el WOE antes de usarlo como feature."},
    {"paso": "Selección de features", "detalle": "Filtro por correlación, VIF, Information Value, PSI y Gini univariado; subset final fijado por FeatureSelector."},
]  # fuente: Feature_Engineering/utils/transformers/woe.py (WOEClassic, Logit_Smoothing_Rolling) y selection/feature_selector.py

MODEL_SELECTION_NOTE = (
    "LogisticRegression alcanzó un AUC (CV) de 0.825, competitivo y más interpretable, "
    "pero no fue el modelo elegido: CatBoost (0.864) y LightGBM (0.865) tuvieron mejor "
    "poder predictivo en la comparación de 6 modelos, por lo que CatBoost se seleccionó "
    "como campeón de producción."
)  # fuente: notebooks/03_training_model.ipynb, MODEL_COMPARISON
```

Estructura de archivos nueva (reemplaza el `app.py` monolítico de SPEC 01):

```
frontend/src/
  app.py                     # entrypoint: page config + st.navigation([...]) + .run()
  layout.py                  # render_header(): título "Credit Risk Project – Give Me Credit" + badge, sin "Kaggle"
  config.py                  # sin cambios (SPEC 01)
  api_client.py              # sin cambios (SPEC 01)
  dashboard_data.py          # + las 4 constantes de arriba
  pages/
    home.py                  # Overview: tarjetas multi-línea + 3 highlights + workflow 5 stages
    eda.py                   # narrativo, sin datos exportados
    feature_engineering.py   # detalle de PREPROCESSING_PIPELINE
    model_training.py        # MODEL_COMPARISON + MONITORING_AUC_GINI mensual + placeholders FI/Score (de SPEC 01)
    model_evaluation.py      # PORTFOLIO_MANAGEMENT + DECILE_KS_LIFT
    monitoring.py            # PSI_SNAPSHOT + TARGET_DRIFT (de SPEC 01)
    make_prediction.py       # formulario + predict() + resultado + key info (de SPEC 01)
```

Todos los archivos nuevos importan con el estilo plano (`from dashboard_data import ...`, `from config import ...`, `from api_client import ...`), igual que se corrigió en SPEC 01 — Streamlit inserta el directorio del script (`src/`) en `sys.path`, no el cwd, así que nunca se usa el prefijo `src.` dentro de `src/`.

---

## Implementation plan

1. Agregar a `frontend/src/dashboard_data.py` las 4 constantes nuevas del [Data model](#data-model). Test manual: `cd frontend/src && python3 -c "from dashboard_data import DECILE_KS_LIFT, PORTFOLIO_MANAGEMENT, PREPROCESSING_PIPELINE, MODEL_SELECTION_NOTE; print(len(DECILE_KS_LIFT), len(PORTFOLIO_MANAGEMENT), len(PREPROCESSING_PIPELINE))"` imprime `4 4 5`.
2. Crear `frontend/src/layout.py` con `render_header()`: título "Credit Risk Project – Give Me Credit" (sin "(Kaggle)") + badge "Production", sin mencionar Kaggle en ningún texto. Test manual: `cd frontend/src && python3 -c "from layout import render_header"` no lanza error.
3. Crear los 7 archivos de `frontend/src/pages/` como stubs mínimos (cada uno llama a `render_header()` y muestra `st.subheader("<nombre de la etapa>")`), y reescribir `frontend/src/app.py` para usar `st.navigation([...])` + `.run()`. Test manual: `streamlit run src/app.py` (comando real, sin `-m`) levanta sin error; el sidebar muestra 7 páginas clickeables que navegan sin recargar toda la app.
4. Mover la lógica completa de "Make Prediction" (formulario, `predict()`, resultado coloreado, Key Information) de la versión de `app.py` de SPEC 01 a `pages/make_prediction.py`. Test manual: con backend local en `:8082`, completar el formulario en la página "Make Prediction" y obtener `pd_estimada`/`banda_riesgo` reales.
5. Mover "Model Performance Summary", "AUC Over Time" y los placeholders de "Feature Importance"/"Score Distribution" a `pages/model_training.py`. Test manual visual: la página muestra los 6 modelos y los 12 periodos, igual que en SPEC 01.
6. Mover "Data Drift (PSI)" y "Target Drift" a `pages/monitoring.py`. Test manual visual: igual que en SPEC 01.
7. Construir `pages/model_evaluation.py` con la tabla de `PORTFOLIO_MANAGEMENT` y la tabla `DECILE_KS_LIFT`, con una nota explicando que estos datos sustentan los thresholds de `clasificar_cliente()` del backend. Test manual visual: se muestran los 4 segmentos y las 4 bandas.
8. Construir `pages/feature_engineering.py` con una tarjeta por técnica de `PREPROCESSING_PIPELINE`, incluyendo la explicación de Log-Odds Rolling Smoothing. Test manual visual: se muestran las 5 técnicas.
9. Construir `pages/eda.py` con texto narrativo (qué cubre la etapa: overview, missings, outliers, IV, PSI train/test), marcado explícitamente como "resumen narrativo — sin datos exportados aún del notebook". Test manual visual.
10. Reescribir `pages/home.py`: tarjetas de Business Goal/Target/Dataset/Modelos Evaluados/Best Model como contenedores con `st.markdown` (sin `st.metric`, sin truncar), sin la palabra "Kaggle"; agregar highlight corto de `PREPROCESSING_PIPELINE` (con nota "ver detalle en Feature Engineering"), highlight corto de `PORTFOLIO_MANAGEMENT` (con nota "ver detalle en Model Evaluation"), y `MODEL_SELECTION_NOTE` como callout; conservar las 5 tarjetas de "Project Workflow". Test manual visual: ninguna tarjeta corta texto.
11. Verificación final: `streamlit run src/app.py`, navegar por las 7 páginas sin errores en consola, confirmar que ningún texto visible dice "Kaggle", y repetir la predicción real end-to-end en "Make Prediction". Test manual: checklist de [Acceptance criteria](#acceptance-criteria).

---

## Acceptance criteria

- [ ] `streamlit run frontend/src/app.py` (comando real, sin `-m`) levanta sin errores en consola.
- [ ] El sidebar muestra 7 páginas clickeables (Home, EDA, Feature Engineering, Model Training, Model Evaluation, Monitoring, Make Prediction) que navegan sin error.
- [ ] Ninguna tarjeta del Overview corta o trunca texto.
- [ ] Ningún texto visible en la app menciona "Kaggle"; el proyecto/dataset se referencia como "Give Me Credit".
- [ ] La página "Model Evaluation" muestra los 4 segmentos de `PORTFOLIO_MANAGEMENT` y las 4 bandas de `DECILE_KS_LIFT`.
- [ ] La página "Feature Engineering" muestra las 5 técnicas de `PREPROCESSING_PIPELINE`, incluyendo Log-Odds Rolling Smoothing.
- [ ] El Overview (Home) muestra el highlight del pipeline de preprocessing, el highlight de gestión de portafolio, y `MODEL_SELECTION_NOTE`.
- [ ] La página "Make Prediction" sigue funcionando end-to-end contra el backend real, igual que en SPEC 01.
- [ ] Las páginas "Model Training" y "Monitoring" muestran el mismo contenido que SPEC 01 (6 modelos/12 periodos, PSI/target drift), ahora en páginas propias.
- [ ] La página "EDA" muestra contenido narrativo marcado explícitamente como "sin datos exportados aún".

---

## Decisions

- **Sí:** Un solo spec para las 4 áreas (navegación, contenido, branding, visual) — decisión explícita del usuario; todo modifica el mismo `app.py`/`pages/`.
- **No (revierte SPEC 01):** la decisión de "una sola página, sin multi-page nav" queda descartada. El usuario pidió sidebar clickeable con navegación real, no solo scroll dentro de una vista.
- **Sí:** EDA y Feature Engineering pasan a ser páginas dedicadas nuevas, aunque EDA no tiene datos exportados — se deja como página narrativa explícita en vez de omitirla, para que el sidebar quede completo y honesto sobre qué existe hoy.
- **Sí:** `layout.py` como helper compartido de header — evita duplicar el markup de título/badge en 7 archivos de página.
- **Sí:** Highlight condensado en Home + detalle completo en la página dedicada (para gestión de portafolio y pipeline FE) — cumple "destacar en el overview" sin duplicar tablas completas en dos lugares.
- **Sí:** El highlight y el detalle leen de las mismas constantes de `dashboard_data.py`, para que no se desincronicen si se edita un solo lugar.
- **No:** No se agregan datos reales de EDA (missings/outliers/IV) — la página EDA es narrativa, no de datos, hasta que exista un export real.
- **No:** El pipeline de preprocessing se muestra como texto/tabla, no como diagrama — un diagrama es una mejora visual que puede ir en un spec futuro si se quiere.

---

## Risks

| Riesgo | Mitigación |
| --- | --- |
| El multi-page real cambia la estructura interna de navegación de Streamlit respecto a SPEC 01 | No hay usuarios ni bookmarks reales todavía (el frontend no está desplegado), así que no hay compatibilidad que romper |
| Duplicar contenido (resumen en Home + detalle en página dedicada) puede desincronizarse si se edita solo un lugar | Ambos leen las mismas constantes de `dashboard_data.py` (`PREPROCESSING_PIPELINE`, `PORTFOLIO_MANAGEMENT`); un cambio en la fuente se refleja en los dos lugares automáticamente |

---

## What is **not** in this spec

- Datos reales de EDA (missings, outliers, IV) — la página EDA sigue siendo narrativa.
- Cambios al backend o a los thresholds de `clasificar_cliente()`.
- Diagrama visual del pipeline de preprocessing.
- Feature Importance Top 10 y Score Distribution con datos reales (ver SPEC 01).
- TLS, dominio, docker-compose, predicción batch, reportes PDF reales (ver SPEC 01).

Cada uno de estos, si se necesita, va en su propio spec.
