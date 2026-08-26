# SPEC 01 — Frontend Streamlit del dashboard de credit risk

> **Estado:** Implementado
> **Depende de:** Ninguna
> **Fecha:** 2026-08-25
> **Objetivo:** Construir y desplegar en Docker, de forma independiente al backend, un frontend Streamlit que replique el dashboard de referencia (`design/pantalla_principal.png`) con métricas reales del pipeline y una predicción individual real contra `POST /api/v1/predict`.

---

## Por qué existe este spec

El proyecto ya tiene los 5 notebooks del pipeline terminados y un backend FastAPI funcional (`/api/v1/predict`, `/health`). Falta únicamente el frontend (`frontend/` solo tiene `requirements.txt` y un `Dockerfile` vacío) para poder mostrar el proyecto como pieza de portafolio desplegada en el VPS Contabo.

La imagen de referencia muestra un dashboard con secciones que hoy no tienen datos exportados como tablas reutilizables (`artifacts/eda`, `artifacts/model_evaluation` y `artifacts/monitoring` están vacíos — solo existen `.pkl` de modelos). Durante la definición de este spec se extrajeron números reales directamente de las salidas ya ejecutadas de `notebooks/03_training_model.ipynb`, `04_model_evaluation.ipynb` y `05_monitoring.ipynb` para usarlos como constantes hardcodeadas, en vez de inventar valores de ejemplo. Dos secciones (Feature Importance Top 10 y Score Distribution) no tenían datos tabulares reutilizables (solo gráficos matplotlib/SHAP embebidos) y quedan como placeholder explícito.

---

## Scope

**In:**

