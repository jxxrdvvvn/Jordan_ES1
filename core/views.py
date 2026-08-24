import json
import os
from django.shortcuts import render, redirect

DATA_FILE = "datos.json"

def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                pass
    return {"inventario": [], "solicitudes": []}

def guardar_datos(datos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

def panel_control(request):
    datos = cargar_datos()
    tab = request.GET.get('tab', 'general')

    if request.method == "POST":
        # 1. Procesar Ingreso de Stock
        if "ingresar_stock" in request.POST:
            prod_nombre = request.POST.get("producto", "").strip()
            cant_ingreso = int(request.POST.get("cantidad", 0))

            if prod_nombre and cant_ingreso > 0:
                encontrado = False
                for p in datos["inventario"]:
                    if p["producto"].lower() == prod_nombre.lower():
                        p["stock"] += cant_ingreso
                        encontrado = True
                        break
                if not encontrado:
                    datos["inventario"].append({"producto": prod_nombre, "stock": cant_ingreso})
                
                guardar_datos(datos)
                return redirect('/?tab=general')

        # 2. Procesar Solicitud de Salida de Stock (Nueva Funcionalidad)
        elif "solicitar_salida" in request.POST:
            prod_nombre = request.POST.get("producto_salida", "").strip()
            cant_salida = int(request.POST.get("cantidad_salida", 0))

            if prod_nombre and cant_salida > 0:
                # Generar ID autoincremental
                nuevo_id = max([s.get("id", 0) for s in datos["solicitudes"]], default=0) + 1
                
                nueva_solicitud = {
                    "id": nuevo_id,
                    "producto": prod_nombre,
                    "cantidad": cant_salida,
                    "estado": "pendiente",
                    "motivo": "Pendiente de revisión por el encargado."
                }
                
                datos["solicitudes"].append(nueva_solicitud)
                guardar_datos(datos)
                return redirect('/?tab=general')

    # Filtrar solicitudes según la pestaña activa
    if tab == 'aceptados':
        solicitudes_filtradas = [s for s in datos["solicitudes"] if s["estado"] == "Aceptado"]
    elif tab == 'rechazados':
        solicitudes_filtradas = [s for s in datos["solicitudes"] if s["estado"] == "Rechazado"]
    else:
        solicitudes_filtradas = [s for s in datos["solicitudes"] if s["estado"] == "pendiente"]

    context = {
        "tab": tab,
        "inventario": datos["inventario"],
        "solicitudes": solicitudes_filtradas,
        "total_pendientes": len([s for s in datos["solicitudes"] if s["estado"] == "pendiente"])
    }
    return render(request, "resumen.html", context)

def responder_solicitud(request, solicitud_id, accion):
    datos = cargar_datos()
    for s in datos["solicitudes"]:
        if s["id"] == solicitud_id and s["estado"] == "pendiente":
            prod_inv = next((p for p in datos["inventario"] if p["producto"].lower() == s["producto"].lower()), None)
            stock_actual = prod_inv["stock"] if prod_inv else 0

            if accion == "aceptar":
                if s["cantidad"] <= 0:
                    s["estado"] = "Inválido"
                    s["motivo"] = "Dato Inválido: La cantidad solicitada debe ser mayor a 0."
                elif s["cantidad"] > 50:
                    s["estado"] = "Rechazado"
                    s["motivo"] = "Rechazado: La cantidad supera el límite máximo permitido por pedido (50 unidades)."
                elif s["cantidad"] > stock_actual:
                    s["estado"] = "Rechazado"
                    s["motivo"] = f"Rechazado: Stock insuficiente. Quedan {stock_actual} unidades en bodega."
                else:
                    s["estado"] = "Aceptado"
                    s["motivo"] = f"Aprobado por el encargado. Se despacharon {s['cantidad']} unidad(es)."
                    prod_inv["stock"] -= s["cantidad"]
            
            elif accion == "rechazar":
                s["estado"] = "Rechazado"
                s["motivo"] = "Rechazado manualmente por el encargado."

            break
            
    guardar_datos(datos)
    return redirect('/?tab=general')