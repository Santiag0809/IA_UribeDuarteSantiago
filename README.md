# 📦 Sistema de Control de Inventario — Cajasan × Campuslands
 
Aplicación de consola en Python para gestionar los equipos electrónicos
prestados por **Cajasan** a los campers de **Campuslands**: trazabilidad de uso,
reportes de incidencias, mantenimiento preventivo y sistema disciplinario.
 
---
 
## 🚀 Ejecución Rápida
 
```bash
# Requisito: Python 3.8 o superior (sin librerías externas)
python cajasan_inventario.py
```
 
> **Tip:** Selecciona la opción `6 → Cargar datos de demostración` para
> explorar el sistema sin ingresar datos manualmente.
 
---
 
## 🗂 Módulos del Sistema
 
| # | Módulo | Qué resuelve |
|---|--------|--------------|
| 1 | **Equipos** | Registro, estados y accesorios por unidad |
| 2 | **Campers** | Registro y puntuación disciplinaria |
| 3 | **Sesiones** | Check-in / Check-out con trazabilidad completa |
| 4 | **Reportes** | Incidencias centralizadas con seguimiento |
| 5 | **Dashboard** | Resumen en tiempo real del inventario |
| 6 | **Demo** | Datos de muestra para pruebas rápidas |
 
---
 
## 🤖 Prompts Utilizados (Discovery → Código)
 
### 1 · Definición del contexto y rol
 
```
Actúa como un Product Owner experto en discovery de producto.
Tu objetivo es ayudarme a identificar problemáticas, necesidades
y posibles soluciones a través de una serie de preguntas (máximo 10).
 
Realiza solo una pregunta a la vez. No avances a soluciones hasta
tener claras las problemáticas.
 
Contexto: Cajasan presta sus instalaciones a Campuslands. Los campers
usan equipos electrónicos de Cajasan sin ningún sistema de control
de inventario.
```
 
---
 
### 2 · Generación de soluciones estructuradas
 
Tras completar el discovery, se proporcionaron las problemáticas
priorizadas y se solicitó al modelo mapear cada una a una solución
concreta. El output fue:
 
```
Por cada problemática identificada, propón una solución con:
- Nombre de la solución
- Cómo funciona (pasos)
- Reglas clave
- Resultado esperado
```
 
---
 
### 3 · Generación del código Python
 
```
Basándote en la problemática descrita y las posibles soluciones
propuestas, desarrolla una aplicación de consola utilizando Python.
 
El programa debe ser:
- Funcional y bien estructurado
- Con comentarios explicativos en el código
- Con manejo adecuado de entrada y salida de datos
- Aplicando buenas prácticas de programación
- Con instrucciones básicas para su ejecución
```
 
---
 
### 4 · Generación del commit y README
 
```
Generame un conventional commit para este archivo y un README que
simplifique los prompts utilizados + la ejecución del programa.
```
 
---
 
## ⚙️ Flujo de Uso Recomendado
 
```
1. Cargar datos demo          →  Opción 6
2. Ver Dashboard              →  Opción 5
3. Registrar Check-In         →  Opción 3 → 1
4. Registrar un reporte       →  Opción 4 → 1
5. Hacer Check-Out            →  Opción 3 → 2
6. Ver estado del camper      →  Opción 2 → 2
```
 
---
 
## 📊 Sistema de Puntuación
 
| Evento | Puntos |
|--------|--------|
| Buen uso (check-in) | +1 |
| Reportar una falla | +2 |
| Daño leve / accesorio perdido | -3 |
| Daño grave | -10 |
 
| Puntuación | Estado |
|------------|--------|
| > -5 | 🟢 Normal |
| -5 a -14 | 🟡 Advertencia |
| -15 a -24 | 🟠 Restricción de uso |
| ≤ -25 | 🔴 Evaluación disciplinaria |
 
---
 
## 🔧 Mantenimiento Preventivo — Triggers Automáticos
 
El sistema cambia el estado del equipo a `revision_pendiente` cuando:
 
- Acumula **3 o más reportes**
- Supera **100 horas de uso**
- Han pasado **30 días** desde la última revisión
 
---
 
## 📁 Estructura del Proyecto
 
```
cajasan_inventario.py   ← Aplicación principal (módulo único)
COMMIT_MESSAGE.txt      ← Conventional commit listo para usar
README.md               ← Este archivo
```
 
---
 
## 🧩 Próximos Pasos Sugeridos
 
- [ ] Migrar la capa de datos a SQLite o PostgreSQL
- [ ] Agregar exportación de reportes a CSV / Excel
- [ ] Implementar autenticación por rol (admin Cajasan / admin Campus / camper)
- [ ] Desarrollar interfaz web con Flask o FastAPI
- [ ] Integrar escaneo real de QR con la librería `qrcode`
