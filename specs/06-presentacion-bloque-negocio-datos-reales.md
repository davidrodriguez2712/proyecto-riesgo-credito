# SPEC 06 — Presentación: Bloque de Negocio con datos reales del proyecto

> **Estado:** Aprobado
> **Depende de:** SPEC 05 (Bloque Técnico con datos reales)
> **Fecha:** 2026-08-26
> **Objetivo:** Reemplazar en `presentacion/Resumen_Presentacion.pptx` (slides 14-19, el "Bloque Negocio") las bandas por score y la comparación "política actual vs. propuesta" — ninguna de las dos respaldada por datos reales del proyecto — por las 4 bandas de riesgo y la economía de cartera realmente calculadas en `04_model_evaluation.ipynb` (`PORTFOLIO_MANAGEMENT`).

---

## Por qué existe este spec

SPEC 05 cubrió el Bloque Técnico (slides 1, 5-12). Al auditar el Bloque Negocio (slides 13-20) contra los mismos datos reales ya vetados en `frontend/src/dashboard_data.py`, aparecieron dos problemas de fondo, no solo placeholders sueltos:

- **Slide 14** define 3 bandas de riesgo por **score** (`≥700`, `620-699`, `<620`) con rangos de PD inventados (`<2%`, `2-8%`, `>8%`). El sistema real (`backend/src/api/routes/predict.py::clasificar_cliente`) usa **4 bandas por PD**: Bajo (≤1.21%), Medio (≤3.1%), Alto (≤16.7%), Muy Alto (>16.7%). No hay ningún score de corte en el sistema desplegado — todo el pricing y las decisiones se basan en PD.
- **Slides 16, 17 y 19** construyen toda su narrativa alrededor de una comparación "política actual (ROA 1.85%) vs. modelo propuesto (ROA 2.20%)" y un "cutoff recomendado: 635" — ninguno de los dos existe como cálculo real en el proyecto. Lo que sí existe es `PORTFOLIO_MANAGEMENT`: la economía real de las 4 bandas (saldo, participación, tasa activa, ROA, utilidad neta), generada por `gestion_portafolio()` en `04_model_evaluation.ipynb` y ya usada para validar los thresholds del backend.

De `PORTFOLIO_MANAGEMENT` se deriva un ROA de cartera ponderado real: `(13.3+19.3+32.5-2.8)M / (282.6+261.3+251.3+73.0)M = 62.3M / 868.2M = 7.18%`, y una participación real de cartera rentable: `100% - 8.4% (Muy Alto Riesgo) = 91.6%`. Estos dos números, ambos reales, reemplazan la comparación inventada y cuentan una historia más defendible: la segmentación por riesgo aísla exactamente el 8.4% de la cartera que pierde dinero (Muy Alto Riesgo, ROA -3.9%), sin necesitar un baseline "antes del modelo" que nunca se calculó.

---

## Scope

**In:**

- Slide 14 ("De score a decisión: bandas y cutoffs"): rediseñar de 3 tarjetas por score a **4 tarjetas por PD real**, mismo estilo visual (círculo de color + banda + rango + acción), reposicionadas para 4 columnas:
  - Bajo Riesgo (verde `2E8B57`): PD ≤ 1.21% → "Aprobación automática"
  - Medio Riesgo (dorado `C9A227`): PD ≤ 3.1% → "Revisión / condiciones ajustadas"
  - Alto Riesgo (naranja `D97C3D`, color nuevo): PD ≤ 16.7% → "Garantías adicionales o repricing (aún rentable: ROA real 12.9%)"
  - Muy Alto Riesgo (rojo `B84C4C`): PD > 16.7% → "Rechazo (único segmento no rentable: ROA real -3.9%)"
  - Texto inferior de la slide ("El cutoff óptimo se define junto con negocio...") se reescribe para reflejar que son 4 bandas fijas, no un cutoff continuo.
