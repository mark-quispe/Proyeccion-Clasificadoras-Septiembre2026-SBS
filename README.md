# Proyección de Clasificaciones de Riesgo SBS - Septiembre 2026

Este proyecto realiza la proyección semestral de las clasificaciones de riesgo para las entidades financieras supervisadas por la **Superintendencia de Banca, Seguros y AFP (SBS)** del Perú para el periodo **Septiembre 2026**. Dado que dicho periodo aún no ha sido publicado oficialmente por la SBS, el modelo infiere y proyecta las notas de riesgo basándose en el comportamiento histórico de los periodos **Septiembre 2025** y **Marzo 2026**.

---

## 👥 Integrantes del Proyecto
* **Mark Quispe Gonzales**
* **Yoshiro Vilchez Cardich**
* **Yunior Yanac Minaya**

---

## 🧠 Metodología y Lógica del Modelo

La proyección a Septiembre 2026 utiliza un modelo híbrido cuantitativo sustentado en los siguientes pilares:

1. **Mapeo Ordinal Numérico:**
   Para poder realizar análisis matemático sobre las notas cualitativas de la SBS, se implementa una escala ordinal numérica:
   * `A+` $\rightarrow$ 12 | `A` $\rightarrow$ 11 | `A-` $\rightarrow$ 10
   * `B+` $\rightarrow$ 9 | `B` $\rightarrow$ 8 | `B-` $\rightarrow$ 7
   * `C+` $\rightarrow$ 6 | `C` $\rightarrow$ 5 | `C-` $\rightarrow$ 4
   * `D+` $\rightarrow$ 3 | `D` $\rightarrow$ 2 | `E` $\rightarrow$ 1
   * `RET` (Retirada) $\rightarrow$ 0

2. **Funcionamiento del Proceso de Predicción:**
   La estimación matemática del rating de cada entidad financiera para $T_2$ (Septiembre 2026) consta de 4 fases ejecutadas automáticamente por el algoritmo:
   
   * **Paso 1: Extracción Estructurada:** El motor parsea las tablas HTML oficiales (`septiembre2025.xls` y `marzo2026.xls`), aislando los textos de clasificación y los metadatos de cambio (`↑` o `↓`) emitidos por cada una de las 6 clasificadoras para cada entidad financiera.
   * **Paso 2: Evaluación del Vector de Cambio (T0 a T1):** Compara el rating numérico en $T_0$ (Septiembre 2025) con el de $T_1$ (Marzo 2026) para establecer el delta individual por clasificadora.
   * **Paso 3: Cálculo del Momentum Estocástico:** El rating proyectado para $T_2$ (Septiembre 2026) se calcula aplicando el factor de momentum sobre el último estado registrado en Marzo 2026 ($R_{T_1}$):
     $$R_{T_2} = R_{T_1} + \Delta_{\text{momentum}}$$
     Donde:
     * Si la clasificadora registró una mejora en $T_1$ (o flecha de subida `↑` activa): $\Delta_{\text{momentum}} = +0.5$ de notch de score numérico, reflejando consolidación o mejora incremental.
     * Si registró un deterioro en $T_1$ (o flecha de bajada `↓` activa): $\Delta_{\text{momentum}} = -0.5$ de notch de score numérico.
     * Si se mantuvo sin cambios (estado estable): $\Delta_{\text{momentum}} = 0$.
   * **Paso 4: Cálculo de Score y Rating Consenso:** 
     Para consolidar el análisis a nivel de entidad financiera y eliminar el sesgo individual de las clasificadoras, se calcula un promedio ponderado de las notas numéricas activas:
     $$Score_{\text{Consenso}} = \frac{1}{N} \sum_{i=1}^{N} R_{i}$$
     *(Donde $N$ es el número de clasificadoras que evaluaron a la entidad).*
     Este score se redondea al entero más cercano para mapear la nota cualitativa consenso final (ej. un score de `10.75` se traduce en una nota consenso proyectada de `A`).

3. **Categorización de Riesgo Consolidado:**
   Según el score consenso obtenido, las entidades son agrupadas en 6 niveles de alerta de riesgo:
   * **Riesgo Mínimo:** $\ge 11.5$ (`A+`)
   * **Bajo Riesgo:** $\ge 9.5$ y $< 11.5$ (`A` / `A-`)
   * **Riesgo Moderado:** $\ge 7.5$ y $< 9.5$ (`B+` / `B`)
   * **Riesgo Medio-Alto:** $\ge 5.5$ y $< 7.5$ (`B-` / `C+`)
   * **Alto Riesgo:** $\ge 3.5$ y $< 5.5$ (`C` / `C-`)
   * **Riesgo Crítico / Estrés:** $< 3.5$ (`D` / `RET`)

---

## 📁 Estructura del Repositorio

* **`Data/`:** Contiene los insumos y los reportes resultantes:
  * `septiembre2025.xls` y `marzo2026.xls`: Reportes HTML oficiales descargados del portal SBS.
  * `septiembre2026_proyeccion.xlsx`: Documento Excel final de salida con tres pestañas (Matriz SBS proyectada, Resumen de Score Consenso por entidad y Transiciones detalladas por clasificadora).
  * `septiembre2026_proyeccion.csv`: Matriz proyectada en formato CSV.
  * `resumen_entidades_riesgo.csv`: Resumen consolidado de tendencia y score numérico.
* **`src/`:** Código fuente en Python:
  * `project_september2026.py`: Parser HTML de datos, cálculo del modelo de proyección de ratings y generación de archivos Excel/CSV de salida.
  * `build_dashboard.py`: Script compilador que genera la interfaz gráfica interactiva.
* **`index.html`:** Dashboard interactivo web autoejecutable. Permite filtrar la data proyectada de forma dinámica por tipo de entidad, nombre y periodo semestral.

---

## 🛠️ Requisitos e Instrucciones de Uso

### Prerrequisitos
Tener instalado Python 3.8+. Las dependencias necesarias se encuentran listadas en el archivo `requirements.txt`. Puedes instalarlas todas juntas ejecutando el siguiente comando en tu terminal:

```bash
pip install -r requirements.txt
```

### Ejecución del Pipeline
Si modificas los archivos origen o deseas actualizar los datos de la proyección, puedes volver a generar los resultados y el dashboard ejecutando en la raíz del proyecto:

1. **Calcular la proyección de riesgo:**
   ```bash
   python src/project_september2026.py
   ```
2. **Recompilar el Dashboard Interactivo:**
   ```bash
   python src/build_dashboard.py
   ```

Una vez completado, puedes abrir el archivo `index.html` directamente en tu navegador favorito para visualizar los resultados interactivos.
