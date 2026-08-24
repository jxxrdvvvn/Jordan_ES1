# Plan de Proyecto: Panel Interactivo de Inventario y Validación de Despachos

---

## 1. APARTADO DE NEGOCIO

### Problema
En las bodegas de almacenes locales, la falta de visibilidad del inventario en tiempo real y la aprobación automática o descontrolada de salidas provoca errores de despacho, quiebres de stock no deseados y despachos por encima de los límites permitidos.

### Solución
Desarrollar un panel web interactivo que combine la gestión de existencias (entradas) con una bandeja de notificaciones para que el encargado de bodega revise, apruebe o rechace manualmente las solicitudes de salida de mercadería en tiempo real.

### Alcance
* **Dentro del alcance:** Formulario web de ingreso de stock, formulario web de solicitud de salida, bandeja de notificaciones pendientes con botones de acción (Aceptar/Rechazar), descuento de stock dinámico en `datos.json` y menú navegable de 3 pestañas.
* **Fuera del alcance:** Conexión a bases de datos relacionales (SQL), inicio de sesión con contraseña (autenticación) o pasarelas de pago.

### Priorización MoSCoW (MVP / PoC)
* **Must (Imprescindibles - MVP):**
  - Formulario de entrada para cargar/incrementar stock.
  - Formulario de solicitud de salida de stock.
  - Bandeja de notificaciones para solicitudes en estado `pendiente`.
  - Botones interactivos para que el usuario determine si aprueba o rechaza la salida.
  - Validación de regla de negocio (máximo 50 unidades y disponibilidad en bodega).
  - Navegación por 3 pestañas: General, Aceptados y Rechazados.
  - Persistencia total en `datos.json` sin base de datos SQL.
* **Should (Debería incluirse a futuro):**
  - Opción para editar el nombre o borrar productos del inventario general.
* **Could (Podría incluirse a futuro):**
  - Exportar el reporte por pestañas a formato PDF o Excel.
* **Won't (No se incluirá en esta entrega):**
  - Autenticación de usuarios por roles (Bodeguero vs Administrador).

---

## 2. APARTADO TÉCNICO

### Requisitos de Datos
* `inventario`: Lista de objetos `{"producto": string, "stock": integer}`.
* `solicitudes`: Lista de objetos `{"id": int, "producto": string, "cantidad": int, "estado": string, "motivo": string}`.

### Reglas de Negocio en Aprobación
Al hacer clic en **Aceptar Salida**:
1. Si `cantidad <= 0` $\rightarrow$ **Inválido**.
2. Si `cantidad > 50` $\rightarrow$ **Rechazado** (supera el límite por pedido).
3. Si `cantidad > stock` $\rightarrow$ **Rechazado** (stock insuficiente en inventario).
4. Si cumple condiciones $\rightarrow$ **Aceptado** y se resta `cantidad` del `stock` correspondiente.