- Slide 15 ("Variables clave, en lenguaje de negocio"): reordenar el bullet 3 ("Carga de deuda vs. ingreso") y el bullet 4 ("Edad del cliente") — el orden real de `FEATURE_IMPORTANCE_TOP10` es Edad (0.0079) antes que Ratio deuda/ingreso (0.0063); hoy están al revés.
- Slide 16 ("Impacto económico del modelo"): reemplazar los 3 KPIs grandes y el chart:
  - KPI 1: **"7.18%"** — "ROA de cartera (ponderado, real)"
  - KPI 2: **"91.6%"** — "de la cartera en bandas rentables (Bajo + Medio + Alto)"
  - KPI 3: **"-3.9%"** — "ROA de Muy Alto Riesgo — único segmento no rentable"
  - Chart (`chart6.xml`): de "Política actual vs. Modelo propuesto" (2 barras inventadas) a un chart de 4 barras — ROA real por banda (4.7% / 7.4% / 12.9% / -3.9%), coloreadas con los mismos 4 colores de la slide 14.
  - Texto "Metodología del cálculo" se ajusta: ya no menciona "cartera simulada bajo el nuevo cutoff", sino "cartera real segmentada en las 4 bandas de riesgo del modelo (`gestion_portafolio()`, `04_model_evaluation.ipynb`)".
- Slide 17 ("Simulación de escenarios de cutoff" → renombrada "Economía de cartera por banda de riesgo"): reemplazar la tabla 4×5 de escenarios inventados por una tabla real de 4 filas × 5 columnas: Banda | Participación % | Tasa activa % | ROA % | Utilidad neta — datos de `PORTFOLIO_MANAGEMENT`. El bloque "★ Recomendación" se reescribe: ya no menciona "cutoff 635", sino que el foco de gestión debe estar en Muy Alto Riesgo (8.4% de cartera, ROA -3.9%) como candidata a rechazo o repricing, mientras las otras 3 bandas ya son rentables.
- Slide 18 ("Recomendaciones e implementación"): el ítem 1 ("Cutoff operativo") se reescribe como "Política de 4 bandas" — adoptar las 4 bandas de riesgo ya calibradas en producción, con foco de revisión a 90 días en el tratamiento de Muy Alto Riesgo. Los ítems 2, 3 y 4 (Monitoreo continuo, Gobernanza del modelo, Plan de reentrenamiento) no mencionan cutoffs por score y quedan sin cambios.
- Slide 19 ("Conclusiones"): el bullet "RESULTADO DE NEGOCIO" se reescribe reemplazando "+0.35 p.p. / -18% frente a la política vigente" por los 3 KPIs reales de la slide 16 (ROA 7.18%, 91.6% de cartera rentable, Muy Alto Riesgo como único segmento negativo). El bullet "RESULTADO TÉCNICO" no cambia (AUC 0.84-0.86 y Gini sin degradación estructural siguen siendo correctos — SPEC 05 solo corrigió la desviación de PD promedio, no el ranking).

**Out of scope (para futuros specs):**

- Slide 13 (divisor de sección "Bloque de Negocio") y Slide 20 (Backup/Anexos) — ya son correctas o quedan fuera de alcance (WOE como tema de anexo es coherente, ver SPEC 05).
- Construir un baseline "sin modelo" (aprobar al 100% de solicitantes a la tasa promedio de default) para simular una comparación antes/después — decisión explícita del usuario: requeriría supuestos de LGD/EAD no confirmados en el código, y el número resultante sería una estimación nueva, no un cálculo ya validado en los notebooks.
- Cualquier cambio a los thresholds reales de `clasificar_cliente()` en el backend — este spec solo refleja esos thresholds en la presentación, no los modifica.
- Cambios al Bloque Técnico (slides 1-12) — ya resuelto en SPEC 05.
- Cambiar el diseño visual/tema/paleta base de la plantilla — solo se ajustan textos, valores de charts/tablas y el layout de las tarjetas de la slide 14 (de 3 a 4 columnas), reutilizando el estilo visual existente.

---

## Data model

Este spec no introduce estructuras de datos nuevas en el código del proyecto. Reutiliza `PORTFOLIO_MANAGEMENT` de `frontend/src/dashboard_data.py` (ya real, ya vetado por SPEC 03) y deriva dos agregados nuevos únicamente para la presentación:

