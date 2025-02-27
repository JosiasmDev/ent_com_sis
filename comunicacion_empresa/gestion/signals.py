# gestion/signals.py
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from notifications.signals import notify
from .models import Tarea, Mensaje

@receiver(m2m_changed, sender=Tarea.asignados.through)
def notificar_asignacion_tarea(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':  # Cuando se añaden usuarios a la tarea
        for user_id in pk_set:
            usuario = instance.asignados.get(id=user_id)
            notify.send(
                instance.proyecto.creador,  # Remitente
                recipient=usuario,          # Destinatario
                verb='te asignó la tarea',
                target=instance
            )

@receiver(m2m_changed, sender=Mensaje.destinatarios.through)
def notificar_mensaje(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':  # Cuando se añaden destinatarios al mensaje
        for user_id in pk_set:
            usuario = instance.destinatarios.get(id=user_id)
            notify.send(
                instance.remitente,         # Remitente
                recipient=usuario,          # Destinatario
                verb='te envió un mensaje',
                target=instance
            )