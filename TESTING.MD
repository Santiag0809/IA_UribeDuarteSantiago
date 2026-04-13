# 🧪 Casos de Prueba Manuales — Sistema de Control de Inventario

Este documento describe los casos de prueba manuales para verificar el correcto funcionamiento del sistema de control de inventario.

---

## 📋 Tabla de Contenidos

1. [Pruebas de Configuración Inicial](#1-pruebas-de-configuración-inicial)
2. [Pruebas del Módulo de Equipos](#2-pruebas-del-módulo-de-equipos)
3. [Pruebas del Módulo de Sesiones](#3-pruebas-del-módulo-de-sesiones)
4. [Pruebas de Persistencia de Datos](#4-pruebas-de-persistencia-de-datos)
5. [Pruebas de Flujo Completo](#5-pruebas-de-flujo-completo)

---

## 1. Pruebas de Configuración Inicial

### Caso 1.1: Verificar la creación de la carpeta `data`
**Descripción:** Asegurarse de que la carpeta `data` se crea automáticamente al ejecutar el programa.  
**Pasos:**
1. Eliminar la carpeta `data` si existe.
2. Ejecutar el programa.
3. Verificar que la carpeta `data` se haya creado.  
**Resultado esperado:** La carpeta `data` se crea correctamente.

### Caso 1.2: Verificar la creación de archivos JSON vacíos
**Descripción:** Asegurarse de que los archivos `equipos.json` y `sesiones.json` se crean vacíos si no existen.  
**Pasos:**
1. Eliminar los archivos `equipos.json` y `sesiones.json` si existen.
2. Ejecutar el programa.
3. Verificar que los archivos se hayan creado y estén vacíos.  
**Resultado esperado:** Los archivos `equipos.json` y `sesiones.json` se crean correctamente.

---

## 2. Pruebas del Módulo de Equipos

### Caso 2.1: Registrar un equipo nuevo
**Descripción:** Verificar que un equipo se registra correctamente.  
**Pasos:**
1. Seleccionar la opción para registrar un equipo.
2. Ingresar los datos requeridos (ID, descripción, estado, horas de uso).
3. Confirmar el registro.  
**Resultado esperado:** El equipo se guarda en `equipos.json` con los datos ingresados.

### Caso 2.2: Listar todos los equipos
**Descripción:** Verificar que se muestran todos los equipos registrados.  
**Pasos:**
1. Registrar al menos dos equipos.
2. Seleccionar la opción para listar equipos.  
**Resultado esperado:** Se muestran todos los equipos registrados con sus detalles.

---

## 3. Pruebas del Módulo de Sesiones

### Caso 3.1: Registrar un check-in
**Descripción:** Verificar que un check-in se registra correctamente.  
**Pasos:**
1. Seleccionar la opción para registrar un check-in.
2. Ingresar los datos requeridos (ID del camper, ID del equipo, hora de inicio).
3. Confirmar el registro.  
**Resultado esperado:** El check-in se guarda en `sesiones.json` con los datos ingresados.

### Caso 3.2: Registrar un check-out
**Descripción:** Verificar que un check-out se registra correctamente.  
**Pasos:**
1. Registrar un check-in.
2. Seleccionar la opción para registrar un check-out.
3. Ingresar la hora de fin.
4. Confirmar el registro.  
**Resultado esperado:** El check-out se actualiza correctamente en `sesiones.json`.

---

## 4. Pruebas de Persistencia de Datos

### Caso 4.1: Verificar la persistencia de equipos
**Descripción:** Asegurarse de que los equipos registrados se guardan correctamente en el archivo JSON.  
**Pasos:**
1. Registrar un equipo.
2. Reiniciar el programa.
3. Listar los equipos registrados.  
**Resultado esperado:** El equipo registrado aparece en la lista.

### Caso 4.2: Verificar la persistencia de sesiones
**Descripción:** Asegurarse de que las sesiones registradas se guardan correctamente en el archivo JSON.  
**Pasos:**
1. Registrar un check-in y un check-out.
2. Reiniciar el programa.
3. Listar las sesiones registradas.  
**Resultado esperado:** La sesión registrada aparece en la lista.

---

## 5. Pruebas de Flujo Completo

### Caso 5.1: Flujo completo de registro y consulta
**Descripción:** Verificar que el sistema funciona correctamente desde el registro de un equipo hasta el registro de una sesión.  
**Pasos:**
1. Registrar un equipo.
2. Registrar un check-in para el equipo.
3. Registrar un check-out para el equipo.
4. Listar los equipos y las sesiones.  
**Resultado esperado:** Los datos registrados aparecen correctamente en las listas.

### Caso 5.2: Cargar datos de demostración
**Descripción:** Verificar que los datos de demostración se cargan correctamente.  
**Pasos:**
1. Seleccionar la opción para cargar datos de demostración.
2. Listar los equipos y las sesiones.  
**Resultado esperado:** Los datos de demostración aparecen correctamente en las listas.

---

## 🛠 Notas Adicionales

- **Errores esperados:** Verificar que el sistema maneja errores como:
  - Intentar registrar un check-out sin un check-in previo.
  - Ingresar un ID de equipo inexistente.
- **Pruebas de rendimiento:** Probar con un archivo JSON que contenga más de 100 registros.