```python
# Reutilizado tal cual desde dashboard_data.py — fuente: gestion_portafolio(), 04_model_evaluation.ipynb
PORTFOLIO_MANAGEMENT = [
    {"segmento": "Bajo Riesgo",     "participacion_pct": 32.6, "tasa_activa_pct": 14.0, "utilidad_neta": "S/13.3M", "roa_pct": 4.7},
    {"segmento": "Medio Riesgo",    "participacion_pct": 30.1, "tasa_activa_pct": 18.0, "utilidad_neta": "S/19.3M", "roa_pct": 7.4},
    {"segmento": "Alto Riesgo",     "participacion_pct": 28.9, "tasa_activa_pct": 28.0, "utilidad_neta": "S/32.5M", "roa_pct": 12.9},
    {"segmento": "Muy Alto Riesgo", "participacion_pct": 8.4,  "tasa_activa_pct": 35.0, "utilidad_neta": "S/-2.8M", "roa_pct": -3.9},
]

# Derivados en este spec, solo para los KPIs de las slides 16/19 (no se persisten como artefacto nuevo)
ROA_CARTERA_PONDERADO = (13.3 + 19.3 + 32.5 - 2.8) / (282.6 + 261.3 + 251.3 + 73.0)  # = 0.0718 -> "7.18%"
PARTICIPACION_RENTABLE = 32.6 + 30.1 + 28.9  # = 91.6 -> "91.6%"

# Umbrales reales de banda — fuente: backend/src/api/routes/predict.py::clasificar_cliente
BANDAS_PD = [
    {"banda": "Bajo Riesgo",     "pd_max": 0.0121, "color": "2E8B57", "accion": "Aprobación automática"},
    {"banda": "Medio Riesgo",    "pd_max": 0.031,  "color": "C9A227", "accion": "Revisión / condiciones ajustadas"},
    {"banda": "Alto Riesgo",     "pd_max": 0.167,  "color": "D97C3D", "accion": "Garantías adicionales o repricing"},
    {"banda": "Muy Alto Riesgo", "pd_max": None,   "color": "B84C4C", "accion": "Rechazo"},
]
```

---

## Implementation plan

