# SPEC 07 — README.md del proyecto para GitHub

> **Estado:** Aprobado
> **Depende de:** Ninguno
> **Fecha:** 2026-08-26
> **Objetivo:** Escribir `README.md` (hoy vacío) con un resumen del proyecto de riesgo crediticio, mostrando al inicio un acceso a la presentación (`presentacion/Resumen_Presentacion.pptx`) y siguiendo una estructura estándar de README de portafolio.

---

## Por qué existe este spec

`README.md` está vacío desde que `setup.py` lo creó como placeholder (`Path('./README.md').touch()`). El repo ya tiene remote en GitHub (`github.com/davidrodriguez2712/proyecto-riesgo-credito`), pipeline de notebooks completo, backend FastAPI funcional, frontend Streamlit multipágina, y una presentación ejecutiva ya corregida con datos reales (SPEC 05/06). Falta el documento que amarra todo eso para quien entra al repo por primera vez.

---

## Scope

**In:**

- Reescribir `README.md` completo, en español, con esta estructura y orden de secciones:
  1. Título + badges de stack tecnológico (shields.io): Python, FastAPI, Streamlit, XGBoost, LightGBM, CatBoost, Docker, License.
  2. **Presentación**: badge/enlace de descarga directo a `presentacion/Resumen_Presentacion.pptx` (ruta relativa dentro del repo), con una línea de contexto ("Resumen ejecutivo del proyecto en formato PowerPoint").
  3. **Descripción del problema**: qué es "Give Me Some Credit" (clasificación binaria de riesgo crediticio, `SeriousDlqin2yrs`), qué resuelve el proyecto de punta a punta (EDA → Feature Engineering → Training → Evaluation → Monitoring → API → Dashboard).
  4. **Screenshot del dashboard**: imagen `design/pantalla_principal.png` embebida con ruta relativa.
  5. **Arquitectura**: diagrama textual o lista de las 5 etapas del pipeline de notebooks (`01_eda` .. `05_monitoring`) + capa de despliegue (`backend/` FastAPI, `frontend/` Streamlit), mencionando que backend y frontend consumen artefactos generados por los notebooks.
  6. **Estructura de carpetas**: árbol simplificado (no exhaustivo de `.venv`/`__pycache__`) con `notebooks/`, `data/`, `artifacts/`, `backend/`, `frontend/`, `presentacion/`, `design/`, `specs/`.
  7. **Instalación y uso rápido**: comandos mínimos para correr backend (`pip install -r backend/requirements.txt` + `uvicorn src.main:app --host 0.0.0.0 --port 8082`, ejecutado desde `backend/`) y frontend (`pip install -r frontend/requirements.txt` + `streamlit run src/app.py`, ejecutado desde `frontend/`). Sin instrucciones Docker.
  8. **Stack tecnológico**: lista corta de librerías/frameworks usados (derivada de `backend/requirements.txt` y `frontend/requirements.txt`: FastAPI, Streamlit, scikit-learn, XGBoost, LightGBM, CatBoost, Optuna, SHAP, Plotly, Docker).
  9. **Estado del proyecto**: nota breve de qué está completo (notebooks, backend) y qué está en progreso (`frontend/Dockerfile` vacío, `05_monitoring.ipynb` casi vacío aunque el módulo compartido `Monitoring/utils/monitor.py` ya existe).
  10. **Licencia**: sección con licencia MIT, enlazando al archivo `LICENSE`.
- Crear el archivo `LICENSE` en la raíz del proyecto con el texto estándar de la licencia MIT, a nombre de David Rodriguez, año 2026.
- Todos los enlaces e imágenes usan rutas relativas dentro del repo (no URLs absolutas a GitHub), para que funcionen tanto en local (preview de editor) como renderizados en GitHub.

**Out of scope (para futuros specs):**

- Convertir slides de la presentación a imágenes PNG para preview visual — se usa solo un badge/enlace de descarga (decisión explícita del usuario).
- Sección de autor/contacto (nombre, GitHub, LinkedIn) al final del README — decisión explícita del usuario de no incluirla.
- Mención formal/badge de la fuente del dataset de Kaggle como sección dedicada — el usuario solo pidió la sección de licencia, no una sección de atribución del dataset. El nombre del dataset puede aparecer de forma natural en la descripción del problema, pero no como sección o enlace formal.
- Traducción del README a inglés o versión bilingüe — el usuario confirmó español únicamente.
- README propios para `backend/` o `frontend/` (sub-READMEs) — no se pidieron, y hoy no existen.
- Documentar en el README los detalles de la duplicación `Model_Evaluation/economic_metrics.py` vs `Training_Model/utils/metrics.py`, o el vendoring de `backend/` — son notas de arquitectura interna (ya cubiertas en `CLAUDE.md`), no contenido para un README de portafolio.
- Badges dinámicos de CI/build (no hay CI configurado en este proyecto).

---

## Data model

Este spec no introduce estructuras de datos. Introduce dos archivos nuevos de documentación/legal:

- `README.md` (raíz del proyecto) — reescrito completo, contenido markdown estático.
- `LICENSE` (raíz del proyecto) — texto estándar MIT License, sin plantillas ni variables adicionales más allá de año y titular.

---

## Implementation plan

