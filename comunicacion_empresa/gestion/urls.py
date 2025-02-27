# gestion/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('proyectos/', views.lista_proyectos, name='lista_proyectos'),
    path('proyectos/crear/', views.crear_proyecto, name='crear_proyecto'),
    path('proyectos/<int:proyecto_id>/', views.vista_proyecto, name='vista_proyecto'),
    path('proyectos/<int:proyecto_id>/tareas/crear/', views.crear_tarea, name='crear_tarea'),
    path('proyectos/<int:proyecto_id>/mensajes/enviar/', views.enviar_mensaje, name='enviar_mensaje'),
    path('tareas/<int:tarea_id>/comentarios/agregar/', views.agregar_comentario, name='agregar_comentario'),
]