from django.db import models


class TypePatient(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Nombre')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    def __unicode__(self):
        return "%s" % self.name

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Tipo de Paciente'
        verbose_name_plural = 'Tipos de Pacientes'

        permissions = (
            ('index_typepatient', 'Can List typePatient'),
        )
