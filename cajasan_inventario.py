"""
============================================================
  SISTEMA DE CONTROL DE INVENTARIO - CAJASAN × CAMPUSLANDS
============================================================
Descripción:
    Aplicación de consola en Python para gestionar el inventario
    de equipos electrónicos prestados por Cajasan a los campers
    de Campuslands. Incluye check-in/check-out, reportes de
    incidencias, mantenimiento preventivo y sistema de puntuación.

Ejecución:
    python cajasan_inventario.py

Requisitos:
    Python 3.8 o superior (sin dependencias externas)

Autor: Generado como solución al discovery de producto Cajasan × Campuslands
"""

import os
import json
from datetime import datetime, timedelta
from typing import Optional

# ─────────────────────────────────────────────
# CONSTANTES DE CONFIGURACIÓN
# ─────────────────────────────────────────────

UMBRAL_REPORTES_MANTENIMIENTO = 3   # Reportes acumulados antes de mantenimiento
HORAS_USO_MANTENIMIENTO = 100       # Horas de uso antes de revisión preventiva
DIAS_MANTENIMIENTO_PERIODICO = 30   # Días entre revisiones periódicas

# Puntuación del sistema disciplinario
PUNTOS = {
    "buen_uso": 1,
    "reporte_falla": 2,
    "danio_leve": -3,
    "danio_grave": -10,
}

# Umbrales disciplinarios
UMBRAL_ADVERTENCIA = -5
UMBRAL_RESTRICCION = -15
UMBRAL_DISCIPLINARIO = -25

# Estados válidos de equipos
ESTADOS_EQUIPO = ["operativo", "revision_pendiente", "fuera_de_servicio"]

# Tipos de incidencia válidos
TIPOS_INCIDENCIA = ["software", "hardware_leve", "hardware_grave", "accesorio_perdido", "suciedad"]

# Accesorios estándar por equipo
ACCESORIOS_ESTANDAR = ["cable_poder", "mouse", "teclado"]


# ─────────────────────────────────────────────
# CAPA DE DATOS (simulación en memoria)
# ─────────────────────────────────────────────

# Diccionario principal de equipos
# Clave: ID del equipo | Valor: dict con atributos del equipo
equipos: dict = {}

# Diccionario de campers registrados
# Clave: ID del camper | Valor: dict con datos y puntuación
campers: dict = {}

# Lista de sesiones activas (check-in sin check-out)
sesiones_activas: list = []

# Historial completo de sesiones cerradas
historial_sesiones: list = []

# Lista de reportes de incidencias
reportes: list = []

# Contador global de IDs para reportes
contador_reporte = 1


# ─────────────────────────────────────────────
# UTILIDADES GENERALES
# ─────────────────────────────────────────────

def limpiar_pantalla():
    """Limpia la consola según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def timestamp_actual() -> str:
    """Retorna la fecha y hora actual como string formateado."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input("\n  Presiona Enter para continuar...")


def separador(titulo: str = ""):
    """Imprime una línea decorativa con título opcional."""
    linea = "─" * 55
    if titulo:
        print(f"\n  ┌{linea}┐")
        print(f"  │  {titulo.upper().center(53)}│")
        print(f"  └{linea}┘")
    else:
        print(f"  {linea}")


def validar_opcion(opciones: list) -> str:
    """
    Solicita al usuario una opción válida dentro de una lista dada.
    Repite la solicitud hasta obtener una entrada válida.
    """
    while True:
        entrada = input("  → Opción: ").strip()
        if entrada in opciones:
            return entrada
        print(f"  ⚠  Opción inválida. Elige entre: {', '.join(opciones)}")


def evaluar_estado_disciplinario(camper_id: str) -> str:
    """
    Evalúa el estado disciplinario de un camper según su puntuación acumulada.
    Retorna el nivel de alerta correspondiente.
    """
    puntuacion = campers[camper_id]["puntuacion"]
    if puntuacion <= UMBRAL_DISCIPLINARIO:
        return "🔴 EVALUACIÓN DISCIPLINARIA"
    elif puntuacion <= UMBRAL_RESTRICCION:
        return "🟠 RESTRICCIÓN DE USO"
    elif puntuacion <= UMBRAL_ADVERTENCIA:
        return "🟡 ADVERTENCIA"
    else:
        return "🟢 NORMAL"


