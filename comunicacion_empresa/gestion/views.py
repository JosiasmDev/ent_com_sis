from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from .models import Proyecto, Tarea, Mensaje, Comentario, Rol, Grupo
from .forms import ProyectoForm, TareaForm, MensajeForm, ComentarioForm, RegistroForm

def inicio(request):
    if request.user.is_authenticated:
        return redirect('lista_proyectos')
    return redirect('login')

@login_required
def lista_proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'gestion/lista_proyectos.html', {'proyectos': proyectos})

@login_required
def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.creador = request.user
            proyecto.save()
            proyecto.usuarios.add(request.user)
            form.save_m2m()
            Rol.objects.create(usuario=request.user, proyecto=proyecto, rol='administrador')
            print("Proyecto guardado:", proyecto.titulo)
            return redirect('lista_proyectos')
        else:
            print("Errores del formulario:", form.errors)
    else:
        form = ProyectoForm()
    return render(request, 'gestion/crear_proyecto.html', {'form': form})

@login_required
def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('lista_proyectos')
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, 'gestion/editar_proyecto.html', {'form': form, 'proyecto': proyecto})

@login_required
def vista_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    rol = Rol.objects.filter(usuario=request.user, proyecto=proyecto).first()
    if request.user not in proyecto.usuarios.all() and (not rol or rol.rol != 'administrador'):
        return render(request, 'gestion/sin_permiso.html')
    
    tareas = proyecto.tareas.all()
    mensajes = proyecto.mensajes.all()
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
        'mensajes': mensajes,
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
    tarea = get_object_or_404(Tarea, id=tarea_id)
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

@login_required
def enviar_mensaje_privado(request):
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.remitente = request.user
            mensaje.save()
            return redirect(request.META.get('HTTP_REFERER', 'lista_proyectos'))
    else:
        form = MensajeForm()
    return render(request, 'gestion/enviar_mensaje_privado.html', {'form': form})

@login_required
def lista_grupos(request):
    grupos = Grupo.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        proyecto_id = request.POST.get('proyecto')
        if nombre and proyecto_id:
            grupo = Grupo.objects.create(nombre=nombre, proyecto_id=proyecto_id)
            return redirect('lista_grupos')
    return render(request, 'gestion/lista_grupos.html', {'grupos': grupos, 'proyectos': Proyecto.objects.all()})

@login_required
def gestionar_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'agregar':
            usuario_id = request.POST.get('usuario')
            rol = request.POST.get('rol')
            if usuario_id and rol:
                usuario = User.objects.get(id=usuario_id)
                grupo.miembros.add(usuario)
                Rol.objects.create(usuario=usuario, proyecto=grupo.proyecto, rol=rol)
        elif accion == 'quitar':
            usuario_id = request.POST.get('usuario')
            if usuario_id:
                usuario = User.objects.get(id=usuario_id)
                grupo.miembros.remove(usuario)
                Rol.objects.filter(usuario=usuario, proyecto=grupo.proyecto).delete()
        elif accion == 'cambiar_rol':
            usuario_id = request.POST.get('usuario')
            rol = request.POST.get('rol')
            if usuario_id and rol:
                usuario = User.objects.get(id=usuario_id)
                Rol.objects.update_or_create(usuario=usuario, proyecto=grupo.proyecto, defaults={'rol': rol})
        elif accion == 'eliminar':
            grupo.delete()
            return redirect('lista_grupos')
        elif accion == 'editar':
            nombre = request.POST.get('nombre')
            if nombre:
                grupo.nombre = nombre
                grupo.save()

    # Preprocesar los roles de los miembros
    miembros_con_roles = []
    for miembro in grupo.miembros.all():
        try:
            rol = Rol.objects.get(usuario=miembro, proyecto=grupo.proyecto)
            miembros_con_roles.append({'miembro': miembro, 'rol': rol.rol})
        except Rol.DoesNotExist:
            miembros_con_roles.append({'miembro': miembro, 'rol': 'Sin rol'})

    return render(request, 'gestion/gestionar_grupo.html', {
        'grupo': grupo,
        'usuarios': User.objects.all(),
        'miembros_con_roles': miembros_con_roles
    })

@login_required
def lista_usuarios(request):
    usuarios = User.objects.all()
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario')
        grupo_id = request.POST.get('grupo')
        rol = request.POST.get('rol')
        accion = request.POST.get('accion')
        if accion == 'agregar' and usuario_id and grupo_id and rol:
            usuario = User.objects.get(id=usuario_id)
            grupo = Grupo.objects.get(id=grupo_id)
            grupo.miembros.add(usuario)
            Rol.objects.create(usuario=usuario, proyecto=grupo.proyecto, rol=rol)
    return render(request, 'gestion/lista_usuarios.html', {'usuarios': usuarios, 'grupos': Grupo.objects.all()})

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'gestion/registro.html', {'form': form})

@login_required
def eliminar_mensaje(request, mensaje_id):
    mensaje = get_object_or_404(Mensaje, id=mensaje_id, remitente=request.user)
    if request.method == 'POST':
        mensaje.delete()
        return redirect(request.META.get('HTTP_REFERER', 'lista_proyectos'))
    return render(request, 'gestion/confirmar_eliminar.html', {'objeto': mensaje, 'tipo': 'mensaje'})

@login_required
def borrar_chat(request, usuario_id):
    if request.method == 'POST':
        Mensaje.objects.filter(
            (models.Q(remitente=request.user) & models.Q(destinatario_id=usuario_id)) |
            (models.Q(destinatario=request.user) & models.Q(remitente_id=usuario_id))
        ).delete()
        return redirect('lista_proyectos')
    return render(request, 'gestion/confirmar_eliminar.html', {'objeto': User.objects.get(id=usuario_id), 'tipo': 'chat'})


@login_required
def enviar_mensaje_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            MensajeProyecto.objects.create(proyecto=proyecto, remitente=request.user, contenido=contenido)
        return redirect('vista_proyecto', proyecto_id=proyecto.id)
    return render(request, 'gestion/enviar_mensaje_proyecto.html', {'proyecto': proyecto})

@login_required
def eliminar_mensaje_proyecto(request, mensaje_id):
    mensaje = get_object_or_404(MensajeProyecto, id=mensaje_id, remitente=request.user)
    if request.method == 'POST':
        mensaje.delete()
        return redirect('vista_proyecto', proyecto_id=mensaje.proyecto.id)
    return render(request, 'gestion/confirmar_eliminar.html', {'objeto': mensaje, 'tipo': 'mensaje_proyecto'})