1. Extraer `presentacion/Resumen_Presentacion.pptx` a un directorio de trabajo (reutilizando el mecanismo de extraer/editar/reempaquetar ya validado en SPEC 05); reempaquetar sin cambios y confirmar que abre bien antes de tocar contenido.
2. Slide 14 (`slide14.xml`): reposicionar/redimensionar las tarjetas de 3 a 4 columnas (mismo ancho de slide, columnas más angostas); editar textos y colores según `BANDAS_PD`; reescribir el texto inferior sobre el cutoff. Test manual visual: 4 tarjetas visibles con los rangos de PD reales.
3. Slide 15 (`slide15.xml`): intercambiar el contenido de los bullets 3 y 4 (Edad antes que Ratio deuda/ingreso). Test manual: el bullet 3 dice "Edad del cliente" y el bullet 4 "Carga de deuda vs. ingreso".
4. Slide 16 (`slide16.xml` + `chart6.xml`): reemplazar los 3 KPIs grandes por los valores derivados (`ROA_CARTERA_PONDERADO`, `PARTICIPACION_RENTABLE`, ROA de Muy Alto Riesgo); reconstruir `chart6.xml` como un chart de 4 barras (ROA real por banda, coloreadas); ajustar el texto de metodología. Test manual: los 3 KPIs y las 4 barras muestran los valores reales.
5. Slide 17 (`slide17.xml`): renombrar el título; reemplazar la tabla 4×5 de escenarios por la tabla real de `PORTFOLIO_MANAGEMENT` (Banda, Participación %, Tasa activa %, ROA %, Utilidad neta); reescribir el bloque de recomendación. Test manual: la tabla muestra los 4 valores reales de ROA/utilidad.
6. Slide 18 (`slide18.xml`): reescribir el ítem 1 ("Cutoff operativo" → "Política de 4 bandas"). Test manual visual.
7. Slide 19 (`slide19.xml`): reescribir el bullet "RESULTADO DE NEGOCIO" con los 3 KPIs reales. Test manual: ya no aparece "+0.35 p.p." ni "-18%" ni "score 635" en ninguna slide del deck.
8. Reempaquetar el .pptx final; validar con el mismo checklist automatizado de SPEC 05 (python-pptx: valores de charts/tablas, ausencia de placeholders y de las cifras inventadas, zip íntegro) y diff contra la versión post-SPEC-05 para confirmar que solo cambiaron las slides 14-19. Checklist de [Acceptance criteria](#acceptance-criteria).

---

## Acceptance criteria

- [ ] Slide 14 muestra 4 tarjetas (Bajo/Medio/Alto/Muy Alto Riesgo) con los rangos de PD reales (≤1.21% / ≤3.1% / ≤16.7% / >16.7%) y ya no menciona ningún score (`≥700`, `620`, etc.).
- [ ] Slide 15: el bullet 3 es "Edad del cliente" y el bullet 4 es "Carga de deuda vs. ingreso" (orden real por `|SHAP|`).
- [ ] Slide 16 muestra los 3 KPIs reales (7.18% / 91.6% / -3.9%) y el chart tiene 4 barras (una por banda) en vez de "Política actual vs. Modelo propuesto".
- [ ] Slide 17 se titula sin mencionar "cutoff" y su tabla tiene 4 filas con los valores reales de `PORTFOLIO_MANAGEMENT` (participación, tasa activa, ROA, utilidad neta).
- [ ] Slide 18: el ítem 1 no menciona "score 635" ni "cutoff operativo" con ese wording; describe la política de 4 bandas.
- [ ] Slide 19: el bullet de resultado de negocio no contiene "+0.35 p.p." ni "-18%"; contiene los 3 KPIs reales de la slide 16.
- [ ] Ningún texto de las slides 14-19 menciona "635", "1.85%", "2.20%", "+6%" (los números inventados originales).
- [ ] El archivo `presentacion/Resumen_Presentacion.pptx` abre sin errores de corrupción tras el reempaquetado.
- [ ] Diff contra la versión guardada al cierre de SPEC 05 muestra cambios únicamente en `slide14.xml`..`slide19.xml`, `chart6.xml`, su Excel embebido y `[Content_Types].xml` si aplica — ninguna otra slide se modifica.

---

## Decisions

- **Sí:** reemplazar las 3 bandas por score con las 4 bandas reales por PD del backend — decisión explícita del usuario; es lo único que realmente corre en producción.
- **Sí:** para el impacto económico, usar el ROA de cartera ponderado real (7.18%) y la participación de cartera rentable (91.6%) en vez de un baseline "política actual" — ambos derivables de `PORTFOLIO_MANAGEMENT` sin inventar ningún dato nuevo.
- **No:** no se construye un baseline "sin modelo" (aprobar al 100%) — requeriría supuestos de LGD/EAD no confirmados en el código; el usuario prefirió evitar introducir una estimación nueva no validada en los notebooks.
- **Sí:** Alto Riesgo cambia de color de rojo (en el sistema viejo de 3 bandas) a naranja (`D97C3D`, nuevo) — porque en los datos reales Alto Riesgo sigue siendo rentable (ROA 12.9%); el rojo se reserva para Muy Alto Riesgo, el único segmento con ROA negativo.
- **Sí:** la slide 17 se retitula de "Simulación de escenarios de cutoff" a algo sin la palabra "cutoff" — el sistema real no tiene un cutoff continuo simulable, tiene 4 bandas fijas; mantener la palabra "cutoff" en el título sería engañoso.
- **No:** no se elimina la slide 17 — se reutiliza para mostrar la tabla completa de economía por banda (complementa el chart resumen de la slide 16, mismo patrón que SPEC 05 usó en la slide 9: chart + tabla).

---

## Risks

| Riesgo | Mitigación |
| --- | --- |
| Achicar las tarjetas de la slide 14 de 3 a 4 columnas puede dejar los textos de "acción" (p. ej. "Garantías adicionales o repricing") apretados en un ancho menor | Usar textos más cortos que en el borrador de este spec si al revisar visualmente en PowerPoint se ven cortados; el ancho de columna se reduce de 3566160 a ~2602230 EMU, un 27% menos |
| Slide 19 depende de los KPIs definidos en la slide 16 — si se implementan en orden inverso, la slide 19 quedaría con placeholders sin resolver momentáneamente | El plan de implementación fija el orden (16 antes que 19); cada paso deja el sistema funcional, pero la slide 19 solo debe darse por completa después del paso 7 |

---

## What is **not** in this spec

- Slides 1-12 (Bloque Técnico) — SPEC 05.
- Slide 13 (divisor) y Slide 20 (Backup/Anexos).
- Baseline "sin modelo" con supuestos de LGD/EAD nuevos.
- Cambios a los thresholds reales de `clasificar_cliente()` en el backend.
- Cambios de diseño visual/tema de la plantilla más allá del layout de 4 columnas en la slide 14.

Cada uno de estos, si se necesita, va en su propio spec.