def verificar_mantenimiento(equipo_id: str):
    """
    Verifica si un equipo requiere mantenimiento preventivo basado en:
    - Número de reportes acumulados
    - Horas de uso acumuladas
    - Días desde la última revisión
    Actualiza el estado del equipo si corresponde.
    """
    equipo = equipos[equipo_id]

    reportes_equipo = sum(1 for r in reportes if r["equipo_id"] == equipo_id)
    horas_uso = equipo.get("horas_uso", 0)
    ultima_revision = equipo.get("ultima_revision")

    necesita_mantenimiento = False
    motivo = ""

    if reportes_equipo >= UMBRAL_REPORTES_MANTENIMIENTO:
        necesita_mantenimiento = True
        motivo = f"{reportes_equipo} reportes acumulados"

    if horas_uso >= HORAS_USO_MANTENIMIENTO:
        necesita_mantenimiento = True
        motivo = f"{horas_uso} horas de uso"

    if ultima_revision:
        fecha_revision = datetime.strptime(ultima_revision, "%Y-%m-%d %H:%M")
        dias_transcurridos = (datetime.now() - fecha_revision).days
        if dias_transcurridos >= DIAS_MANTENIMIENTO_PERIODICO:
            necesita_mantenimiento = True
            motivo = f"{dias_transcurridos} días sin revisión"

    if necesita_mantenimiento and equipo["estado"] == "operativo":
        equipos[equipo_id]["estado"] = "revision_pendiente"
        print(f"\n  ⚙  ALERTA: Equipo {equipo_id} requiere mantenimiento preventivo.")
        print(f"     Motivo: {motivo}")


# ─────────────────────────────────────────────
# MÓDULO 1: GESTIÓN DE EQUIPOS
# ─────────────────────────────────────────────

def registrar_equipo():
    """Registra un nuevo equipo en el sistema con sus accesorios estándar."""
    separador("Registrar Equipo")

    equipo_id = input("  ID único del equipo (ej. PC-001): ").strip().upper()
    if not equipo_id:
        print("  ⚠  El ID no puede estar vacío.")
        return

    if equipo_id in equipos:
        print(f"  ⚠  El equipo {equipo_id} ya está registrado.")
        return

    descripcion = input("  Descripción (ej. Laptop HP 14): ").strip()
    ubicacion = input("  Ubicación (ej. Aula 3 - Puesto 12): ").strip()

    # Registrar accesorios individuales para este equipo
    accesorios = {}
    print(f"\n  Accesorios estándar: {', '.join(ACCESORIOS_ESTANDAR)}")
    for acc in ACCESORIOS_ESTANDAR:
        estado_acc = input(f"  ¿{acc} presente? (s/n): ").strip().lower()
        accesorios[acc] = estado_acc == "s"

    equipos[equipo_id] = {
        "id": equipo_id,
        "descripcion": descripcion,
        "ubicacion": ubicacion,
        "estado": "operativo",
        "accesorios": accesorios,
        "horas_uso": 0,
        "ultima_revision": timestamp_actual(),
        "fecha_registro": timestamp_actual(),
    }

    print(f"\n  ✅ Equipo {equipo_id} registrado exitosamente.")


def listar_equipos():
    """Muestra el listado completo de equipos con su estado actual."""
    separador("Inventario de Equipos")

    if not equipos:
        print("  No hay equipos registrados.")
        return

    # Encabezado de la tabla
    print(f"\n  {'ID':<10} {'Descripción':<22} {'Estado':<22} {'Horas':>6}")
    separador()

    for eq in equipos.values():
        # Indicador visual según estado
        icono = {"operativo": "🟢", "revision_pendiente": "🟡", "fuera_de_servicio": "🔴"}.get(eq["estado"], "⚪")
        print(f"  {eq['id']:<10} {eq['descripcion']:<22} {icono} {eq['estado']:<18} {eq['horas_uso']:>6}h")

    separador()
    print(f"  Total equipos: {len(equipos)}")


