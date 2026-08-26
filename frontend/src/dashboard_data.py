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
FEATURE_IMPORTANCE_TOP10 = [
    {"feature": "RevolvingUtilizationOfUnsecuredLines", "importance": 0.0278},
    {"feature": "NumberOfTime30-59DaysPastDueNotWorse", "importance": 0.0183},
    {"feature": "NumberOfTimes90DaysLate", "importance": 0.0178},
    {"feature": "NumberOfTime60-89DaysPastDueNotWorse", "importance": 0.0124},
    {"feature": "age", "importance": 0.0079},
    {"feature": "DebtRatio", "importance": 0.0063},
    {"feature": "NumberOfOpenCreditLinesAndLoans", "importance": 0.0056},
    {"feature": "MonthlyIncome", "importance": 0.0047},
    {"feature": "NumberRealEstateLoansOrLines", "importance": 0.0035},
    {"feature": "NumberOfDependents", "importance": 0.0012},
]  # fuente: notebooks/04_model_evaluation.ipynb, shap_values (mean |SHAP| por feature, top 10)

# Placeholder — no existe como dato tabular hoy. Fuente esperada: sklearn.calibration.calibration_curve()
# (o Training_Model/utils/calibration.py) sobre y_true/y_pred_proba del set de validación/OOT.
CALIBRATION_CURVE = [
    {"mean_predicted": 0.003778, "fraction_positives": 0.005937, "n_bin": 4500},
    {"mean_predicted": 0.005778, "fraction_positives": 0.008258, "n_bin": 4500},
    {"mean_predicted": 0.008000, "fraction_positives": 0.010737, "n_bin": 4500},
    {"mean_predicted": 0.014000, "fraction_positives": 0.013667, "n_bin": 4500},
    {"mean_predicted": 0.017333, "fraction_positives": 0.017812, "n_bin": 4500},
    {"mean_predicted": 0.026444, "fraction_positives": 0.025314, "n_bin": 4500},
    {"mean_predicted": 0.039111, "fraction_positives": 0.039612, "n_bin": 4500},
    {"mean_predicted": 0.065778, "fraction_positives": 0.064199, "n_bin": 4500},
    {"mean_predicted": 0.115333, "fraction_positives": 0.113148, "n_bin": 4500},
    {"mean_predicted": 0.372889, "fraction_positives": 0.364468, "n_bin": 4500},
]
# Formato esperado: [{"mean_predicted": 0.05, "fraction_positives": 0.04, "n_bin": 1500}, ...] por bin (p.ej. 10 bins)

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

DATASET_INFO = {
    "poblacion_train": 150000,
    "poblacion_val": 45000,
    "n_features": 10,
    "n_modelos_evaluados": 6,
    "target": "SeriousDlqin2yrs",
    "default_rate_train": 0.0668,
}  # fuente: data/raw/cs-training.csv (150000 filas) y split de 04_model_evaluation.ipynb

EDA_OVERVIEW = {
    "filas": 150000, "columnas": 11, "features_numericas": 11, "features_categoricas": 0,
    "missing_global": 33655, "features_con_missing": 2, "filas_duplicadas": 609,
    "features_constantes": 0, "features_casi_constantes": 1,
}  # fuente: artifacts/eda/tables/data_overview.csv

EDA_TARGET_SUMMARY = {
    "registros": 150000, "missing_target": 0, "positive_rate": 0.06684, "negative_rate": 0.93316,
    "imbalance_rate": "13.96:1", "baseline_accuracy": 0.9332, "nivel_desbalance": "Desbalanceado",
}  # fuente: artifacts/eda/tables/target_summary.csv

EDA_MISSING = [
    # feature, missing_pct — únicas dos features con nulos del dataset
    {"feature": "MonthlyIncome", "missing_pct": 19.82},
    {"feature": "NumberOfDependents", "missing_pct": 2.62},
]  # fuente: artifacts/eda/tables/feature_inventory.csv

EDA_INFORMATION_VALUE = [
    {"feature": "RevolvingUtilizationOfUnsecuredLines", "iv": 1.05955},
    {"feature": "age", "iv": 0.250022},
    {"feature": "MonthlyIncome", "iv": 0.076565},
    {"feature": "DebtRatio", "iv": 0.059485},
    {"feature": "NumberOfOpenCreditLinesAndLoans", "iv": 0.048021},
    {"feature": "NumberOfDependents", "iv": 0.024083},
    {"feature": "NumberRealEstateLoansOrLines", "iv": 0.01209},
    {"feature": "NumberOfTime30-59DaysPastDueNotWorse", "iv": 0.0},
    {"feature": "NumberOfTimes90DaysLate", "iv": 0.0},
    {"feature": "NumberOfTime60-89DaysPastDueNotWorse", "iv": 0.0},
]  # fuente: artifacts/eda/tables/information_value.csv

EDA_OUTLIERS_IQR = [
    {"feature": "DebtRatio", "pct_fuera_rango": 20.87},
    {"feature": "NumberOfDependents", "pct_fuera_rango": 8.89},
    {"feature": "MonthlyIncome", "pct_fuera_rango": 3.25},
    {"feature": "NumberOfOpenCreditLinesAndLoans", "pct_fuera_rango": 2.65},
    {"feature": "RevolvingUtilizationOfUnsecuredLines", "pct_fuera_rango": 0.51},
    {"feature": "age", "pct_fuera_rango": 0.03},
]  # fuente: artifacts/eda/tables/outliers_iqr.csv

EDA_PSI_TRAIN_TEST = [
    {"feature": "MonthlyIncome", "psi": 0.0004, "interpretacion": "Sin drift"},
    {"feature": "RevolvingUtilizationOfUnsecuredLines", "psi": 0.0001, "interpretacion": "Sin drift"},
    {"feature": "age", "psi": 0.0001, "interpretacion": "Sin drift"},
    {"feature": "DebtRatio", "psi": 0.0001, "interpretacion": "Sin drift"},
    {"feature": "NumberOfOpenCreditLinesAndLoans", "psi": 0.0001, "interpretacion": "Sin drift"},
    {"feature": "NumberRealEstateLoansOrLines", "psi": 0.0001, "interpretacion": "Sin drift"},
    {"feature": "NumberOfDependents", "psi": 0.0001, "interpretacion": "Sin drift"},
    {"feature": "NumberOfTime30-59DaysPastDueNotWorse", "psi": 0.0, "interpretacion": "Sin drift"},
    {"feature": "NumberOfTimes90DaysLate", "psi": 0.0, "interpretacion": "Sin drift"},
    {"feature": "NumberOfTime60-89DaysPastDueNotWorse", "psi": 0.0, "interpretacion": "Sin drift"},
]  # fuente: artifacts/eda/tables/psi.csv (PSI train vs test, distinto del PSI_SNAPSHOT de monitoreo)

EDA_FIGURES = {
    "analisis_target": "artifacts/eda/figures/analisis_target.png",
    "missing_graph": "artifacts/eda/figures/missing_graph.png",
    "distribucion_numericas": "artifacts/eda/figures/distribucion_numericas.png",
    "correlaciones": "artifacts/eda/figures/correlaciones.png",
}  # rutas relativas a la raíz del proyecto (2-give-me-some-credit/)
