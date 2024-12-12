from django.urls import path
from django.contrib import admin
from .import views

urlpatterns = [
    path('', views.index,name="urls_index"),
    path('promociones/listar_promociones', views.listar_promociones,name="listar_promociones"),
    path('promociones/create', views.procesar_promocion,name="procesar_promocion"),
    path('promociones/buscar',views.buscar_promocion,name="buscar_promocion"),
    path('promociones/editar/<int:promocion_id>', views.editar_promocion,name="editar_promocion"),
    path('promociones/eliminar/<int:promocion_id>',views.eliminar_promocion,name='eliminar_promocion'),
]       