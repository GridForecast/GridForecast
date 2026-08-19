# Project Charter — Plataforma de Forecasting Probabilístico del Sistema Eléctrico

> **Fuente única de verdad:** este repositorio. Si una decisión importante no está aquí, en una Issue o en un PR, no existe.

---

## 1. Visión

Construir un **sistema de forecasting en producción** que prediga demanda eléctrica y generación renovable en tiempo real, con incertidumbre bien calibrada, monitoreo de deriva y reentrenamiento automático, más una capa de reportes en lenguaje natural.

El objetivo **no** es investigación académica ni un notebook aislado, sino un sistema que corre, que cualquiera puede abrir en una URL, y que demuestra el ciclo completo de un data scientist moderno.

## 2. Objetivo real

Empleabilidad y portafolio. El éxito se mide por lo que un reclutador o hiring manager puede ver funcionando y verificar, no por métricas de precisión en un vacío. El diferenciador es la **ingeniería y operación alrededor del modelo**, no el modelo en sí.

Al terminar, cada integrante debe poder mostrar: un pipeline de datos en vivo, un modelo probabilístico calibrado, despliegue y monitoreo, tests y CI/CD, integración de LLM con propósito, y un dashboard público.

## 3. Alcance

**Dentro:**
- Ingesta en vivo de datos de red (ENTSO-E u operador público) + meteorología abierta.
- Almacenamiento versionado en Parquet.
- Forecasting probabilístico con cuantificación de incertidumbre (conformal prediction / intervalos calibrados).
- Backtesting y validación out-of-sample honesta.
- Despliegue del modelo + dashboard.
- Monitoreo de data drift y calibración; reentrenamiento programado.
- Capa LLM que traduce el forecast a un reporte legible.

**Fuera (por ahora):**
- Trading o recomendaciones de inversión.
- Bases de datos gestionadas caras.
- GPUs y tiers premium sin milestone que lo justifique.
- Cualquier recurso cloud always-on ocioso.

## 4. Equipo y roles

Cada rol tiene un dueño; el sombrero de **revisor rota cada sprint** para que todos toquen todo.

| Rol | Dueño | Responsabilidad principal |
|-----|-------|---------------------------|
| **Data & Infra** | _(por asignar)_ | Ingesta en vivo, almacenamiento, nube y **dueño del presupuesto** |
| **Modeling** | _(por asignar)_ | Forecasting probabilístico, incertidumbre, calibración |
| **MLOps & Monitoring** | _(por asignar)_ | Despliegue, drift detection, reentrenamiento, CI/CD |
| **Product & GenAI** | _(por asignar)_ | Dashboard, capa LLM de reportes, documentación, narrativa |

## 5. Metodología

**Kanban con sprints de 2 semanas, todo anclado a GitHub.**

- Cada tarea (feature, modelo, bug) es una **Issue**.
- Tablero de columnas: `Backlog → En progreso → En revisión → Hecho`.
- Cada tarea sale en una **rama propia** → **Pull Request** → **revisión obligatoria de un compañero** → merge.
- **Nadie** hace push directo a `main`.
- Demo quincenal al cerrar el sprint.

**Ritmos:**
- **Standup asíncrono diario** en el chat (3 líneas: qué hice, qué haré, qué me bloquea).
- **Sync semanal** de 30 min: repaso del tablero + captura de costos cloud.
- **Retro** al final de cada sprint (qué funcionó, qué no, un ajuste).

## 6. Stack de herramientas

| Necesidad | Herramienta | Costo | Cuándo se adopta |
|-----------|-------------|-------|------------------|
| Código, tareas, docs | **GitHub** (repo + Projects + Wiki) | Gratis | Semana 0 |
| Comunicación | **Discord / Slack** (asíncrono por defecto) | Gratis | Semana 0 |
| Videollamada | **Google Meet / Discord** | Gratis | Semana 0 |
| Experiment tracking | **MLflow** (local/autoalojado) | Gratis | Semana ~4 |
| Dashboard | **Streamlit** | Gratis local | Cuando haya algo que mostrar |
| Nube | **Azure** (serverless, scale-to-zero) | ~5–20 USD/mes austero | Fase de despliegue |

> **Regla:** no adoptar una herramienta hasta necesitarla de verdad. Se arranca solo con GitHub y el chat.

## 7. Definition of Done

Una tarea está *hecha* solo si cumple **todo**:

- [ ] Código/notebook reproducible desde cero.
- [ ] Chequeo out-of-sample donde aplique.
- [ ] Revisión de código aprobada por un compañero.
- [ ] Entrada en la documentación.
- [ ] **Cost gate**: si crea un recurso cloud, se verificó el precio en la calculadora de Azure *antes* de crearlo.

## 8. Control de costos (blindaje anti-sorpresas)

- **Azure Budgets con alertas al 50 / 80 / 100 %** — protección número uno.
- Suscripción con crédito de estudiante y límite de gasto activado.
- Todo serverless / scale-to-zero; auto-shutdown en cualquier VM.
- Un solo resource group, todo etiquetado.
- Revisión de costos de 5 min en cada sync semanal.

**Estimado:** ~5–20 USD/mes en modo austero; probablemente **0 USD** los primeros meses con Azure for Students (100 USD de crédito) + GitHub Student Pack.

## 9. Calendario (~14 semanas)

| Fase | Semanas | Entregable |
|------|---------|------------|
| Setup | 0 | Repo, roles, presupuesto con alertas, fuente de datos elegida |
| Ingesta | 1–3 | Datos limpios fluyendo (local/serverless) |
| Modelado | 4–7 | Forecasting probabilístico + evaluación rigurosa |
| Monitoreo | 8–10 | Drift detection + reentrenamiento |
| Despliegue | 11–13 | Dashboard + backtesting con validación honesta |
| Cierre | 14+ | Documentación, writeup de portafolio, capa LLM |

## 10. Backlog del Sprint 0 (setup)

Convertir cada punto en una Issue y asignarla:

1. Crear la organización/repo en GitHub e invitar a los cuatro.
2. Configurar branch protection en `main` (PR + 1 review obligatorio).
3. Crear el tablero en GitHub Projects con las cuatro columnas.
4. Montar el servidor de Discord/Slack y conectar notificaciones de GitHub.
5. Asignar los cuatro roles (usar el diagnóstico de skills del equipo).
6. Crear la suscripción de Azure for Students y configurar Budgets + alertas.
7. Investigar y decidir la fuente de datos de red (ENTSO-E vs operador local).
8. Escribir el `README.md` con setup del entorno (Python, dependencias).

## 11. Normas de trabajo

- **Asíncrono por defecto.** El chat es para desbloquear rápido; las decisiones van a GitHub.
- **Revisar el código del otro es aprender**, no vigilar.
- Ninguna herramienta nueva sin necesidad real.
- El encuadre del proyecto es **investigación y educación**, nunca recomendación de inversión.
