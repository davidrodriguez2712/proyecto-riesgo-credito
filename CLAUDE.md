# CLAUDE.md

Este archivo da contexto a Claude Code (claude.ai/code) al trabajar en este repositorio.

## Qué es esto

Un proyecto generado a partir del sistema de templates de `handsbook-ds`, para el dataset de Kaggle "Give Me Some Credit" (clasificación binaria de riesgo crediticio: `SeriousDlqin2yrs`). El proyecto en sí tiene poco código propio — es un scaffold (`setup.py`, `README.md`, `.env`, `params.yaml` vacíos) más un set de notebooks que ejecutan un pipeline de credit-risk importando módulos compartidos y reutilizables desde otras partes del monorepo `handsbook-ds`.

No hay build, lint ni tests configurados en este proyecto (sin CI, sin pytest, sin linter). El trabajo aquí es notebook-first, con `backend/` ya funcional como capa de despliegue (FastAPI sirviendo predicciones) y `frontend/` (Streamlit) todavía sin empezar.

## Estructura del repo (relevante para este proyecto)

```
handsbook-ds/                          <- raíz del monorepo (3 niveles arriba de notebooks/)
├── CORE/metadata.py                   <- inventario_features() — helper compartido de auditoría de features
├── EDA/utils/                         <- classifications.py (clase EDAClasificacion) + missing.py/outliers.py (funciones sueltas, extraídas pero aún no usadas por la clase)
├── Feature_Engineering/utils/         <- transformers/ + selection/ (incl. feature_selector.py) + reports/ (etapa FE)
├── Training_Model/utils/              <- algorithm.py, optuna_tunning.py, metrics.py (KS/lift/deciles/gestión de portafolio), calibration.py (Platt scaling, Vasicek)
├── Model_Evaluation/economic_metrics.py <- tablas de deciles ponderadas por saldo + gestión de portafolio (ver nota de duplicación abajo)
├── Monitoring/utils/monitor.py         <- monitoreo de performance/PSI/IV/outliers/SHAP entre baseline y periodos actuales
└── 11_Project_Templates/
    ├── 1-clasificacion-banca-no-temporal/  <- proyecto hermano (mismo template)
    └── 2-give-me-some-credit/         <- ESTE proyecto
        ├── notebooks/01_eda.ipynb .. 05_monitoring.ipynb
        ├── data/{raw,external,interim,processed}
        ├── artifacts/{eda,feature_engineering,training_model,model_evaluation,monitoring}
        ├── backend/   <- FastAPI funcional (endpoint /api/v1/predict, Dockerfile OK, código vendorizado de CORE/Training_Model/Feature_Engineering)
        ├── frontend/  <- Streamlit (requirements.txt listo, Dockerfile vacío, sin empezar)
        └── params.yaml, setup.py, .env  <- vacíos
```

**Importante: este proyecto no tiene un paquete propio independiente.** Toda la lógica real (clase de EDA, transformers de WOE/binning/outliers, selección de features, tuning de hiperparámetros) vive en los paquetes de nivel superior `EDA/`, `Feature_Engineering/`, `Training_Model/` y `CORE/` en la raíz del monorepo, y se comparte entre todos los proyectos bajo `11_Project_Templates/`. Antes de agregar un nuevo transformer, selector o helper de modelos aquí, revisa si ya existe en alguno de esos paquetes compartidos — la intención del sistema de templates es reutilización, no duplicación por proyecto.

## Cómo los notebooks llegan al código compartido

Cada notebook resuelve la raíz del monorepo en tiempo de ejecución y la agrega a `sys.path` antes de importar:

```python
PARENT_DIRECTORY_1 = Path.cwd().parent.parent.parent
sys.path.append(f"{str(PARENT_DIRECTORY_1)}")

from EDA.utils.classifications import EDAClasificacion
from Feature_Engineering.utils.transformers.woe import WOEClassic, Logit_Smoothing_Rolling
from Feature_Engineering.utils.selection.correlation import correlation
from Training_Model.utils.algorithm import initial_models
from Training_Model.utils.optuna_tunning import OptunaTunning
```

Esta resolución asume que el **cwd del notebook es `notebooks/`** — `Path.cwd().parent.parent.parent` sube `notebooks/ -> 2-give-me-some-credit/ -> 11_Project_Templates/ -> handsbook-ds/`. Varios módulos compartidos (p. ej. `Feature_Engineering/utils/selection/feature_selector.py`, `Training_Model/utils/algorithm.py`) hacen internamente la misma subida de `Path.cwd().parent.parent.parent` para llegar a `CORE.metadata`, así que solo resuelven bien cuando el cwd de quien los llama también está tres niveles bajo la raíz. Tenlo en cuenta al correr código fuera de Jupyter (script suelto, `python -c`, etc.) — la suposición de cwd se rompe y los imports fallan.

## Etapas del pipeline (notebooks, en orden)

