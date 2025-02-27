from django.http import HttpResponse
from django.shortcuts import render

def crear_proyecto(request):
    # Lógica para crear el proyecto
    return render(request, 'crear_proyecto.html')


def lista_proyectos(request):
    return HttpResponse("Lista de proyectos")
