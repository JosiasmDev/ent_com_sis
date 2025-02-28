# gestion/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_proyectos, name='lista_proyectos'),
    path('crear/', views.crear_proyecto, name='crear_proyecto'),
    path('<int:proyecto_id>/', views.vista_proyecto, name='vista_proyecto'),
    path('<int:proyecto_id>/editar/', views.editar_proyecto, name='editar_proyecto'),
    path('<int:proyecto_id>/tareas/crear/', views.crear_tarea, name='crear_tarea'),
    path('<int:proyecto_id>/mensajes/enviar/', views.enviar_mensaje, name='enviar_mensaje'),
    path('tareas/<int:tarea_id>/comentarios/agregar/', views.agregar_comentario, name='agregar_comentario'),
    path('mensaje/nuevo/', views.enviar_mensaje_privado, name='enviar_mensaje_privado'),
    path('mensaje/<int:mensaje_id>/eliminar/', views.eliminar_mensaje, name='eliminar_mensaje'),
    path('chat/<int:usuario_id>/borrar/', views.borrar_chat, name='borrar_chat'),
    path('grupos/', views.lista_grupos, name='lista_grupos'),
    path('grupos/<int:grupo_id>/', views.gestionar_grupo, name='gestionar_grupo'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('<int:proyecto_id>/mensajes/enviar/', views.enviar_mensaje_proyecto, name='enviar_mensaje_proyecto'),
    path('mensajes/proyecto/<int:mensaje_id>/eliminar/', views.eliminar_mensaje_proyecto, name='eliminar_mensaje_proyecto'),
    path('tareas/<int:tarea_id>/editar/', views.editar_tarea, name='editar_tarea'),
    path('tareas/<int:tarea_id>/eliminar/', views.eliminar_tarea, name='eliminar_tarea'),
    path('comentarios/<int:comentario_id>/editar/', views.editar_comentario, name='editar_comentario'),
    path('comentarios/<int:comentario_id>/eliminar/', views.eliminar_comentario, name='eliminar_comentario'),
    path('mensaje/<int:mensaje_id>/editar/', views.editar_mensaje, name='editar_mensaje'),
]