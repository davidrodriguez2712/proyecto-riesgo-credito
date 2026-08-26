# SPEC 03 — Artefactos reales del pipeline y SHAP waterfall por cliente

> **Estado:** Aprobado
> **Depende de:** SPEC 02
> **Fecha:** 2026-08-26
> **Objetivo:** Incorporar a sus páginas correspondientes los artefactos reales (tablas y gráficos) que ahora existen en `artifacts/feature_engineering`, `artifacts/model_evaluation`, `artifacts/training_model` y `artifacts/monitoring`, y agregar en Make Prediction un SHAP waterfall que explique, para el cliente recién predicho, qué features empujaron su PD hacia arriba o hacia abajo.

---

## Por qué existe este spec

SPEC 01/02 dejaron varias páginas con datos extraídos a mano de la salida impresa de los notebooks (`MODEL_COMPARISON`, `PORTFOLIO_MANAGEMENT`, etc.) y dos placeholders explícitos (Feature Importance, Score Distribution) porque no existían artefactos exportados. Desde entonces se generaron y guardaron artefactos reales en `artifacts/feature_engineering/`, `artifacts/model_evaluation/`, `artifacts/training_model/` y `artifacts/monitoring/` (CSVs y PNGs), que hoy no se muestran en ningún lado del frontend.

Además, Make Prediction hoy solo devuelve `pd_estimada` y `banda_riesgo` — útil para decidir, pero no explica *por qué* un cliente cae en esa banda. Para un portafolio de credit risk, mostrar la contribución de cada feature a la decisión (interpretabilidad a nivel de cliente individual, no solo a nivel de modelo) es una pieza de valor que hoy falta.

---

## Scope

**In:**

- `frontend/src/dashboard_data.py`: nuevas constantes `FEATURE_SELECTION_RULES`, `FEATURE_ENGINEERING_EVALUATION`, `VIF_TABLE`, `FE_FIGURES` (desde `artifacts/feature_engineering/`), `MODEL_EVALUATION_FIGURES` (desde `artifacts/model_evaluation/`), `MONITORING_FIGURES` (desde `artifacts/monitoring/`).
- `pages/feature_engineering.py`: 3 tablas nuevas (`feature_selection.csv`, `feature_engineering_evaluation.csv`, `vif.csv`) + la imagen `logit_vs_feature_values.png`, debajo del pipeline de pasos ya existente.
- `pages/model_evaluation.py`: las 4 imágenes de `MODEL_EVALUATION_FIGURES` (SHAP importance, SHAP individual importance, distribución buenos/malos por decil, relación SHAP vs valores de features), cada una con caption "gráfico original de `04_model_evaluation.ipynb`".
- `pages/model_training.py`: un caption bajo el gráfico Feature Importance existente, apuntando al gráfico SHAP real en Model Evaluation (ambos conviven, ninguno reemplaza al otro).
- `pages/monitoring.py`: las 12 imágenes de `artifacts/monitoring/`, agrupadas en 4 secciones temáticas (Performance, Drift, SHAP, Calibración), debajo del contenido ya existente (PSI/Target Drift). Se confirma con `performance_temporal.csv` que `MONITORING_AUC_GINI` ya es correcto — no cambia, solo se deja constancia.
- `artifacts/training_model/model_comparison_inicial_cv.csv` confirma que `MODEL_COMPARISON` ya es correcto — no requiere cambios de página, solo se deja constancia (no hay contenido visual nuevo en esa carpeta: los demás archivos son `.pkl`).
- Backend (`backend/src/services/model_services.py`, `backend/src/api/routes/predict.py`, `backend/src/models/schemas.py`): un `shap.TreeExplainer` sobre el `CatBoostClassifier` ya cargado, que calcula la contribución de cada feature a la PD del cliente predicho.
- `POST /api/v1/predict` devuelve dos campos nuevos: `shap_contributions` (lista de hasta 7 entradas: top 6 features + "Otras features") y `base_pd` (PD base del modelo antes de aplicar las features del cliente).
- `pages/make_prediction.py`: un waterfall Plotly (`go.Waterfall`) debajo del resultado coloreado existente, construido con `base_pd`, `shap_contributions` y `pd_estimada`.

