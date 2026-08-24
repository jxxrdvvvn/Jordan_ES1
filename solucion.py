import json
import os
from tabulate import tabulate


def evaluar_despacho(producto, stock, cantidad):
    """Regla de decisión con los 4 resultados requeridos por la pauta."""
    # 1. Dato Inválido (Revisar siempre al inicio)
    if stock <= 0 or cantidad <= 0:
        return "Inválido", "Error: El stock y la cantidad deben ser mayores a 0."
    
    # 2. Aceptado
    elif cantidad <= stock and cantidad <= 50:
        return "Aceptado", f"Despacho aprobado para {cantidad} unidad(es) de {producto}."
    
    # 3. Rechazado por límite máximo por pedido
    elif cantidad > 50:
        return "Rechazado", "La cantidad supera el límite máximo permitido por pedido (50 unidades)."
    
    # 4. Rechazado por stock insuficiente
    else:
        return "Rechazado", f"Stock insuficiente. Quedan {stock} unidades en bodega."


def main():
    print("=== SISTEMA DE CONTROL DE DESPACHOS ===")
    producto = input("Nombre del producto: ")
    
    try:
        stock = int(input("Stock disponible: "))
        cantidad = int(input("Cantidad solicitada: "))
    except ValueError:
        print("Error: Ingresa números enteros para stock y cantidad.")
        return

    # Evaluar la regla
    estado, motivo = evaluar_despacho(producto, stock, cantidad)
    print(f"\nResultado: {estado} - {motivo}\n")

    # Estructura del registro
    nuevo = {
        "producto": producto,
        "stock": stock,
        "cantidad": cantidad,
        "estado": estado,
        "motivo": motivo
    }

    # Leer JSON existente si hay uno
    registros = []
    if os.path.exists("datos.json"):
        with open("datos.json", "r", encoding="utf-8") as f:
            try:
                registros = json.load(f)
            except json.JSONDecodeError:
                registros = []

    # Guardar nuevo registro en el JSON
    registros.append(nuevo)
    with open("datos.json", "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=2, ensure_ascii=False)

    # Mostrar la tabla formateada con tabulate en la terminal
    print("=== HISTORIAL REGISTRADO EN JSON ===")
    print(tabulate(registros, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    main()