1. Crear `LICENSE` en la raíz con el texto estándar de MIT License (año 2026, titular "David Rodriguez"). Test manual: el archivo existe y el texto coincide con la plantilla oficial de MIT.
2. Escribir en `README.md` el bloque de título + badges (shields.io) + sección de Presentación con el badge/enlace a `presentacion/Resumen_Presentacion.pptx`. Test manual: los badges renderizan como imágenes markdown válidas y el enlace de descarga apunta a una ruta relativa existente.
3. Agregar la sección de Descripción del problema (Give Me Some Credit, riesgo crediticio, pipeline de punta a punta). Test manual: se lee de corrido, sin jerga sin explicar.
4. Insertar el screenshot `design/pantalla_principal.png` con ruta relativa correcta. Test manual: la imagen se previsualiza en un editor markdown local.
5. Escribir la sección de Arquitectura (5 etapas del pipeline + backend + frontend) y la de Estructura de carpetas (árbol simplificado). Test manual: los nombres de carpetas/archivos citados existen realmente en el repo (`notebooks/`, `backend/src/`, `frontend/src/`, etc.).
6. Escribir Instalación y uso rápido (comandos backend/frontend) y Stack tecnológico. Test manual: los comandos de instalación coinciden con los `requirements.txt` reales y los comandos de arranque (`uvicorn src.main:app --port 8082`, `streamlit run src/app.py`) coinciden con lo que hay en `backend/Dockerfile` y `frontend/src/app.py`.
7. Escribir Estado del proyecto y la sección de Licencia enlazando a `LICENSE`. Test manual: el enlace `[LICENSE](LICENSE)` resuelve al archivo creado en el paso 1.
8. Revisión final: leer el README completo de punta a punta, confirmar orden de secciones según el Scope, y verificar el checklist de [Acceptance criteria](#acceptance-criteria).

---

## Acceptance criteria

- [ ] `README.md` ya no está vacío y sigue el orden de secciones definido en el Scope (título/badges → presentación → descripción → screenshot → arquitectura → estructura de carpetas → instalación → stack → estado → licencia).
- [ ] La sección de Presentación contiene un enlace/badge que apunta a `presentacion/Resumen_Presentacion.pptx` con ruta relativa válida.
- [ ] La imagen `design/pantalla_principal.png` está embebida con ruta relativa y se previsualiza correctamente.
- [ ] Los comandos de instalación/uso mencionan `backend/requirements.txt`, `frontend/requirements.txt`, `uvicorn src.main:app --host 0.0.0.0 --port 8082` (desde `backend/`) y `streamlit run src/app.py` (desde `frontend/`).
- [ ] Existe el archivo `LICENSE` en la raíz con el texto estándar de MIT License, y el README lo enlaza en su sección de Licencia.
- [ ] El README no incluye sección de autor/contacto ni sección dedicada a la fuente del dataset de Kaggle.
- [ ] El README no menciona instrucciones Docker para el frontend (su Dockerfile sigue vacío).
- [ ] Todo el contenido del README está en español.
- [ ] El README renderiza sin errores de sintaxis markdown en la previsualización de GitHub o de un editor local.

---

## Decisions

- **Sí:** mostrar la presentación mediante un badge/enlace de descarga a `presentacion/Resumen_Presentacion.pptx`, no imágenes de slides — GitHub no puede embeber `.pptx`, y el usuario prefirió la opción simple sin generar imágenes nuevas.
- **No:** convertir slides a PNG para preview visual — descartado explícitamente por el usuario a favor de la opción más simple.
- **Sí:** README en español — consistente con `CLAUDE.md`, notebooks, specs y comentarios de código compartido, todos en español.
- **No:** versión en inglés o bilingüe — el usuario confirmó español únicamente; se puede reconsiderar en otro spec si cambia la audiencia objetivo.
- **Sí:** incluir `design/pantalla_principal.png` como preview del dashboard — ya existe, da contexto visual sin trabajo adicional.
- **Sí:** instrucciones de instalación como comandos rápidos (pip + uvicorn/streamlit), sin Docker — el `Dockerfile` del frontend está vacío, documentar Docker solo para el backend generaría una experiencia asimétrica; el usuario prefirió mantenerlo simple.
- **Sí:** incluir badges de shields.io del stack tecnológico — da un look profesional estándar de README de portafolio.
- **Sí:** agregar sección de licencia con archivo `LICENSE` (MIT) — pedido explícito del usuario aunque el archivo no existía aún.
- **No:** sección dedicada a la fuente del dataset de Kaggle — el usuario, al elegir entre licencia y atribución del dataset, solo marcó licencia.
- **No:** sección de autor/contacto — descartada explícitamente por el usuario.

---

## Risks

| Riesgo | Mitigación |
| --- | --- |
| Los comandos de instalación/arranque documentados pueden desincronizarse si cambian `requirements.txt` o los scripts de arranque en el futuro | Los comandos se derivan directamente de los archivos reales (`backend/Dockerfile`, `frontend/src/app.py`) en el momento de escribir el README; no hay mitigación automática, es responsabilidad de mantenimiento manual al modificar backend/frontend |
| Los badges de shields.io son imágenes externas — si shields.io está caído, el README se ve con íconos rotos temporalmente | Riesgo aceptado; es el estándar de facto en READMEs de GitHub y no afecta el contenido textual |

---

## What is **not** in this spec

- Conversión de slides a imágenes PNG para preview visual de la presentación.
- Sección de autor/contacto.
- Sección o badge de atribución formal del dataset de Kaggle.
- Traducción a inglés o versión bilingüe.
- Sub-READMEs para `backend/` o `frontend/`.
- Documentación de decisiones de arquitectura interna (vendoring, duplicación de métricas) — eso vive en `CLAUDE.md`.
- Instrucciones Docker para el frontend.

Cada uno de estos, si se necesita, va en su propio spec.