**Out of scope (para futuros specs):**

- Quitar la sección "Key Information" de Make Prediction — es una limpieza de contenido, va en SPEC 04.
- Traducción a español de títulos/subtítulos/labels — va en SPEC 04.
- Corrección del label del target ("1 = Delincuente") y remoción del paso "WOE Encoding" de `PREPROCESSING_PIPELINE` — va en SPEC 04.
- `shap.TreeExplainer(model, data=..., model_output="probability")` (SHAP nativo en espacio de probabilidad) — requeriría vendorizar una muestra del training set dentro del backend solo para eso; se logra el mismo resultado con la conversión manual descrita en [Data model](#data-model), sin ese artefacto nuevo.
- Endpoint `/predict/explain` separado — el desglose SHAP viaja en la misma respuesta de `/predict`.
- Cache o persistencia de explicaciones SHAP pasadas — cada submit recalcula desde cero.
- Cambios a los thresholds de `clasificar_cliente()`.

---

## Data model

Nuevas constantes en `frontend/src/dashboard_data.py`, con datos reales de los CSVs:

```python
FEATURE_SELECTION_RULES = [
    {"feature": "RevolvingUtilizationOfUnsecuredLines", "roc_auc": 0.778, "gini": 0.556, "missing_pct": 0.0, "regla": "Mantener"},
    {"feature": "NumberOfTime30-59DaysPastDueNotWorse", "roc_auc": 0.690, "gini": 0.379, "missing_pct": 0.0, "regla": "Mantener"},
    {"feature": "NumberOfTimes90DaysLate", "roc_auc": 0.657, "gini": 0.314, "missing_pct": 0.0, "regla": "Mantener"},
    {"feature": "NumberOfTime60-89DaysPastDueNotWorse", "roc_auc": 0.622, "gini": 0.243, "missing_pct": 0.0, "regla": "Mantener"},
    {"feature": "NumberOfDependents", "roc_auc": 0.547, "gini": 0.094, "missing_pct": 0.02616, "regla": "Mantener"},
    {"feature": "DebtRatio", "roc_auc": 0.524, "gini": 0.048, "missing_pct": 0.0, "regla": "Mantener"},
    {"feature": "NumberRealEstateLoansOrLines", "roc_auc": 0.463, "gini": -0.075, "missing_pct": 0.0, "regla": "Revisar"},
    {"feature": "NumberOfOpenCreditLinesAndLoans", "roc_auc": 0.455, "gini": -0.089, "missing_pct": 0.0, "regla": "Revisar"},
    {"feature": "MonthlyIncome", "roc_auc": 0.424, "gini": -0.152, "missing_pct": 0.198207, "regla": "Eliminar"},
    {"feature": "age", "roc_auc": 0.365, "gini": -0.271, "missing_pct": 0.0, "regla": "Revisar"},
]  # fuente: artifacts/feature_engineering/feature_selection.csv

FEATURE_ENGINEERING_EVALUATION = [
    {"feature": "RevolvingUtilizationOfUnsecuredLines", "funcion": "polynomial_1", "auc_train": 0.777888, "auc_val": 0.777486, "r2": 0.887166},
    {"feature": "NumberOfTime30-59DaysPastDueNotWorse", "funcion": "polynomial_1", "auc_train": 0.686970, "auc_val": 0.695416, "r2": 0.787866},
    {"feature": "NumberOfTime60-89DaysPastDueNotWorse", "funcion": "polynomial_1", "auc_train": 0.622201, "auc_val": 0.620665, "r2": 0.824595},
    {"feature": "NumberOfTimes90DaysLate", "funcion": "polynomial_1", "auc_train": 0.659081, "auc_val": 0.652470, "r2": 0.766860},
    {"feature": "age", "funcion": "polynomial_1", "auc_train": 0.630955, "auc_val": 0.645652, "r2": 0.820277},
    {"feature": "NumberOfDependents", "funcion": "polynomial_1", "auc_train": 0.545507, "auc_val": 0.549962, "r2": 0.418343},
    {"feature": "NumberRealEstateLoansOrLines", "funcion": "polynomial_1", "auc_train": 0.536094, "auc_val": 0.540528, "r2": 0.078617},
    {"feature": "NumberOfOpenCreditLinesAndLoans", "funcion": "polynomial_1", "auc_train": 0.546330, "auc_val": 0.539902, "r2": 0.077480},
    {"feature": "MonthlyIncome", "funcion": "logarithmic", "auc_train": 0.574984, "auc_val": 0.578731, "r2": 0.020552},
    {"feature": "DebtRatio", "funcion": "polynomial_1", "auc_train": 0.477167, "auc_val": 0.473647, "r2": 0.060358},
]  # fuente: artifacts/feature_engineering/feature_engineering_evaluation.csv

VIF_TABLE = [
    {"feature": "NumberOfOpenCreditLinesAndLoans_log_odds", "vif": 1.272831},
    {"feature": "NumberRealEstateLoansOrLines_log_odds", "vif": 1.269276},
    {"feature": "NumberOfDependents_log_odds", "vif": 1.124942},
    {"feature": "MonthlyIncome_log_odds", "vif": 1.122312},
    {"feature": "age_log_odds", "vif": 1.104787},
    {"feature": "DebtRatio_log_odds", "vif": 1.070102},
    {"feature": "NumberOfTime30-59DaysPastDueNotWorse_log_odds", "vif": 1.006762},
    {"feature": "RevolvingUtilizationOfUnsecuredLines_log_odds", "vif": 1.000333},
]  # fuente: artifacts/feature_engineering/vif.csv — solo 8 features (las de conteo con VIF colineal quedaron fuera del cálculo)

FE_FIGURES = {
    "logit_vs_feature_values": "artifacts/feature_engineering/logit_vs_feature_values.png",
}

MODEL_EVALUATION_FIGURES = {
    "shap_importance": "artifacts/model_evaluation/SHAP importance.png",
    "shap_individual_importance": "artifacts/model_evaluation/shap individual importance.png",
    "dist_buenos_malos_decil": "artifacts/model_evaluation/dist_buenos_malos_decil.png",
    "relacion_shap_features_values": "artifacts/model_evaluation/relacion_shap_features_values.png",
}

MONITORING_FIGURES = {
    "performance": [
        "artifacts/monitoring/curva_roc_monitoreo.png",
        "artifacts/monitoring/monitorinc_auc.png",
        "artifacts/monitoring/monitoreo_pd_br.png",
    ],
    "drift": [
        "artifacts/monitoring/evolutivo_psi_features.png",
        "artifacts/monitoring/psi_features.png",
        "artifacts/monitoring/iqr_features.png",
        "artifacts/monitoring/porcentaje_missing_feature.png",
    ],
    "shap": [
        "artifacts/monitoring/evolutivo_shap.png",
        "artifacts/monitoring/variacion_contribution_shap.png",
    ],
    "calibracion": [
        "artifacts/monitoring/calibration_curve_monitoring.png",
        "artifacts/monitoring/curva_calibracion_post_platt_scaling.png",
        "artifacts/monitoring/intervalos_vasicek.png",
    ],
}
# Rutas relativas a la raíz del proyecto, igual que EDA_FIGURES (SPEC 02); se resuelven con
# Path(__file__).resolve().parents[3] desde cada página, igual que ya hace pages/eda.py.
```

**Algoritmo del SHAP waterfall (backend)** — validado en este entorno con `shap==0.52.0` sobre el `CatBoostClassifier` real (`backend/src/ml/artifacts/model.pkl`): `shap.TreeExplainer(model).shap_values(x)` devuelve un array `(1, 10)` en espacio margin/log-odds, y `explainer.expected_value` es un escalar (`base_value`). Se confirmó que `sigmoid(base_value + shap_values.sum())` reproduce `predict_proba` exacto (mismos dígitos flotantes).

Con eso, `ModelService.explain(features: dict) -> dict`:

1. Calcula `shap_values` (10 valores, uno por feature, en margin/log-odds) y `base_value`.
2. Ordena las features por `|shap_value|` descendente; toma las 6 primeras, agrupa el resto en un bucket `"Otras features"` (suma de sus `shap_value`).
3. Recorre esa secuencia de 7 pasos acumulando `running_margin` desde `base_value`; en cada paso, `contribucion_pp = sigmoid(running_margin_after) - sigmoid(running_margin_before)`. Esto garantiza que `base_pd + Σ contribucion_pp == pd_estimada` exacto (no es una aproximación: es la misma cantidad, solo repartida paso a paso vía la función sigmoide).
4. `base_pd = sigmoid(base_value)`.

`backend/src/models/schemas.py` — `PredictionOutput` extendido:

```python
class ShapContribution(BaseModel):
    feature: str
    valor_cliente: float | None  # None para el bucket "Otras features"
    contribucion_pp: float

class PredictionOutput(BaseModel):
    pd_estimada: float
    banda_riesgo: str
    version_modelo: str
    base_pd: float
    shap_contributions: list[ShapContribution]
```

---

## Implementation plan

1. Agregar a `frontend/src/dashboard_data.py` las 6 constantes nuevas del [Data model](#data-model). Test manual: `cd frontend/src && python3 -c "from dashboard_data import FEATURE_SELECTION_RULES, FEATURE_ENGINEERING_EVALUATION, VIF_TABLE, FE_FIGURES, MODEL_EVALUATION_FIGURES, MONITORING_FIGURES; print(len(FEATURE_SELECTION_RULES), len(VIF_TABLE), len(MONITORING_FIGURES['drift']))"` imprime `10 8 4`.
2. `pages/feature_engineering.py`: agregar las 3 tablas (`st.dataframe`) + la imagen `logit_vs_feature_values.png` debajo del pipeline existente. Test manual visual.
3. `pages/model_evaluation.py`: agregar las 4 imágenes de `MODEL_EVALUATION_FIGURES` con caption de fuente. Test manual visual.
4. `pages/model_training.py`: agregar un `st.caption` bajo el gráfico Feature Importance apuntando al gráfico SHAP real en Model Evaluation. Test manual visual.
5. `pages/monitoring.py`: agregar las 4 secciones temáticas con las 12 imágenes de `MONITORING_FIGURES`, debajo de PSI/Target Drift. Test manual visual: se ven las 12 imágenes agrupadas.
6. `backend/src/services/model_services.py`: construir `shap.TreeExplainer(self.model_path)` una sola vez (mismo objeto cacheado que el modelo) y agregar `explain(features: dict) -> dict` con el algoritmo descrito arriba. Test manual: script suelto con el payload de ejemplo (`RevolvingUtilizationOfUnsecuredLines=0.5, age=35, ...`) verificando `abs(base_pd + sum(contribuciones) - pd_estimada) < 1e-6`.
7. `backend/src/models/schemas.py` + `backend/src/api/routes/predict.py`: extender `PredictionOutput` con `base_pd`/`shap_contributions`, y en el endpoint llamar a `service.explain(...)` además de `service.predict(...)`. Test manual: `curl -X POST http://localhost:8082/api/v1/predict -d '{...}'` devuelve `shap_contributions` con 7 entradas y `base_pd`.
8. `pages/make_prediction.py`: construir el `go.Waterfall` (measure `["absolute"] + ["relative"]*7 + ["total"]`) debajo del resultado coloreado, usando `base_pd`, `shap_contributions` y `pd_estimada` de la respuesta. Test manual: con backend real corriendo, completar el formulario y ver el waterfall, con la barra final igual al `pd_estimada` mostrado arriba.
9. Verificación final: `streamlit run frontend/src/app.py` con backend real, recorrer Feature Engineering, Model Evaluation, Model Training, Monitoring y Make Prediction sin errores en consola. Checklist de [Acceptance criteria](#acceptance-criteria).

---

## Acceptance criteria

- [ ] Feature Engineering muestra las 3 tablas nuevas (`feature_selection`, `feature_engineering_evaluation`, `vif`) y la imagen `logit_vs_feature_values.png`, debajo del pipeline existente.
- [ ] Model Evaluation muestra las 4 imágenes de `MODEL_EVALUATION_FIGURES`, cada una con caption indicando que es el gráfico original del notebook.
- [ ] Model Training conserva su gráfico de Feature Importance y agrega un caption apuntando al gráfico SHAP real en Model Evaluation.
- [ ] Monitoring muestra las 12 imágenes de `artifacts/monitoring/` agrupadas en 4 secciones (Performance, Drift, SHAP, Calibración), debajo del contenido ya existente.
- [ ] `POST /api/v1/predict` devuelve `shap_contributions` (hasta 7 entradas) y `base_pd`, además de los 3 campos existentes.
- [ ] Para un mismo payload, `base_pd + Σ contribucion_pp` coincide con `pd_estimada` con tolerancia `1e-6`.
- [ ] Make Prediction muestra un waterfall Plotly debajo del resultado, cuya barra final coincide con el `pd_estimada` mostrado en el resultado coloreado.
- [ ] `streamlit run frontend/src/app.py` levanta sin errores en consola tras estos cambios.
- [ ] `docker build` del backend sigue funcionando sin error (no se agregan dependencias nuevas: `shap` ya estaba en `requirements.txt`).

---

## Decisions

- **Sí:** SHAP en espacio margin/log-odds vía `TreeExplainer` path-dependent, sin background dataset — validado en este entorno que reconstruye `predict_proba` exacto. Evita vendorizar una muestra de training data como artefacto nuevo del backend.
- **No:** `shap.TreeExplainer(model, data=..., model_output="probability")` — el mismo resultado en puntos porcentuales se logra con la conversión manual (sigmoide acumulada), sin esa dependencia extra.
- **Sí:** top 6 features + bucket "Otras features" — balance entre legibilidad para un cliente no técnico y que el total siga sumando exacto.
- **Sí:** unidades en puntos porcentuales de PD (pp) — decisión explícita del usuario, más intuitivo que log-odds para el público objetivo.
- **Sí:** `shap_contributions`/`base_pd` viajan en la misma respuesta de `/predict` — decisión explícita del usuario, evita una segunda llamada de red.
- **Sí:** cálculo de SHAP en el backend, no en el frontend — evita agregar `catboost`+`shap` a `frontend/requirements.txt` (hoy solo tiene `streamlit`/`requests`/`pandas`/`plotly`).
- **Sí:** el PNG del SHAP importance real convive con el bar chart Plotly ya existente en Model Training (no se reemplaza) — decisión explícita del usuario, ambos son datos reales y no se contradicen.
- **Sí:** `model_comparison_inicial_cv.csv` y `performance_temporal.csv` solo se usan para *confirmar* que `MODEL_COMPARISON`/`MONITORING_AUC_GINI` ya eran correctos — no generan cambios de página, para no introducir números duplicados de la misma fuente.

---

## Risks

| Riesgo | Mitigación |
| --- | --- |
| Los nombres de archivo en `artifacts/model_evaluation/` tienen espacios (`"SHAP importance.png"`) | Se referencian como string completo en `dashboard_data.py`; `st.image()` los abre igual, solo hay que evitar asumir snake_case al construir las rutas |
| `shap.TreeExplainer` puede devolver `expected_value`/`shap_values` con shapes distintas según la versión de la librería (escalar vs. arreglo de 2 clases) | Ya validado en este entorno (`shap==0.52.0` + `CatBoostClassifier`): `expected_value` escalar, `shap_values` con shape `(1,10)`. Si se reentrena con otra versión de `shap`, `explain()` debe normalizar la forma antes de usarla |
| Calcular SHAP en cada request de `/predict` agrega latencia | No hay SLA de latencia definido para este proyecto de portafolio; el explainer se construye una sola vez (cacheado), no por request |

---

## What is **not** in this spec

- Quitar "Key Information" de Make Prediction (SPEC 04).
- Traducción a español de títulos/subtítulos/labels (SPEC 04).
- Corrección del label del target y remoción del paso WOE de `PREPROCESSING_PIPELINE` (SPEC 04).
- SHAP nativo en espacio de probabilidad con background dataset vendorizado.
- Endpoint `/predict/explain` separado.
- Cambios a los thresholds de `clasificar_cliente()`.

Cada uno de estos, si se necesita, va en su propio spec.
