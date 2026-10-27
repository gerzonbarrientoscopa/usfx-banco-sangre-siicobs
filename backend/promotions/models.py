from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    init_at = models.DateTimeField(verbose_name='Fecha y Hora de Inicio')
    end_at = models.DateTimeField(verbose_name='Fecha y Hora de Finalizacíon')
    is_active = models.BooleanField(default=True, verbose_name='Esta Activo')
    register_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    def __unicode__(self):
        return "%s" % self.name

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        unique_together = ('name', 'init_at', 'end_at')

        permissions = (
            ('index_event', 'Can List Event'),
        )