1. **`01_eda.ipynb`** — `EDA.utils.classifications.EDAClasificacion(data, target_name, tipo_problema)`. Una sola clase que cubre toda la etapa de EDA: overview, análisis de missings, detección de outliers (IQR/percentil), distribuciones numéricas/categóricas, análisis del target, information value, PSI (drift train vs test), y un método `run_all()` de conveniencia.
2. **`02_feature_engineering.ipynb`** — arma un `Pipeline`/`ColumnTransformer` de sklearn con `Feature_Engineering.utils`: encoding WOE (`woe.py`), binning (`binning.py`), manejo de outliers (`outliers.py`), y selección de features por correlación/VIF/IV/PSI/gini (`selection/`), terminando con `selection.feature_selector.FeatureSelector` (un `BaseEstimator`/`TransformerMixin` que subsetea a una lista fija de features). Guarda el pipeline de preprocesamiento entrenado en `artifacts/feature_engineering/preprocessing.pkl`.
3. **`03_training_model.ipynb`** — `Training_Model.utils.algorithm.initial_models(...)` hace baseline de varios algoritmos (LogisticRegression, DecisionTree, RandomForest, XGBoost, LightGBM, CatBoost), y luego `Training_Model.utils.optuna_tunning.OptunaTunning` hace búsqueda de hiperparámetros con Optuna por algoritmo. Produce `pipeline_htunning_catboost.pkl` / `pipeline_htunning_lgbm.pkl` (raíz del proyecto) y `artifacts/training_model/params_*.pkl`.
4. **`04_model_evaluation.ipynb`** — el notebook en sí sigue siendo casi un duplicado de los imports/setup de training, pero el paquete compartido `Model_Evaluation/economic_metrics.py` ya existe: tablas de deciles ponderadas por saldo (`tabla_deciles_completa_saldos`, `seleccion_deciles_agrupamiento`, `tanteo_deciles`) y simulación de gestión de portafolio/pricing (`gestion_portafolio`). **Nota:** este archivo es casi una copia literal del tramo final de `Training_Model/utils/metrics.py` (mismas funciones, mismo cuerpo) — antes de tocar cualquiera de las dos, revisa si conviene consolidarlas en una sola en vez de seguir manteniendo el duplicado.
5. **`05_monitoring.ipynb`** — el notebook sigue prácticamente vacío, pero `Monitoring/utils/monitor.py` ya está construido: compara un baseline ("expected") contra periodos actuales ("actual") en performance (AUC/Gini), missings, PSI, outliers IQR, IV, bad rate vs PD, curvas ROC/PR, y variación de contribución SHAP (`shap_variacion_global`, `shap_variacion_global_periodica`). `Monitoring/README.md` existe pero está vacío.

## Backend / Frontend (backend ya funcional, frontend sin empezar)

- **`backend/`**: app FastAPI real bajo `backend/src/` — `main.py` (registra routers), `api/routes/{health,predict}.py`, `services/model_services.py` (`ModelService` carga el `.pkl` con joblib y expone `predict`), `models/schemas.py` (Pydantic), `config/config.py` + `config/logger.yaml`, y el modelo servido en `backend/src/ml/artifacts/model.pkl`. El endpoint `POST /api/v1/predict` recibe un `ClienteInput`, calcula la PD y la clasifica en bandas de riesgo (Bajo/Medio/Alto/Muy Alto Riesgo) por thresholds fijos en `predict.py`.
  - **Arquitectura de dependencias distinta a la que sugiere la raíz del repo**: en vez de que el Dockerfile copie desde el monorepo en build time (`COPY ../../...`, inválido en un build context estándar), el proyecto ahora **vendoriza copias físicas** de `CORE/`, `Training_Model/` y partes de `Feature_Engineering/utils/` (`selection/`, `transformers/`, más algunos módulos nuevos como `domain.py`, `encoders.py`, `binary_classification.py` que no existen en el `Feature_Engineering/` raíz del monorepo) directamente dentro de `backend/`. El build context de Docker es `backend/` mismo. Esto significa que **estas copias vendorizadas se desincronizan silenciosamente** de los paquetes compartidos en la raíz si estos últimos cambian — no hay symlink ni submódulo, es copy-paste. Al modificar `Feature_Engineering`/`Training_Model`/`CORE` compartidos, recuerda propagar el cambio manualmente a `backend/` si el backend depende de esa lógica.
  - El `Dockerfile` ya no está roto: `CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8082"]` es correcto y las rutas `COPY` (`CORE`, `Training_Model`, subcarpetas de `Feature_Engineering`, `src`, `logs`, `.env`) resuelven bien porque apuntan a las copias vendorizadas dentro de `backend/`, no a `../../`.
- **`frontend/`**: Streamlit, mismo `requirements.txt` ampliado (agrega `requests`, `catboost`, `pydantic_settings`). El `Dockerfile` sigue vacío — no hay nada desplegable todavía en esta capa.

## Convenciones de trabajo

- Comentarios, docstrings y nombres de variables en los utils compartidos (`EDA`, `Feature_Engineering`, `Training_Model`) están en **español**. Respeta esa convención al editar esos archivos.
- Los transformers custom compatibles con sklearn (`WOEClassic`, `Binning`, `AutoOutlierHandler`, `FeatureSelector`, etc.) siguen el patrón estándar `BaseEstimator, TransformerMixin` con fit/transform — sigue el mismo patrón al agregar nuevos para que compongan dentro de un `ColumnTransformer`/`Pipeline`.
- `data/raw/` contiene los archivos originales de Kaggle (`cs-training.csv`, `cs-test.csv`, `sampleEntry.csv`, `Data Dictionary.xls`); trátalos como inputs de solo lectura. Los datos derivados van en `data/interim/` o `data/processed/`.