def cambiar_estado_equipo():
    """Permite cambiar manualmente el estado de un equipo."""
    separador("Cambiar Estado de Equipo")

    listar_equipos()
    equipo_id = input("\n  ID del equipo a actualizar: ").strip().upper()

    if equipo_id not in equipos:
        print("  ⚠  Equipo no encontrado.")
        return

    print(f"\n  Estado actual: {equipos[equipo_id]['estado']}")
    print(f"  Estados disponibles:")
    for i, est in enumerate(ESTADOS_EQUIPO, 1):
        print(f"    {i}. {est}")

    opcion = validar_opcion([str(i) for i in range(1, len(ESTADOS_EQUIPO) + 1)])
    nuevo_estado = ESTADOS_EQUIPO[int(opcion) - 1]

    equipos[equipo_id]["estado"] = nuevo_estado

    # Si pasa a revisión completada, actualizar fecha de revisión
    if nuevo_estado == "operativo":
        equipos[equipo_id]["ultima_revision"] = timestamp_actual()

    print(f"\n  ✅ Estado de {equipo_id} actualizado a: {nuevo_estado}")


# ─────────────────────────────────────────────
# MÓDULO 2: GESTIÓN DE CAMPERS
# ─────────────────────────────────────────────

def registrar_camper():
    """Registra un nuevo camper en el sistema con puntuación inicial."""
    separador("Registrar Camper")

    camper_id = input("  ID del camper (ej. C-2024-001): ").strip().upper()
    if not camper_id:
        print("  ⚠  El ID no puede estar vacío.")
        return

    if camper_id in campers:
        print(f"  ⚠  El camper {camper_id} ya está registrado.")
        return

    nombre = input("  Nombre completo: ").strip()
    email = input("  Email (opcional): ").strip()

    campers[camper_id] = {
        "id": camper_id,
        "nombre": nombre,
        "email": email,
        "puntuacion": 10,           # Puntuación inicial positiva
        "sesiones_totales": 0,
        "fecha_registro": timestamp_actual(),
    }

    print(f"\n  ✅ Camper {nombre} registrado con ID {camper_id}.")


def listar_campers():
    """Muestra el listado de campers con su estado disciplinario."""
    separador("Listado de Campers")

    if not campers:
        print("  No hay campers registrados.")
        return

    print(f"\n  {'ID':<15} {'Nombre':<25} {'Puntos':>7}  Estado")
    separador()

    for cp in campers.values():
        estado = evaluar_estado_disciplinario(cp["id"])
        print(f"  {cp['id']:<15} {cp['nombre']:<25} {cp['puntuacion']:>7}  {estado}")

    separador()


def ajustar_puntuacion_camper(camper_id: str, tipo_evento: str):
    """
    Aplica el ajuste de puntuación correspondiente a un camper según el evento.
    Muestra alerta si cruza un umbral disciplinario.
    """
    if camper_id not in campers or tipo_evento not in PUNTOS:
        return

    delta = PUNTOS[tipo_evento]
    campers[camper_id]["puntuacion"] += delta

    estado = evaluar_estado_disciplinario(camper_id)
    nombre = campers[camper_id]["nombre"]

    print(f"\n  📊 Puntuación de {nombre}: {campers[camper_id]['puntuacion']} ({'+' if delta > 0 else ''}{delta})")

    # Mostrar alerta si el estado no es normal
    if "NORMAL" not in estado:
        print(f"  {estado} — Se recomienda revisión del caso.")


# ─────────────────────────────────────────────
# MÓDULO 3: CHECK-IN / CHECK-OUT
# ─────────────────────────────────────────────

