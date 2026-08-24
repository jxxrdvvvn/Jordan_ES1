# Declaración sobre el uso de Inteligencia Artificial (ia.md)

---

## 1. Herramienta utilizada y propósito
Se utilizó la herramienta **Gemini** como asistente técnico para la arquitectura del proyecto en Django, el diseño de la interfaz gráfica web en HTML/CSS con temática futurista (Dark Mode & Neón) y la implementación de la lógica interactiva para el manejo de inventario y despachos.

---

## 2. Consulta concreta realizada (Prompt)
> "Necesito transformar la aplicación de validación automática en un panel de control interactivo en Django. Debe permitir ingresar stock, solicitar salidas de stock, mostrar una notificación de solicitudes pendientes para que el encargado pueda aprobar o rechazar manualmente con un clic, y filtrar los registros en 3 pestañas (Stock General, Stock Aceptado y Stock Rechazado), guardando todo en el archivo datos.json."

---

## 3. Corrección y validación propia realizada

* **Propuesta inicial de la IA:**
  La herramienta sugirió utilizar AJAX/JavaScript dinámico junto con el uso de modelos relacionales de Django (`models.py`) y migraciones para manejar las notificaciones y botones de aprobación en tiempo real.

* **Corrección aplicada por el estudiante:**
  Ajusté la solución para mantener la restricción fundamental de la pauta de evaluación: **no utilizar bases de datos ni modelos ORM**. Reestructuré el código en `core/views.py` para procesar el estado mediante peticiones HTTP estándar (`POST` y `GET`), guardando y actualizando las estructuras del inventario y las solicitudes directamente en el archivo `datos.json`.