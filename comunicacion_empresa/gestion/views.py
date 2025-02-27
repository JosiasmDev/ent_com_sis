# gestion/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Proyecto, Tarea, Mensaje, Comentario, Rol
from .forms import ProyectoForm, TareaForm, MensajeForm, ComentarioForm

def inicio(request):
    if request.user.is_authenticated:
        return redirect('lista_proyectos')
    return render(request, 'gestion/inicio.html')

@login_required
def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.creador = request.user
            proyecto.save()
            form.save_m2m()
            return redirect('lista_proyectos')
    else:
        form = ProyectoForm()
    return render(request, 'gestion/crear_proyecto.html', {'form': form})

@login_required
def lista_proyectos(request):
    proyectos = Proyecto.objects.filter(usuarios=request.user)
    return render(request, 'gestion/lista_proyectos.html', {'proyectos': proyectos})

@login_required
def vista_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    rol = Rol.objects.filter(usuario=request.user, proyecto=proyecto).first()
    if not rol or rol.rol != 'administrador':
        return render(request, 'gestion/sin_permiso.html')
    
    tareas = proyecto.tareas.all()
    estado = request.GET.get('estado', '')
    usuario_id = request.GET.get('usuario', '')
    
    if estado:
        tareas = tareas.filter(estado=estado)
    if usuario_id:
        tareas = tareas.filter(asignados__id=usuario_id)
    
    tareas = tareas.order_by('fecha_limite')
    return render(request, 'gestion/proyecto.html', {
        'proyecto': proyecto,
        'tareas': tareas,
        'usuarios': proyecto.usuarios.all()
    })

@login_required
def crear_tarea(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.proyecto = proyecto
            tarea.save()
            form.save_m2m()
            return redirect('vista_proyecto', proyecto_id=proyecto.id)
    else:
        form = TareaForm()
    return render(request, 'gestion/crear_tarea.html', {'form': form, 'proyecto': proyecto})

@login_required
def enviar_mensaje(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.proyecto = proyecto
            mensaje.remitente = request.user
            mensaje.save()
            form.save_m2m()
            return redirect('vista_proyecto', proyecto_id=proyecto.id)
    else:
        form = MensajeForm()
    return render(request, 'gestion/enviar_mensaje.html', {'form': form, 'proyecto': proyecto})

@login_required
def agregar_comentario(request, tarea_id):
    tarea = get_object_or_404( Tarea, id=tarea_id)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.tarea = tarea
            comentario.autor = request.user
            comentario.save()
            return redirect('vista_proyecto', proyecto_id=tarea.proyecto.id)
    else:
        form = ComentarioForm()
    return render(request, 'gestion/agregar_comentario.html', {'form': form, 'tarea': tarea})