- App Streamlit (`frontend/src/app.py`) de una sola vista scrolleable, replicando el orden de secciones de `design/pantalla_principal.png`: header, overview, workflow de 5 etapas, model performance summary, AUC over time, data drift (PSI), target drift, panel de predicción (formulario + resultado + key information).
- Formulario de predicción con los 10 campos exactos de `ClienteInput` (`backend/src/models/schemas.py`), llamando a `POST {BACKEND_URL}/api/v1/predict` y mostrando `pd_estimada`, `banda_riesgo` y `version_modelo` reales.
- Coloreado del resultado según `banda_riesgo` (Bajo/Medio/Alto/Muy Alto Riesgo, los mismos 4 valores que ya devuelve `predict.py`).
- Secciones de métricas con datos reales fijos extraídos de los notebooks (comparación de modelos, AUC/Gini en el tiempo, drift PSI, target drift) — ver [Data model](#data-model).
- Placeholders explícitos y marcados como tales para Feature Importance Top 10 y Score Distribution.
- Botón "Download Project PPT" visible pero deshabilitado (el archivo no existe todavía).
- `frontend/Dockerfile` funcional y `frontend/requirements.txt` ajustado a lo que el frontend realmente usa.
- Configuración de la URL del backend vía variable de entorno `BACKEND_URL`, sin hardcodear IP/host en la imagen Docker.

**Out of scope (para futuros specs):**

- Predicción batch (subir CSV) — el backend no tiene endpoint batch hoy.
- Reportes descargables reales (Technical Report, EDA/Model/Monitoring PDF) — no existen esos archivos.
- Exportar Feature Importance y Score Distribution como datos reales desde los notebooks (requeriría tocar `04_model_evaluation.ipynb` para guardar esas tablas, no solo graficarlas).
- TLS/dominio/reverse proxy (nginx, certbot) — este spec despliega por HTTP plano en IP:puerto.
- docker-compose u orquestación conjunta con el backend — cada contenedor se levanta y administra por separado en el VPS.
- Multi-page navigation de Streamlit (`st.navigation`/carpeta `pages/`) — todo vive en una sola página.
- Actualización automática de las métricas hardcodeadas cuando el modelo se reentrene — hoy es un snapshot fijo.

---

## Data model

Este feature no introduce persistencia ni base de datos. Introduce dos tipos de estructuras nuevas en el frontend: constantes hardcodeadas para las secciones de métricas, y el payload/response que ya define el backend.

`frontend/src/dashboard_data.py` — constantes reales extraídas de los notebooks (snapshot congelado a 2026-08):

```python
MODEL_COMPARISON = [
    # modelo, auc_cv, std_auc, max_auc, min_auc, gini_cv (derivado: 2*auc_cv - 1)
    {"modelo": "LGBMClassifier",        "auc_cv": 0.865, "std_auc": 0.004, "max_auc": 0.869, "min_auc": 0.859},
    {"modelo": "CatBoostClassifier",    "auc_cv": 0.864, "std_auc": 0.003, "max_auc": 0.869, "min_auc": 0.858},
    {"modelo": "XGBClassifier",         "auc_cv": 0.856, "std_auc": 0.004, "max_auc": 0.862, "min_auc": 0.851},
    {"modelo": "RandomForestClassifier","auc_cv": 0.840, "std_auc": 0.004, "max_auc": 0.847, "min_auc": 0.836},
    {"modelo": "LogisticRegression",    "auc_cv": 0.825, "std_auc": 0.005, "max_auc": 0.834, "min_auc": 0.820},
    {"modelo": "DecisionTreeClassifier","auc_cv": 0.614, "std_auc": 0.005, "max_auc": 0.623, "min_auc": 0.607},
]  # fuente: notebooks/03_training_model.ipynb, salida de initial_models()

BEST_MODEL = {"nombre": "CatBoost", "auc_cv": 0.864}  # confirmado por el usuario como el .pkl servido en backend

MONITORING_AUC_GINI = {
    "expected_global": {"auc": 0.87, "gini": 0.73},
    "actual_global": {"auc": 0.84, "gini": 0.69},
    "mensual": [
        # (periodo, auc, gini) — 12 meses, jul-2025 a jun-2026
        ("2025-07", 0.85, 0.70), ("2025-08", 0.85, 0.70), ("2025-09", 0.85, 0.69),
        ("2025-10", 0.84, 0.68), ("2025-11", 0.85, 0.69), ("2025-12", 0.84, 0.67),
        ("2026-01", 0.84, 0.67), ("2026-02", 0.85, 0.70), ("2026-03", 0.84, 0.68),
        ("2026-04", 0.83, 0.66), ("2026-05", 0.85, 0.70), ("2026-06", 0.85, 0.70),
    ],
}  # fuente: notebooks/05_monitoring.ipynb, tabla de AUC/Gini por periodo

TARGET_DRIFT = [
    # (periodo, bad_rate, pd_promedio)
    ("Baseline", 0.06684, 0.06664),
    ("2025-07", 0.11324, 0.06714), ("2025-08", 0.10600, 0.06842), ("2025-09", 0.11292, 0.06735),
    ("2025-10", 0.10858, 0.06470), ("2025-11", 0.10920, 0.06687), ("2025-12", 0.10875, 0.06593),
    ("2026-01", 0.11661, 0.06798), ("2026-02", 0.11186, 0.06716), ("2026-03", 0.11164, 0.06545),
    ("2026-04", 0.11046, 0.06630), ("2026-05", 0.11283, 0.06719), ("2026-06", 0.11025, 0.06735),
]  # fuente: notebooks/05_monitoring.ipynb, bad_rate vs pd por periodo

PSI_SNAPSHOT = [
    # feature, psi, interpretacion — snapshot del último periodo monitoreado (2026-06)
    {"feature": "RevolvingUtilizationOfUnsecuredLines", "psi": 0.0001, "interpretacion": "Sin drift"},
    {"feature": "age", "psi": 0.0001, "interpretacion": "Sin drift"},
    {"feature": "NumberOfTime30-59DaysPastDueNotWorse", "psi": 0.0000, "interpretacion": "Sin drift"},
    {"feature": "DebtRatio", "psi": 0.0001, "interpretacion": "Sin drift"},
    {"feature": "MonthlyIncome", "psi": 0.0004, "interpretacion": "Sin drift"},
    {"feature": "NumberOfOpenCreditLinesAndLoans", "psi": 0.0001, "interpretacion": "Sin drift"},
    {"feature": "NumberOfTimes90DaysLate", "psi": 0.0000, "interpretacion": "Sin drift"},
    {"feature": "NumberRealEstateLoansOrLines", "psi": 0.0001, "interpretacion": "Sin drift"},
    {"feature": "NumberOfTime60-89DaysPastDueNotWorse", "psi": 0.0000, "interpretacion": "Sin drift"},
    {"feature": "NumberOfDependents", "psi": 0.0001, "interpretacion": "Sin drift"},
]  # fuente: notebooks/05_monitoring.ipynb; ver Decisiones sobre cómo se consolidó este snapshot

# Placeholders explícitos: no existen como datos tabulares reutilizables en los notebooks hoy.
FEATURE_IMPORTANCE_TOP10 = None  # TBD — solo existe como shap.plots.bar() embebido en 04_model_evaluation.ipynb
SCORE_DISTRIBUTION = None  # TBD — solo existe como figura matplotlib embebida

DATASET_INFO = {
    "poblacion_train": 150000,
    "poblacion_val": 45000,
    "n_features": 10,
    "n_modelos_evaluados": 6,
    "target": "SeriousDlqin2yrs",
    "default_rate_train": 0.0668,
}  # fuente: data/raw/cs-training.csv (150000 filas) y split de 04_model_evaluation.ipynb
```

`frontend/src/config.py` — configuración de runtime:

```python
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8082")

RISK_BAND_COLORS = {
    "Bajo Riesgo": "#2ecc71",
    "Medio Riesgo": "#f1c40f",
    "Alto Riesgo": "#e67e22",
    "Muy Alto Riesgo": "#e74c3c",
}  # las 4 llaves deben coincidir exactamente con clasificar_cliente() en backend/src/api/routes/predict.py
```

El payload de predicción y su respuesta reutilizan tal cual `ClienteInput`/`PredictionOutput` de `backend/src/models/schemas.py` — no se redefinen en el frontend, solo se arma el `dict` con las mismas 10 llaves (incluyendo los dos alias con guion) antes de hacer el POST.

---

## Implementation plan

1. Crear `frontend/src/config.py` con `BACKEND_URL` (env var, default `http://localhost:8082`) y `RISK_BAND_COLORS`. Test manual: `python -c "from src.config import BACKEND_URL; print(BACKEND_URL)"`.
2. Crear `frontend/src/api_client.py` con `predict(payload: dict) -> dict` (POST a `{BACKEND_URL}/api/v1/predict`, propaga errores HTTP como excepción) y `check_health() -> bool` (GET `{BACKEND_URL}/health`, devuelve `False` si falla). Test manual: con el backend local corriendo en `:8082`, `python -c "from src.api_client import check_health; print(check_health())"` imprime `True`.
3. Crear `frontend/src/dashboard_data.py` con las constantes del [Data model](#data-model), incluyendo los dos placeholders `None`. Test manual: `python -c "from src.dashboard_data import MODEL_COMPARISON; print(len(MODEL_COMPARISON))"` imprime `6`.
4. Crear `frontend/src/app.py` con el skeleton: `st.set_page_config(layout="wide")`, sidebar estático (título, las 5 etapas marcadas "Completado", enlaces "Make Prediction"/"Documentación") y las secciones del layout vacías en orden. Test manual: `streamlit run frontend/src/app.py` levanta sin errores y muestra el sidebar.
5. Implementar la sección Overview (título, badge "Production", botón "Download Project PPT" deshabilitado, tarjetas de business goal/target/dataset/modelos evaluados/mejor modelo) con `DATASET_INFO` y `BEST_MODEL`. Test manual visual.
6. Implementar "Project Workflow – 5 Stages" con las 5 tarjetas (EDA, Feature Engineering, Model Training, Model Evaluation, Monitoring), todas en estado "Completado". Test manual visual.
7. Implementar "Model Performance Summary" (bar chart AUC y Gini derivado por modelo, desde `MODEL_COMPARISON`) y "AUC Over Time (OOT)" (line chart desde `MONITORING_AUC_GINI["mensual"]`) con Plotly. Test manual: los charts muestran 6 modelos y 12 meses respectivamente.
8. Implementar "Feature Importance Top 10" y "Score Distribution" como tarjetas placeholder ("Próximamente — pendiente de exportar datos reales del notebook") cuando la constante correspondiente es `None`. Test manual visual.
9. Implementar "Data Drift (PSI)" (tabla desde `PSI_SNAPSHOT`) y "Target Drift" (line chart bad_rate vs pd desde `TARGET_DRIFT`). Test manual visual.
10. Implementar el panel "Make Prediction": formulario con los 10 campos de `ClienteInput` (inputs numéricos con labels legibles), botón "Predict Probability" que arma el payload y llama a `api_client.predict(...)` con spinner, capturando errores de conexión/500 en un `st.error()` sin crashear la app. Test manual: con backend local corriendo, completar el form y obtener `pd_estimada`/`banda_riesgo` reales.
11. Implementar "Prediction Result" (probabilidad + banda coloreada según `RISK_BAND_COLORS`) y "Key Information" (Model Type, Target, Eval Metric, Best AUC, Default Rate, Población) con `DATASET_INFO`/`BEST_MODEL`. Test manual: flujo end-to-end formulario → resultado coloreado.
12. Escribir `frontend/Dockerfile` (base `python:3.11-slim`, copia `requirements.txt` y `src/`, `EXPOSE 8501`, `CMD streamlit run src/app.py --server.port=8501 --server.address=0.0.0.0`) y recortar `frontend/requirements.txt` a `streamlit`, `requests`, `pandas`, `plotly`. Test manual: `docker build -t give-me-credit-frontend .` seguido de `docker run -p 8501:8501 -e BACKEND_URL=http://<ip-vps>:8082 give-me-credit-frontend` sirve la app en `:8501`.

---

## Acceptance criteria

- [ ] `streamlit run frontend/src/app.py` arranca sin errores en consola.
- [ ] Las 5 tarjetas de "Project Workflow" muestran estado "Completado".
- [ ] El formulario de predicción tiene exactamente los 10 campos de `ClienteInput`, incluyendo `NumberOfTime30-59DaysPastDueNotWorse` y `NumberOfTime60-89DaysPastDueNotWorse` con guion.
- [ ] Con el backend corriendo local en `:8082`, enviar el formulario muestra `pd_estimada` y `banda_riesgo` reales devueltos por `/api/v1/predict`.
- [ ] Si el backend no responde (apagado o error 500), el frontend muestra un mensaje de error legible sin crashear la app.
- [ ] El color del resultado corresponde exactamente a la banda de riesgo devuelta, usando `RISK_BAND_COLORS`.
- [ ] "Model Performance Summary" muestra los 6 modelos de `MODEL_COMPARISON` y "AUC Over Time" muestra los 12 periodos de `MONITORING_AUC_GINI["mensual"]`.
- [ ] "Feature Importance Top 10" y "Score Distribution" muestran el placeholder "Próximamente" en vez de un gráfico con datos inventados.
- [ ] El botón "Download Project PPT" está visible pero deshabilitado.
- [ ] `docker build` del frontend termina sin error.
- [ ] `docker run -p 8501:8501 -e BACKEND_URL=...` sirve la app en el puerto 8501 accesible por HTTP.
- [ ] Con `BACKEND_URL` apuntando a la IP del VPS y el backend corriendo ahí en `:8082`, una predicción completa funciona de punta a punta contra el backend desplegado.

---

## Decisions

- **Sí:** Streamlit como framework — ya está escafoldado (`requirements.txt`, `Dockerfile` vacío) y no hay señal de querer cambiarlo.
- **Sí:** Dashboard completo con datos hardcodeados, no solo un MVP de predicción — decisión explícita del usuario para tener la pieza de portafolio terminada ya.
- **Sí:** `Feature Importance Top 10` y `Score Distribution` quedan como placeholder (`None`) — esos números solo existen como gráficos `matplotlib`/`shap` embebidos en `04_model_evaluation.ipynb`, no como tablas exportadas; inventarlos sería mentir en un portafolio.
- **Sí:** `PSI_SNAPSHOT` consolida en una sola tabla valores confirmados de dos extremos de la salida impresa (features de 2025-07 y de 2026-06), porque pandas trunca las filas intermedias de un DataFrame de 120 filas al imprimirlo. Todos los valores confirmados caen en el mismo rango (~0.0000–0.0004, "Sin drift"), así que no se inventa magnitud, solo se etiqueta como snapshot del "último periodo monitoreado" en vez de un corte exacto de una sola fecha.
- **Sí:** Gini de `MODEL_COMPARISON` se deriva con `Gini = 2*AUC - 1` porque la comparación de CV en `03_training_model.ipynb` solo registró AUC. La fórmula es la relación estándar y se validó contra los pares reales de monitoreo (0.87/0.73 y 0.84/0.69 encajan dentro del margen de redondeo).
- **Sí:** `BACKEND_URL` como variable de entorno inyectada en `docker run -e`, sin docker-compose ni red Docker compartida — decisión explícita del usuario (contenedores administrados independientemente).
- **Sí:** Despliegue HTTP plano por IP:puerto para este spec — decisión explícita del usuario; TLS/dominio quedan para un spec de infraestructura futuro.
- **Sí:** Una sola página Streamlit (`app.py`), sin `st.navigation`/carpeta `pages/` — el layout de referencia es una vista scrolleable, no páginas separadas; el sidebar es mayormente informativo salvo el formulario de predicción.
- **No:** Predicción batch — el backend no expone un endpoint batch y agregarlo no es parte de un spec de frontend.
- **No:** Sección de reportes PDF (EDA/Model/Monitoring Report) del pie de la imagen — no existen esos archivos; solo se conserva el botón superior "Download Project PPT" como placeholder deshabilitado.
- **No:** docker-compose — decisión explícita del usuario de administrar los contenedores por separado.

---

## Risks

| Riesgo | Mitigación |
| --- | --- |
| Las métricas hardcodeadas (AUC, PSI, drift) quedan congeladas y no reflejan un futuro reentrenamiento del modelo | Están documentadas en `dashboard_data.py` como snapshot fijo (agosto 2026, con la fuente de cada constante en comentario); actualizar el archivo a mano es responsabilidad de un futuro spec/tarea, no hay refresco automático aquí |
| El backend cambia de IP/puerto en el VPS o no está corriendo al desplegar el frontend | `BACKEND_URL` es una env var inyectada en `docker run`, nunca hardcodeada en la imagen; `api_client.check_health()` permite mostrar un aviso en vez de que el formulario falle silenciosamente |
| `CORS_ORIGIN=['*']` en el backend acepta cualquier origen | Configuración heredada del backend, fuera de alcance de este spec de frontend; se deja registrado como riesgo conocido |

---

## What is **not** in this spec

- Predicción batch (subir CSV) — requiere un endpoint nuevo en el backend.
- Reportes descargables reales (PPT/PDF) — el botón queda deshabilitado hasta que existan los archivos.
- Feature Importance Top 10 y Score Distribution con datos reales — quedan como placeholder hasta exportar esos números desde los notebooks.
- TLS, dominio o reverse proxy — despliegue HTTP plano por IP:puerto por ahora.
- docker-compose u orquestación conjunta con el backend.
- Multi-page navigation en Streamlit.

Cada uno de estos, si se necesita, va en su propio spec.