def check_in():
    """
    Registra el inicio de sesión de un camper con un equipo específico.
    Valida disponibilidad del equipo y que el camper no tenga sesión activa.
    """
    separador("Check-In de Sesión")

    camper_id = input("  ID del camper: ").strip().upper()
    if camper_id not in campers:
        print("  ⚠  Camper no encontrado. Regístralo primero.")
        return

    # Verificar que el camper no tenga sesión activa
    sesion_existente = next((s for s in sesiones_activas if s["camper_id"] == camper_id), None)
    if sesion_existente:
        print(f"  ⚠  El camper ya tiene una sesión activa con el equipo {sesion_existente['equipo_id']}.")
        return

    equipo_id = input("  ID del equipo a usar: ").strip().upper()
    if equipo_id not in equipos:
        print("  ⚠  Equipo no encontrado.")
        return

    equipo = equipos[equipo_id]

    # Verificar que el equipo esté operativo
    if equipo["estado"] != "operativo":
        print(f"  ⚠  El equipo {equipo_id} no está disponible (estado: {equipo['estado']}).")
        return

    # Verificar que el equipo no tenga sesión activa
    equipo_en_uso = next((s for s in sesiones_activas if s["equipo_id"] == equipo_id), None)
    if equipo_en_uso:
        print(f"  ⚠  El equipo ya está en uso por el camper {equipo_en_uso['camper_id']}.")
        return

    # Mostrar estado de accesorios al iniciar
    print(f"\n  📋 Accesorios al momento del check-in:")
    for acc, presente in equipo["accesorios"].items():
        estado_acc = "✅" if presente else "❌"
        print(f"     {estado_acc} {acc}")

    confirmacion = input("\n  ¿Confirmas el estado de los accesorios? (s/n): ").strip().lower()
    if confirmacion != "s":
        print("  ℹ  Reporta el accesorio faltante antes de iniciar sesión.")
        return

    # Registrar sesión activa
    sesion = {
        "id": f"SES-{len(historial_sesiones) + len(sesiones_activas) + 1:04d}",
        "camper_id": camper_id,
        "equipo_id": equipo_id,
        "inicio": timestamp_actual(),
        "fin": None,
        "accesorios_inicio": dict(equipo["accesorios"]),
    }

    sesiones_activas.append(sesion)

    # Sumar punto por buen uso al iniciar
    ajustar_puntuacion_camper(camper_id, "buen_uso")
    campers[camper_id]["sesiones_totales"] += 1

    print(f"\n  ✅ Check-in exitoso — Sesión {sesion['id']} iniciada.")
    print(f"     Camper: {campers[camper_id]['nombre']} | Equipo: {equipo_id} | Hora: {sesion['inicio']}")

    # Verificar si el equipo necesita mantenimiento
    verificar_mantenimiento(equipo_id)


def check_out():
    """
    Cierra la sesión activa de un camper, verifica accesorios y
    registra el estado final del equipo.
    """
    separador("Check-Out de Sesión")

    camper_id = input("  ID del camper: ").strip().upper()
    if camper_id not in campers:
        print("  ⚠  Camper no encontrado.")
        return

    # Buscar sesión activa del camper
    sesion = next((s for s in sesiones_activas if s["camper_id"] == camper_id), None)
    if not sesion:
        print("  ⚠  El camper no tiene sesión activa.")
        return

    equipo_id = sesion["equipo_id"]
    equipo = equipos[equipo_id]

    print(f"\n  Equipo: {equipo_id} | Iniciado: {sesion['inicio']}")
    print(f"\n  📋 Verificación de accesorios al check-out:")

    accesorios_fin = {}
    accesorio_perdido = False

    for acc, presente_inicio in sesion["accesorios_inicio"].items():
        if presente_inicio:
            respuesta = input(f"  ¿'{acc}' sigue presente? (s/n): ").strip().lower()
            accesorios_fin[acc] = respuesta == "s"
            if not accesorios_fin[acc]:
                print(f"  ⚠  ACCESORIO FALTANTE: {acc}")
                accesorio_perdido = True
                ajustar_puntuacion_camper(camper_id, "danio_leve")
        else:
            accesorios_fin[acc] = False

    # Actualizar accesorios del equipo
    equipos[equipo_id]["accesorios"] = accesorios_fin

    # Calcular horas de uso aproximadas (simplificado a 2h por sesión en demo)
    equipos[equipo_id]["horas_uso"] += 2

    # Preguntar estado general del equipo
    print(f"\n  ¿El equipo presenta algún problema? (s/n): ", end="")
    tiene_problema = input().strip().lower() == "s"

    if tiene_problema:
        print("  Registra el problema a través del módulo de Reportes.")

    # Cerrar sesión
    sesion["fin"] = timestamp_actual()
    sesion["accesorios_fin"] = accesorios_fin
    sesion["accesorio_perdido"] = accesorio_perdido

    historial_sesiones.append(sesion)
    sesiones_activas.remove(sesion)

    print(f"\n  ✅ Check-out exitoso — Sesión {sesion['id']} cerrada.")

    # Verificar mantenimiento post-sesión
    verificar_mantenimiento(equipo_id)


