# encoding: utf-8
from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=15, verbose_name=u'Nombre de Lugar')

    def __unicode__(self):
        return "%s" % self.name

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Lugar'
        verbose_name_plural = 'Lugares'
        ordering = ['name']

        permissions = (
            ('index_place', 'Can List Place'),
        )


class SettingPhisical(models.Model):
    place = models.OneToOneField(Place, related_name='settingphysical', on_delete=models.PROTECT, unique=True, verbose_name='Lugar de Donación')
    hematocrit_min = models.IntegerField(verbose_name='Hematocrito Min. Femenino')
    hematocrit_max = models.IntegerField(verbose_name='Hematocrito Max. Femenino')
    hematocrit_min_m = models.IntegerField(verbose_name='Hematocrito Min. Masculino')
    hematocrit_max_m = models.IntegerField(verbose_name='Hematocrito Max. Masculino')
    systolic_min = models.IntegerField(verbose_name='Sistolica Min.')
    systolic_max = models.IntegerField(verbose_name='Sistolica Max.')
    diastolic_min = models.IntegerField(verbose_name='Diastolica Min.')
    diastolic_max = models.IntegerField(verbose_name='Diastolica Max.')
    pulse_min = models.IntegerField(verbose_name='Pulso Min.')
    pulse_max = models.IntegerField(verbose_name='Pulso Max.')
    weight_min = models.IntegerField(verbose_name='Peso Min.')
    hemoglobin_factor = models.FloatField(verbose_name='Factor de Hemoglobina')

    def __unicode__(self):
        return "%s" % self.place

    def __str__(self):
        return "%s" % self.place

    class Meta:
        verbose_name = u'Configuracion Examen Físico'
        verbose_name_plural = 'Configuraciones Examen Fisico'
        ordering = ['place']

        permissions = (
            ('index_settingphisical', 'Can List SettingPhisical'),
        )

TYPE_REASON = (('TE', 'TEMPORAL'), ('PE', 'PERMANENTE'))


class Reason(models.Model):
    type = models.CharField(max_length=2, choices=TYPE_REASON, verbose_name=u'Razón ')
    name = models.CharField(max_length=40, verbose_name='Nombre')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Fecha de Creación')

    def __unicode__(self):
        return "%s %s" % (self.type, self.name)

    def __str__(self):
        return "%s %s" % (self.type, self.name)

    class Meta:
        verbose_name = u'Razón'
        verbose_name_plural = 'Razones'
        ordering = ['created_at', 'name']

        permissions = (
            ('index_reason', 'Can List Reason'),
        )