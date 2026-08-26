# SPEC 05 — Presentación: Bloque Técnico con datos reales del proyecto

> **Estado:** Implementado
> **Depende de:** SPEC 03 (artefactos reales), SPEC 04 (correcciones de contenido)
> **Fecha:** 2026-08-26
> **Objetivo:** Reemplazar en `presentacion/Resumen_Presentacion.pptx` (slides 1 y 5-12, el "Bloque Técnico") todo placeholder, dato de ejemplo o gráfico genérico por los valores reales del proyecto (modelo, SHAP, calibración, monitoreo), completando además las dos slides que quedaron casi vacías.

---

## Por qué existe este spec

El usuario armó la presentación (20 slides) en dos bloques — "Bloque Técnico" (slides 3-12) y "Bloque Negocio" (slides 13-20) — usando un template con placeholders (`[Tu Nombre]`, `[ej. Regresión Logística sobre WOE / Gradient Boosting]`), gráficos nativos de PowerPoint con datos de ejemplo, y dejó comentarios puntuales pidiendo completar contenido (slide 6: "Por completar"; slide 9: "Falta agregar mas metricas como KS y Lift").

Al auditar cada slide del Bloque Técnico contra los datos reales ya vetados en `frontend/src/dashboard_data.py` (SPEC 02/03/04) y los artefactos/notebooks del proyecto, se encontraron:

- Placeholders literales sin resolver (nombre del candidato, algoritmo final, método de calibración).
- Gráficos nativos (6 en total) con series/valores de ejemplo que no corresponden a ninguna corrida real del pipeline.
- Dos slides casi vacías (6 y 8) que necesitan contenido nuevo, no solo corrección.
- Una slide (7) cuyo orden de features por importancia SHAP es incorrecto frente al ranking real (falta "atrasos 30-59 días", que es el driver real #2).
- Una slide (9) cuya tabla Train/Test/OOT no tiene respaldo real — el proyecto solo generó AUC por cross-validation (media/mín/máx), no un split train/test/OOT único.
- Una slide (12) cuyo dato de PSI (0.06) y desviación de PD (+0.4 p.p.) no coinciden con la realidad: el PSI real es casi cero (sin drift de features), pero la tasa de mora observada (~11.1%) supera consistentemente a la PD promedio predicha (~6.7%) en los 12 periodos monitoreados — una brecha real de ~4.4 p.p. que el template no reflejaba y que cambia la conclusión de la slide.

Este spec cubre solo el Bloque Técnico (slides 1, 5-12); el Bloque Negocio (13-20) tiene sus propios huecos de datos (p. ej. no existe una comparación real "política actual vs. propuesta" ni una tabla de escenarios de cutoff) y se resuelve en un spec separado.

---

## Scope

**In:**

- Slide 1: reemplazar `Candidato: [Tu Nombre]` por `Candidato: David Rodriguez`.
- Slide 5 (Metodología y pipeline): paso "03 Feature Eng." — quitar la mención a "WOE-IV" (el pipeline real usa Log-Odds Rolling Smoothing, no WOE — mismo error ya corregido en el frontend por SPEC 04); paso "05 Modelado" — reemplazar el placeholder `[ej. Regresión Logística sobre WOE / Gradient Boosting]` por el texto real: *"CatBoost, seleccionado por desempeño e interpretabilidad frente a 6 algoritmos comparados."*
- Slide 6 ("Elección del Modelo", hoy solo dice "Por completar"): agregar un chart de barras nuevo con los 6 modelos de `MODEL_COMPARISON` (AUC CV) y un bloque de texto con `MODEL_SELECTION_NOTE` (por qué CatBoost y no LGBM pese a tener AUC ligeramente menor).
- Slide 7 (SHAP): corregir `chart1.xml` a los 6 features reales de mayor `|SHAP|` medio (orden y valores de `FEATURE_IMPORTANCE_TOP10`, top 6); corregir el bullet "Los atrasos recientes (60-89 y 90+ días) son el segundo driver más fuerte" — el driver real #2 es "atrasos de 30-59 días", no el grupo 60-89/90+.
- Slide 8 ("Simulación para diferentes tipos de clientes", hoy casi vacía): agregar 3 tarjetas con clientes reales del set de validación (uno por banda Bajo/Medio/Alto Riesgo), cada una con PD real, banda real, y sus top drivers SHAP reales — datos ya calculados en este spec (ver [Data model](#data-model)).
- Slide 9 (Modelo y métricas de desempeño): rediseñar la tabla (hoy Train/Test/OOT × AUC-ROC/KS/Gini) a **CV Mean/Min/Max** × AUC-ROC/Gini (derivado) para CatBoost; agregar una segunda tabla pequeña con `DECILE_KS_LIFT` (banda × bad rate/lift/KS) — resuelve el comentario "Falta agregar mas metricas como KS y Lift" con datos reales por banda en vez de un dato inventado por split. Corregir `chart2.xml` (ROC) con la curva real reproducida en este spec (12 puntos, AUC 0.8667).
- Slide 10 (Calibración): corregir `chart3.xml` con los 10 bins reales de `CALIBRATION_CURVE` (mean_predicted vs. fraction_positives, en %); reemplazar el placeholder `[ej. Platt scaling / regresión isotónica]` por "Platt scaling" (método real, confirmado en `Training_Model/utils/calibration.py`).
- Slide 11 (Estabilidad Gini mensual): corregir `chart4.xml` — categorías pasan de "Ene..Dic" genéricos a los 12 periodos reales (`2025-07` .. `2026-06`) con los valores reales de `MONITORING_AUC_GINI["mensual"]`.
- Slide 12 (Backtesting): reemplazar por completo el enfoque de `chart5.xml` (barras estáticas por 3 bandas) por una vista de tendencia mensual (Baseline + 12 meses reales) comparando bad rate observado vs. PD promedio predicha (`TARGET_DRIFT`), evidenciando la brecha real de ~4.4 p.p.; actualizar el bloque "Indicadores de estabilidad": PSI del score → rango real por variable (`PSI_SNAPSHOT`, ~0.0000-0.0004, "Sin drift"); "Desviación PD media" → +4.4 p.p. real (bad rate observado vs. PD promedio predicha); "Conclusión" → reescribir como hallazgo de drift de calibración/target (no de features): sin drift de covariables, ranking (Gini) estable, pero PD promedio predicha desalineada con la tasa de mora observada — recomienda recalibración.

**Out of scope (para futuros specs):**

- Slides 13-20 (Bloque Negocio): bandas de riesgo por score, impacto económico (ROA), simulación de escenarios de cutoff, recomendaciones, conclusiones y anexos — va en un spec separado, porque requiere decisiones propias sobre datos que hoy no existen en el proyecto (p. ej. no hay una comparación real "política actual vs. modelo propuesto" ni una tabla de escenarios de cutoff con datos reales).
- Slides 2, 3, 4: ya son correctas frente a los datos reales (agenda, divisor de sección, y ficha de datos — 150,000 registros / 10 variables / ~6.7% default / split 70-30 — todos verificados contra `DATASET_INFO`), no requieren cambios.
- Reentrenar o re-tunear el modelo, o generar nuevos artefactos en `artifacts/` — este spec solo lee datos ya existentes (`dashboard_data.py`, artefactos, el modelo ya entrenado `artifacts/training_model/model_catboost_extra.pkl`) y reproduce, sin volver a ajustar hiperparámetros, la curva ROC real y los 3 clientes ejemplo de la slide 8.
- Cambiar el diseño visual/tema/paleta de colores de la plantilla — solo se tocan textos, valores de charts y (en slides 6 y 8) shapes nuevos que reutilizan el estilo visual ya presente en slides análogas (p. ej. tarjetas de banda como en la slide 14, numeración como en la slide 5).
- Slide 20 (Backup/Anexos): menciona "Definiciones completas de WOE / IV por variable" como tema de anexo — es coherente dejarlo (WOE fue explorado y descartado en favor de Log-Odds Rolling Smoothing, "por qué no WOE" es justamente material de backup), no se modifica en este spec.

---

## Data model

Este spec no introduce estructuras de datos nuevas en el código del proyecto. Reutiliza y, en dos casos, reproduce datos reales:

**Reutilizados tal cual desde `frontend/src/dashboard_data.py`:**

```python
MODEL_COMPARISON        # 6 modelos × auc_cv/std_auc/max_auc/min_auc → slide 6 (chart nuevo)
MODEL_SELECTION_NOTE     # texto de justificación → slide 6
FEATURE_IMPORTANCE_TOP10  # top 6 usado → slide 7 (chart1.xml)
CALIBRATION_CURVE        # 10 bins → slide 10 (chart3.xml)
MONITORING_AUC_GINI["mensual"]  # 12 periodos reales → slide 11 (chart4.xml)
TARGET_DRIFT              # Baseline + 12 periodos, bad_rate vs pd_promedio → slide 12 (chart5.xml, rediseñado)
PSI_SNAPSHOT               # PSI por variable, snapshot 2026-06 → slide 12 (texto)
DECILE_KS_LIFT              # 4 bandas × bad_rate_pct/lift/ks_pct → slide 9 (tabla nueva)
```

**Reproducidos en este spec (no existían como artefacto guardado):**

Curva ROC real (slide 9, `chart2.xml`) — reproducida cargando el modelo ya entrenado y guardado (`artifacts/training_model/model_catboost_extra.pkl`) sobre el mismo split determinístico que usa `04_model_evaluation.ipynb` (`train_test_split(..., random_state=42, test_size=0.3, stratify=TARGET)`), sin reentrenar nada:

```python
# AUC real: 0.8667 (single split; distinto del auc_cv=0.864 de MODEL_COMPARISON, que es la media de 5-fold CV)
ROC_CURVE_REAL = [
    (0.0, 0.0), (0.0077, 0.1759), (0.0186, 0.2985), (0.0333, 0.4112),
    (0.0528, 0.5013), (0.0764, 0.5868), (0.113, 0.6619), (0.1653, 0.735),
    (0.2353, 0.8075), (0.3439, 0.8773), (0.538, 0.9471), (1.0, 1.0),
]  # (fpr, tpr), 12 puntos representativos de los 4592 puntos reales de roc_curve()
```

Tres clientes reales de ejemplo (slide 8) — filas reales del set de validación (mismo split de arriba), elegidas por cercanía a un PD objetivo dentro de cada banda; explicación SHAP calculada con `shap.TreeExplainer` sobre el mismo modelo:

```python
CLIENTES_EJEMPLO = [
    {
        "banda": "Bajo Riesgo", "pd": 0.0060,
        "top_drivers": [
            ("Utilización línea de crédito", -0.60, "0.0"),
            ("Edad", -0.45, "77"),
            ("Ratio deuda/ingreso", -0.24, "0.0"),
        ],
    },
    {
        "banda": "Medio Riesgo", "pd": 0.0200,
        "top_drivers": [
            ("N° atrasos 30-59 días", -0.18, "0"),
            ("Ingreso mensual", +0.11, "S/5,000"),
            ("N° líneas de crédito abiertas", -0.11, "7"),
        ],
    },
    {
        "banda": "Alto Riesgo", "pd": 0.0800,
        "top_drivers": [
            ("Utilización línea de crédito", +0.97, "0.74"),
            ("Ratio deuda/ingreso", +0.20, "0.58"),
            ("N° líneas de crédito abiertas", +0.14, "13"),
        ],
    },
]  # PD y contribuciones SHAP (espacio margin/log-odds) reales, sobre X_val real
```

Tabla nueva de la slide 9 (CV Mean/Min/Max, derivada de `MODEL_COMPARISON` filtrado a CatBoost):

```python
CV_METRICS_CATBOOST = {
    "auc":  {"mean": 0.864, "min": 0.858, "max": 0.869},
    "gini": {"mean": 0.728, "min": 0.716, "max": 0.738},  # derivado: 2*auc - 1
}
```

---

## Implementation plan

1. Extraer `presentacion/Resumen_Presentacion.pptx` (es un .zip) a un directorio de trabajo temporal; confirmar que reempaquetar sin cambios produce un .pptx idéntico y abrible (valida el mecanismo de ida y vuelta antes de tocar contenido). Test: abrir el .pptx reempaquetado en Keynote/PowerPoint sin errores.
2. Slide 1 (`slide1.xml`): reemplazar el texto `[Tu Nombre]` por `David Rodriguez`. Test manual: la slide 1 muestra "Candidato: David Rodriguez".
3. Slide 5 (`slide5.xml`): corregir el bullet de "03 Feature Eng." (quitar "WOE-IV") y el bullet de "05 Modelado" (texto real de CatBoost). Test manual visual.
4. Slide 6 (`slide6.xml` + nuevo `chart7.xml`/rels/embedding): quitar el texto "Por completar"; agregar un chart de barras con `MODEL_COMPARISON` (6 modelos, AUC CV) y un textbox con `MODEL_SELECTION_NOTE`, reutilizando el estilo visual de los charts existentes. Test manual visual: la slide muestra 6 barras con CatBoost y LGBM como las dos más altas.
5. Slide 7 (`chart1.xml` + `slide7.xml`): actualizar categorías/valores del chart a los 6 features reales de `FEATURE_IMPORTANCE_TOP10` en el orden correcto; corregir el bullet sobre el driver #2. Test manual: el orden de barras coincide con `FEATURE_IMPORTANCE_TOP10[:6]`.
6. Slide 8 (`slide8.xml`): agregar 3 tarjetas (Bajo/Medio/Alto Riesgo) con PD real y top 3 drivers SHAP reales de `CLIENTES_EJEMPLO`, reutilizando el estilo de tarjeta de la slide 14. Test manual visual.
7. Slide 9 (`slide9.xml` + `chart2.xml`): reemplazar la tabla 4×4 por la tabla CV Mean/Min/Max (`CV_METRICS_CATBOOST`) + tabla nueva de banda × bad rate/lift/KS (`DECILE_KS_LIFT`); corregir `chart2.xml` con los 12 puntos reales de `ROC_CURVE_REAL` y el label de AUC a 0.8667. Test manual: ambas tablas visibles, sin la fila "OOT" ni el placeholder anterior.
8. Slide 10 (`slide10.xml` + `chart3.xml`): corregir `chart3.xml` con los 10 bins de `CALIBRATION_CURVE` (en %); reemplazar el placeholder del método por "Platt scaling". Test manual visual.
9. Slide 11 (`chart4.xml`): reemplazar categorías "Ene..Dic" por los 12 periodos reales (`2025-07`..`2026-06`) y los valores de Gini reales de `MONITORING_AUC_GINI["mensual"]`. Test manual visual.
10. Slide 12 (`slide12.xml` + `chart5.xml`): rediseñar `chart5.xml` a una serie temporal Baseline + 12 meses (bad rate observado vs. PD promedio predicha, de `TARGET_DRIFT`); reescribir el bloque de indicadores (PSI real por variable, desviación PD real +4.4 p.p., conclusión reescrita como hallazgo de drift de calibración). Test manual visual: el chart muestra 13 categorías (Baseline + 12 meses) y dos series con la brecha visible.
11. Reempaquetar el .pptx final y validar que abre sin errores y que las 12 slides tocadas (1, 5-12) reflejan los cambios. Checklist de [Acceptance criteria](#acceptance-criteria).

---

## Acceptance criteria

- [ ] Slide 1 muestra "Candidato: David Rodriguez" (sin corchetes).
- [ ] Slide 5 no menciona "WOE-IV" y el paso "05 Modelado" describe CatBoost con el texto real de selección.
- [ ] Slide 6 ya no dice "Por completar"; muestra un chart de 6 barras (AUC CV) donde CatBoost y LGBM son las dos más altas, y el texto de `MODEL_SELECTION_NOTE`.
- [ ] Slide 7: el chart de SHAP muestra 6 barras en el orden real de `FEATURE_IMPORTANCE_TOP10` (utilización de línea, 30-59 días, 90 días, 60-89 días, edad, ratio deuda/ingreso); el bullet sobre el driver #2 menciona "30-59 días", no "60-89 y 90+".
- [ ] Slide 8 muestra 3 tarjetas de cliente (Bajo/Medio/Alto Riesgo) con PD real y al menos 3 drivers SHAP reales cada una.
- [ ] Slide 9 muestra una tabla CV Mean/Min/Max (AUC-ROC y Gini) y una tabla separada de banda × bad rate/lift/KS con los 4 valores reales de `DECILE_KS_LIFT`; el chart ROC tiene 12 puntos reales con AUC 0.8667 (no 0.9/0.97/1.0 genéricos).
- [ ] Slide 10: el chart de calibración usa los 10 bins reales de `CALIBRATION_CURVE`; el método de calibración dice "Platt scaling" sin corchetes.
- [ ] Slide 11: las categorías del chart de Gini mensual son periodos reales (`2025-07`..`2026-06`), no "Ene".."Dic"; los 12 valores coinciden con `MONITORING_AUC_GINI["mensual"]`.
- [ ] Slide 12: el chart muestra 13 categorías (Baseline + 12 meses reales) con bad rate observado y PD promedio predicha; el texto de indicadores ya no dice "PSI del score: 0.06" ni "+0.4 p.p."; la conclusión menciona explícitamente la brecha de ~4.4 p.p. y recomienda recalibración.
- [ ] El archivo `presentacion/Resumen_Presentacion.pptx` abre sin errores de corrupción en PowerPoint/Keynote tras el reempaquetado.
- [ ] Ningún placeholder entre corchetes (`[...]`) queda visible en las slides 1, 5-12.

---

## Decisions

- **Sí:** dividir la presentación en dos specs (Técnico ahora, Negocio después) — decisión explícita del usuario; las slides 13-20 dependen de datos (comparación de política, escenarios de cutoff) que hoy no existen en el proyecto y requieren su propia ronda de clarificación.
- **Sí:** actualizar los 6 charts nativos editando su XML + Excel embebido en vez de reemplazarlos por imágenes PNG — decisión explícita del usuario; mantiene los charts editables en PowerPoint.
- **No, para el chart ROC específicamente:** no se usó la imagen `curva_roc_monitoreo.png` como excepción — se prefirió reproducir los puntos reales (el usuario eligió re-ejecutar el cálculo) para mantener el chart nativo consistente con el resto.
- **Sí:** para el chart ROC, se recalculó cargando el modelo ya entrenado (`model_catboost_extra.pkl`) sobre el split determinístico existente, sin reentrenar — evita el costo de volver a correr Optuna (50 trials × 2 algoritmos) solo para obtener una curva.
- **Sí:** la tabla de la slide 9 cambia de Train/Test/OOT a CV Mean/Min/Max — el proyecto real no generó un split train/test/OOT único con estas 3 métricas; sí generó AUC por 5-fold CV. Evita inventar números de "test"/"OOT" que no existen.
- **Sí:** el KS/Lift pedido en el comentario del usuario se resuelve con la tabla real por banda (`DECILE_KS_LIFT`), no con un KS agregado por split (que tampoco existe como dato real).
- **Sí:** slide 8 usa 3 clientes reales tomados del set de validación (elegidos por cercanía a un PD objetivo dentro de cada banda), no clientes sintéticos inventados — decisión explícita del usuario, más honesto para un portafolio.
- **Sí:** slide 12 reporta la brecha real de ~4.4 p.p. entre bad rate observado y PD promedio predicha, reescribiendo la conclusión de "sin degradación" a "drift de calibración, sin drift de features" — decisión explícita del usuario tras planteársela; es un hallazgo real que cambiaría la conclusión si se ocultara.
- **No:** no se toca la sección "WOE / IV por variable" de la slide 20 (Backup) — queda fuera de este spec (slides 13-20), y de todos modos es coherente como material de respaldo sobre por qué se descartó WOE.

---

## Risks

| Riesgo | Mitigación |
| --- | --- |
| Editar `chart.xml` a mano (sin PowerPoint) puede desincronizar el chart con su Excel embebido (`ppt/embeddings/*.xlsx`), causando que PowerPoint marque el archivo como corrupto al abrir | Editar ambos (XML del chart y el `.xlsx` embebido) en el mismo paso, y validar reabriendo el .pptx reempaquetado antes de dar cada slide por terminada (paso 1 y 11 del plan) |
| `replace_data()` de python-pptx (si se usa) puede resetear formato custom de un chart (colores, forma de línea) | Preferir edición directa de XML cuando el chart ya tenga formato custom que se quiera preservar; usar python-pptx solo para charts nuevos (slide 6) donde no hay formato previo que perder |
| El AUC real reproducido (0.8667, single split) difiere ligeramente del `auc_cv` de `MODEL_COMPARISON` (0.864, media de 5-fold CV) | Ambos son reales y coexisten en distintas slides (6 usa CV, 9 usa el split real); se documenta la diferencia en este spec para que no se lea como inconsistencia al implementar |
| El hallazgo de la brecha de 4.4 p.p. en la slide 12 puede generar preguntas del panel sobre por qué el modelo no se recalibró antes del despliegue | Fuera del alcance de este spec — es contenido honesto de la presentación, no un bug del proyecto; se puede abordar como pregunta de seguimiento en la sesión real |

---

## What is **not** in this spec

- Slides 13-20 (Bloque Negocio): bandas por score, impacto económico, escenarios de cutoff, recomendaciones, conclusiones, backup.
- Reentrenamiento o re-tuning del modelo.
- Cambios de diseño visual/tema de la plantilla.
- Nuevos artefactos guardados en `artifacts/` (los datos reproducidos en este spec — curva ROC, clientes ejemplo — se calculan para poblar la presentación, no se persisten como archivo nuevo del pipeline).

Cada uno de estos, si se necesita, va en su propio spec.