def ver_sesiones_activas():
    """Muestra todas las sesiones de uso actualmente en curso."""
    separador("Sesiones Activas")

    if not sesiones_activas:
        print("  No hay sesiones activas en este momento.")
        return

    print(f"\n  {'Sesión':<12} {'Camper':<15} {'Equipo':<10} {'Inicio':<17}")
    separador()

    for s in sesiones_activas:
        nombre = campers[s["camper_id"]]["nombre"]
        print(f"  {s['id']:<12} {s['camper_id']:<15} {s['equipo_id']:<10} {s['inicio']:<17}")

    separador()
    print(f"  Total sesiones activas: {len(sesiones_activas)}")


# ─────────────────────────────────────────────
# MÓDULO 4: REPORTES DE INCIDENCIAS
# ─────────────────────────────────────────────

def crear_reporte():
    """
    Permite registrar una incidencia vinculada a un equipo y camper,
    con tipo de falla, descripción y evidencia textual.
    """
    global contador_reporte
    separador("Registrar Reporte de Incidencia")

    camper_id = input("  ID del camper que reporta: ").strip().upper()
    if camper_id not in campers:
        print("  ⚠  Camper no encontrado.")
        return

    equipo_id = input("  ID del equipo con problema: ").strip().upper()
    if equipo_id not in equipos:
        print("  ⚠  Equipo no encontrado.")
        return

    print("\n  Tipos de incidencia:")
    for i, tipo in enumerate(TIPOS_INCIDENCIA, 1):
        print(f"    {i}. {tipo}")

    opcion = validar_opcion([str(i) for i in range(1, len(TIPOS_INCIDENCIA) + 1)])
    tipo_incidencia = TIPOS_INCIDENCIA[int(opcion) - 1]

    descripcion = input("  Descripción del problema: ").strip()
    evidencia = input("  Referencia de evidencia (foto/video ID, opcional): ").strip()

    reporte_id = f"REP-{contador_reporte:04d}"
    contador_reporte += 1

    reporte = {
        "id": reporte_id,
        "camper_id": camper_id,
        "equipo_id": equipo_id,
        "tipo": tipo_incidencia,
        "descripcion": descripcion,
        "evidencia": evidencia,
        "estado": "abierto",
        "fecha_creacion": timestamp_actual(),
        "fecha_resolucion": None,
    }

    reportes.append(reporte)

    # Ajustar puntuación según tipo de incidencia
    if tipo_incidencia == "hardware_grave":
        ajustar_puntuacion_camper(camper_id, "danio_grave")
    elif tipo_incidencia in ["hardware_leve", "accesorio_perdido"]:
        ajustar_puntuacion_camper(camper_id, "danio_leve")
    else:
        # Reportar falla de software o suciedad suma puntos por responsabilidad
        ajustar_puntuacion_camper(camper_id, "reporte_falla")

    # Verificar si el equipo necesita pasar a mantenimiento
    verificar_mantenimiento(equipo_id)

    print(f"\n  ✅ Reporte {reporte_id} creado exitosamente.")


def listar_reportes():
    """Muestra todos los reportes registrados con su estado actual."""
    separador("Listado de Reportes")

    if not reportes:
        print("  No hay reportes registrados.")
        return

    print(f"\n  {'ID':<10} {'Equipo':<10} {'Tipo':<20} {'Estado':<12} {'Fecha'}")
    separador()

    for r in reportes:
        icono = {"abierto": "🔴", "en_proceso": "🟡", "resuelto": "🟢"}.get(r["estado"], "⚪")
        print(f"  {r['id']:<10} {r['equipo_id']:<10} {r['tipo']:<20} {icono} {r['estado']:<10} {r['fecha_creacion']}")

    separador()
    abiertos = sum(1 for r in reportes if r["estado"] == "abierto")
    print(f"  Total reportes: {len(reportes)} | Abiertos: {abiertos}")


def actualizar_reporte():
    """Permite cambiar el estado de un reporte existente."""
    separador("Actualizar Estado de Reporte")

    listar_reportes()
    reporte_id = input("\n  ID del reporte a actualizar: ").strip().upper()

    reporte = next((r for r in reportes if r["id"] == reporte_id), None)
    if not reporte:
        print("  ⚠  Reporte no encontrado.")
        return

    print(f"\n  Estado actual: {reporte['estado']}")
    print("  Nuevos estados: 1. en_proceso  2. resuelto")
    opcion = validar_opcion(["1", "2"])

    nuevo_estado = "en_proceso" if opcion == "1" else "resuelto"
    reporte["estado"] = nuevo_estado

    if nuevo_estado == "resuelto":
        reporte["fecha_resolucion"] = timestamp_actual()
        print(f"  ✅ Reporte {reporte_id} marcado como resuelto.")
    else:
        print(f"  ✅ Reporte {reporte_id} marcado como en proceso.")


