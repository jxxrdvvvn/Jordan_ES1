from django.contrib import admin
from django.urls import path
from core.views import panel_control, responder_solicitud

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', panel_control, name='panel'),
    path('responder/<int:solicitud_id>/<str:accion>/', responder_solicitud, name='responder_solicitud'),
]