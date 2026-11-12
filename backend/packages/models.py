from django.db import models
from insurance.models import TypePatient

class TypeHemocomponent(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Nombre')
    acronym = models.CharField(max_length=10, verbose_name='Sigla')
    expiration_day = models.IntegerField(default=30, verbose_name='Duracion en dias')
    max_expiration_days = models.IntegerField(default=30, verbose_name='Maxima Duración en dias')
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    typecoagulation = models.CharField(max_length=15, default='CPDA - 1', verbose_name='Sigla')
    temperature_save = models.CharField(max_length=15, default='4 ± 2', verbose_name='Temperatura De Almacenamiento.')
    position = models.PositiveSmallIntegerField(default=1, verbose_name='Posición')
    is_pediatric = models.BooleanField(default=False, verbose_name='Es de uso Pediatrico')
    can_add_bags = models.BooleanField(default=False, verbose_name='Agregar mas bolsas')
    show_in_billing = models.BooleanField(default=True, verbose_name='Mostrar en facturación')
    show_in_fragmentation = models.BooleanField(default=True, verbose_name='Mostrar en fraccionamiento')
    show_in_request_release = models.BooleanField(default=True, verbose_name='Mostrar en Solicitud de Liberacion')
    blocks_release_with_irregular_antibodies = models.BooleanField(
        default=False,
        verbose_name='Bloquear liberación con anticuerpos irregulares positivos'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    def __unicode__(self):
        return "%s" % self.name

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Tipo de Hemocomponente'
        verbose_name_plural = 'Tipos de Hemocomponentes'
        ordering = ['position', 'name']

        permissions = (
            ('index_typehemocomponent', 'Can List TypeHemocomponent'),
        )


class TypeDiscard(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    typehemocomponent = models.ForeignKey(TypeHemocomponent, related_name='typediscards', on_delete=models.PROTECT,
                                          verbose_name='Tipo de Hemocomponente')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    def __unicode__(self):
        return "%s %s" % (self.typehemocomponent.name, self.name)

    def __str__(self):
        return "%s %s" % (self.typehemocomponent.name, self.name)

    class Meta:
        verbose_name = 'Tipo de Descarte para Hemocomponente'
        verbose_name_plural = 'Tipos de Descartes para Hemocomponentes'
        unique_together = ['name', 'typehemocomponent']

        permissions = (
            ('index_typediscard', 'Can List TypeDiscard'),
        )


class Package(models.Model):
    typepatient = models.ForeignKey(TypePatient, on_delete=models.PROTECT, verbose_name='Tipo de Paciente')
    code = models.CharField(max_length=200, verbose_name='Codigo')
    typehemocomponent = models.ForeignKey(TypeHemocomponent, on_delete=models.PROTECT,
                                          verbose_name='Tipo de Hemocomponente')
    description = models.TextField(null=True, blank=True, verbose_name='Descripcion')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Precio Unitario')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    def __unicode__(self):
        return "%s" % self.typehemocomponent.name

    def __str__(self):
        return "%s" % self.typehemocomponent.name

    class Meta:
        verbose_name = 'Paquete'
        verbose_name_plural = 'Paquetes'
        unique_together = ['typehemocomponent', 'typepatient']

        permissions = (
            ('index_package', 'Can List Package'),
        )