# ─────────────────────────────────────────────
# MÓDULO 5: DASHBOARD / RESUMEN
# ─────────────────────────────────────────────

def mostrar_dashboard():
    """Muestra un resumen ejecutivo del estado actual del sistema."""
    separador("Dashboard General")

    # Conteo de equipos por estado
    total_equipos = len(equipos)
    operativos = sum(1 for e in equipos.values() if e["estado"] == "operativo")
    revision = sum(1 for e in equipos.values() if e["estado"] == "revision_pendiente")
    fuera_servicio = sum(1 for e in equipos.values() if e["estado"] == "fuera_de_servicio")

    # Conteo de reportes
    total_reportes = len(reportes)
    reportes_abiertos = sum(1 for r in reportes if r["estado"] == "abierto")

    # Conteo de campers con alertas
    campers_alerta = sum(
        1 for c in campers
        if "NORMAL" not in evaluar_estado_disciplinario(c)
    )

    print(f"""
  📦 INVENTARIO
  ─────────────────────────────────────
  Total equipos registrados : {total_equipos}
  🟢 Operativos             : {operativos}
  🟡 Revisión pendiente     : {revision}
  🔴 Fuera de servicio      : {fuera_servicio}

  🔧 INCIDENCIAS
  ─────────────────────────────────────
  Total reportes            : {total_reportes}
  🔴 Reportes abiertos      : {reportes_abiertos}

  👤 CAMPERS
  ─────────────────────────────────────
  Total campers             : {len(campers)}
  ⚠  Campers con alerta     : {campers_alerta}
  📍 Sesiones activas ahora : {len(sesiones_activas)}

  🕓 Última actualización   : {timestamp_actual()}
    """)


# ─────────────────────────────────────────────
# MÓDULO 6: CARGA DE DATOS DE PRUEBA
# ─────────────────────────────────────────────

def cargar_datos_demo():
    """
    Carga datos de muestra para facilitar la evaluación del sistema
    sin necesidad de ingresar información manualmente.
    """
    global contador_reporte

    # Equipos de muestra
    equipos_demo = [
        ("PC-001", "Laptop HP 14", "Aula 3 - Puesto 01"),
        ("PC-002", "Laptop Dell Inspiron", "Aula 3 - Puesto 02"),
        ("PC-003", "Laptop Lenovo IdeaPad", "Aula 3 - Puesto 03"),
        ("PC-004", "Laptop Asus VivoBook", "Aula 3 - Puesto 04"),
        ("PC-005", "Laptop HP 15", "Aula 3 - Puesto 05"),
    ]

    for eid, desc, ubic in equipos_demo:
        equipos[eid] = {
            "id": eid,
            "descripcion": desc,
            "ubicacion": ubic,
            "estado": "operativo",
            "accesorios": {acc: True for acc in ACCESORIOS_ESTANDAR},
            "horas_uso": 0,
            "ultima_revision": timestamp_actual(),
            "fecha_registro": timestamp_actual(),
        }

    # Equipos con estado especial
    equipos["PC-003"]["estado"] = "revision_pendiente"
    equipos["PC-005"]["estado"] = "fuera_de_servicio"

    # Campers de muestra
    campers_demo = [
        ("C-001", "Ana García", "ana@campus.co"),
        ("C-002", "Luis Martínez", "luis@campus.co"),
        ("C-003", "María Rodríguez", "maria@campus.co"),
        ("C-004", "Carlos López", "carlos@campus.co"),
    ]

    for cid, nombre, email in campers_demo:
        campers[cid] = {
            "id": cid,
            "nombre": nombre,
            "email": email,
            "puntuacion": 10,
            "sesiones_totales": 0,
            "fecha_registro": timestamp_actual(),
        }

    # Camper con puntuación baja (alerta)
    campers["C-004"]["puntuacion"] = -8

    # Reporte de muestra
    reportes.append({
        "id": f"REP-{contador_reporte:04d}",
        "camper_id": "C-002",
        "equipo_id": "PC-003",
        "tipo": "software",
        "descripcion": "El sistema operativo no arranca correctamente.",
        "evidencia": "IMG-2024-001",
        "estado": "abierto",
        "fecha_creacion": timestamp_actual(),
        "fecha_resolucion": None,
    })
    contador_reporte += 1

    print("\n  ✅ Datos de demostración cargados correctamente.")
    print("     5 equipos | 4 campers | 1 reporte de muestra")


