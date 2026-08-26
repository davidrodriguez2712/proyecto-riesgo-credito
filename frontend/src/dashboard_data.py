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
