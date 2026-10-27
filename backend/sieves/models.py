# encoding:utf-8
from django.db import models
from django.db.models import JSONField
from donations.models import Donation
from users.models import Employee
import datetime

OPTIONS = (('S', 'SIMPLE'), ('T', 'TEXTO'))
STATUS = (('A', 'ACTIVO'), ('I', 'INACTIVO'))


class ClinicalHistoryQuestion(models.Model):
    title = models.CharField(max_length=1000, default='', verbose_name=u'Título')
    questions = JSONField(default=dict, verbose_name='Preguntas')
    is_active = models.BooleanField(default=False, verbose_name='Esta activo')
    register_at = models.DateField(default=datetime.date.today, verbose_name='Fecha de Registro')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')

    def __unicode__(self):
        return "%s" % self.title

    def __str__(self):
        return "%s" % self.title

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = ['title']

        permissions = (
            ('index_clinicalhistoryquestion', 'Can list clinicalhistoryquestion'),
        )


class ClinicalHistoryAnswer(models.Model):
    questionnaire = models.ForeignKey(ClinicalHistoryQuestion, on_delete=models.PROTECT, verbose_name='Cuestionario')
    donation = models.OneToOneField(Donation, unique=True, on_delete=models.PROTECT,
                                    related_name='clinicalhistoryanswer', verbose_name='Donación')
    responses = JSONField(default=dict, verbose_name='Respuestas')
    observations = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Empleado')
    register = models.ForeignKey(Employee, default=1, related_name='%(class)s_register', on_delete=models.PROTECT,
                                 verbose_name='Registrador')
    register_at = models.DateField(default=datetime.date.today, verbose_name='Fecha de Registro')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')

    def __unicode__(self):
        return "%s" % self.donation

    def __str__(self):
        return "%s" % self.donation

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
        ordering = ['register_at']

        permissions = (
            ('index_clinicalhistoryanswer', 'Can list clinicalhistoryanswer'),
        )