# ─────────────────────────────────────────────
# MENÚS DE NAVEGACIÓN
# ─────────────────────────────────────────────

def menu_equipos():
    """Submenú de gestión de equipos."""
    while True:
        limpiar_pantalla()
        separador("Gestión de Equipos")
        print("""
  1. Registrar nuevo equipo
  2. Ver inventario completo
  3. Cambiar estado de equipo
  0. Volver al menú principal
        """)
        opcion = validar_opcion(["1", "2", "3", "0"])

        if opcion == "1":
            registrar_equipo()
        elif opcion == "2":
            listar_equipos()
        elif opcion == "3":
            cambiar_estado_equipo()
        elif opcion == "0":
            break

        pausar()


def menu_campers():
    """Submenú de gestión de campers."""
    while True:
        limpiar_pantalla()
        separador("Gestión de Campers")
        print("""
  1. Registrar nuevo camper
  2. Ver listado de campers
  0. Volver al menú principal
        """)
        opcion = validar_opcion(["1", "2", "0"])

        if opcion == "1":
            registrar_camper()
        elif opcion == "2":
            listar_campers()
        elif opcion == "0":
            break

        pausar()


def menu_sesiones():
    """Submenú de check-in / check-out."""
    while True:
        limpiar_pantalla()
        separador("Control de Sesiones")
        print("""
  1. Check-In (iniciar sesión)
  2. Check-Out (cerrar sesión)
  3. Ver sesiones activas
  0. Volver al menú principal
        """)
        opcion = validar_opcion(["1", "2", "3", "0"])

        if opcion == "1":
            check_in()
        elif opcion == "2":
            check_out()
        elif opcion == "3":
            ver_sesiones_activas()
        elif opcion == "0":
            break

        pausar()


def menu_reportes():
    """Submenú de gestión de reportes."""
    while True:
        limpiar_pantalla()
        separador("Reportes de Incidencias")
        print("""
  1. Crear nuevo reporte
  2. Ver todos los reportes
  3. Actualizar estado de reporte
  0. Volver al menú principal
        """)
        opcion = validar_opcion(["1", "2", "3", "0"])

        if opcion == "1":
            crear_reporte()
        elif opcion == "2":
            listar_reportes()
        elif opcion == "3":
            actualizar_reporte()
        elif opcion == "0":
            break

        pausar()


def menu_principal():
    """Menú raíz de la aplicación."""
    while True:
        limpiar_pantalla()
        print("""
  ╔═══════════════════════════════════════════════════════╗
  ║   SISTEMA DE INVENTARIO — CAJASAN × CAMPUSLANDS       ║
  ╚═══════════════════════════════════════════════════════╝

  1. 📦  Gestión de Equipos
  2. 👤  Gestión de Campers
  3. 🔄  Control de Sesiones (Check-In / Check-Out)
  4. 🔧  Reportes de Incidencias
  5. 📊  Dashboard General
  6. 🗂   Cargar Datos de Demostración
  0. 🚪  Salir
        """)

        opcion = validar_opcion(["1", "2", "3", "4", "5", "6", "0"])

        if opcion == "1":
            menu_equipos()
        elif opcion == "2":
            menu_campers()
        elif opcion == "3":
            menu_sesiones()
        elif opcion == "4":
            menu_reportes()
        elif opcion == "5":
            limpiar_pantalla()
            mostrar_dashboard()
            pausar()
        elif opcion == "6":
            limpiar_pantalla()
            cargar_datos_demo()
            pausar()
        elif opcion == "0":
            limpiar_pantalla()
            print("\n  👋 Cerrando el sistema. ¡Hasta pronto!\n")
            break


# ─────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────

if __name__ == "__main__":
    menu_principal()
