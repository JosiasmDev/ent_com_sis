# ent_com_sis

## Sistema de Comunicación Empresarial

Este proyecto es una aplicación web desarrollada con Django que permite la gestión de proyectos, tareas, grupos, usuarios y mensajes dentro de una empresa. Incluye un sistema de notificaciones en tiempo real para mantener a los usuarios informados sobre eventos relevantes, como la creación de proyectos, modificaciones de tareas y mensajes enviados.

## Descripción general

La aplicación facilita la colaboración entre empleados mediante la creación de proyectos, la asignación de tareas, la gestión de grupos y la comunicación a través de mensajes privados y mensajes asociados a proyectos. Los usuarios reciben notificaciones automáticas sobre acciones que les afectan, como asignaciones, modificaciones o eliminaciones.

## Requisitos previos

- **Python**: Versión 3.13.1 (o superior compatible con Django 5.1.6).
- **PostgreSQL**: Base de datos utilizada para almacenar los datos de la aplicación.
- **Entorno virtual**: Recomendado para gestionar dependencias (por ejemplo, venv).
- **Sistema operativo**: Probado en Windows (compatible con Linux/Mac con ajustes menores).

## Instalación

Sigue estos pasos para instalar y configurar el proyecto en tu máquina local:

### 1. Clonar el repositorio

```bash
git clone https://github.com/JosiasmDev/ent_com_sis.git
cd comunicacion_empresa
```

### 2. Crear y activar un entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
./venv/Scripts/activate   # En Windows
```

### 3. Instalar las dependencias

Asegúrate de tener el archivo `requirements.txt` generado previamente y luego instala las dependencias:

```bash
pip install -r requirements.txt
```

#### Dependencias principales:

- `Django==5.1.6`: Framework web.
- `django-notifications-hq==1.7.0`: Sistema de notificaciones.
- `psycopg2-binary==2.9.9`: Adaptador de PostgreSQL.

### 4. Configurar la base de datos

1. Instala PostgreSQL y crea una base de datos llamada `comunicacion_empresa`.
2. Edita `comunicacion_empresa/settings.py` con tus credenciales de PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'comunicacion_empresa',
        'USER': 'postgres',  # Cambia según tu usuario
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear un superusuario

```bash
python manage.py createsuperuser
```

## Ejecución

### Iniciar el servidor

```bash
python manage.py runserver
```

### Acceder a la aplicación

- Abre tu navegador en [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
- Inicia sesión con el superusuario o regístrate en `/proyectos/registro/`.

### Rutas principales

- `/proyectos/`: Lista de proyectos.
- `/proyectos/<id>/`: Vista detallada de un proyecto.
- `/proyectos/notificaciones/`: Lista de notificaciones.
- `/login/`: Inicio de sesión.
- `/proyectos/registro/`: Registro de nuevos usuarios.

## Arquitectura del proyecto

### Estructura de directorios

```
comunicacion_empresa/
├── comunicacion_empresa/   # Configuración principal
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── gestion/                # Aplicación principal
│   ├── __init__.py
│   ├── admin.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── migrations/
│   ├── models.py
│   ├── templatetags/
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       ├── gestion/
│       └── registration/
├── static/                 # Archivos estáticos (CSS, JS)
├── templates/              # Plantillas base
├── manage.py
└── requirements.txt
```

### Modelos principales

- **Proyecto**: Representa un proyecto con título, descripción, fechas y usuarios asignados.
- **Tarea**: Tareas asociadas a un proyecto con estado, asignados y comentarios.
- **Mensaje**: Mensajes privados entre usuarios.
- **MensajeProyecto**: Mensajes asociados a un proyecto.
- **Grupo**: Grupos de usuarios dentro de un proyecto.
- **Rol**: Roles de usuarios en proyectos (administrador, miembro, invitado).
- **Comentario**: Comentarios en tareas.

### Vistas principales

- **CRUD de proyectos**: Crear, leer, actualizar y eliminar proyectos.
- **Gestión de tareas**: Crear, editar y eliminar tareas.
- **Mensajería**: Enviar mensajes privados y al proyecto.
- **Notificaciones**: Mostrar y marcar notificaciones como leídas.
- **Grupos y usuarios**: Gestionar grupos y asignaciones.

## Dependencias externas

- **Django**: Framework principal para manejar vistas, modelos y URLs.
- **django-notifications-hq**: Sistema de notificaciones en tiempo real.
- **Bootstrap 5**: Framework CSS para la interfaz.
- **Font Awesome**: Iconos para mejorar la UI.

## Decisiones de diseño

### Arquitectura monolítica
- **Razón**: Facilidad de desarrollo y mantenimiento.
- **Impacto**: Simplifica la implementación inicial, aunque podría complicar la escalabilidad futura.

### Base de datos PostgreSQL
- **Razón**: Soporte robusto para relaciones ManyToMany y transacciones.
- **Impacto**: Mayor rendimiento y fiabilidad en comparación con SQLite.

### Sistema de notificaciones
- **Razón**: Uso de `django-notifications-hq` para enviar notificaciones automáticas.
- **Impacto**: Mejora la comunicación en tiempo real.

### Diseño oscuro
- **Razón**: Estética profesional y reducción de fatiga visual.
- **Impacto**: Consistencia visual con alto contraste para legibilidad.

## Problemas conocidos y soluciones

- **Notificaciones duplicadas**: Resuelto asegurando una sola llamada a `notify.send()`.
- **Asignación de usuarios al crear proyectos**: Corregido procesando `form.cleaned_data['usuarios']` explícitamente.
- **Widgets de fecha**: Restaurados con `DateInput` en `ProyectoForm`.

## Contribución

1. Clona el repositorio y crea una rama:

   ```bash
   git checkout -b nueva-funcionalidad
   ```

2. Realiza cambios y haz un commit:

   ```bash
   git add .
   git commit -m "Descripción de los cambios"
   ```

3. Envía un pull request al repositorio principal.

## Licencia

Este proyecto no tiene una licencia explícita definida. Se considera de uso privado a menos que se especifique lo contrario.

