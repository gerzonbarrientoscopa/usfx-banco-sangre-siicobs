import datetime

from django.db import models

from extractions.models import Extraction
from users.models import Employee

class Menu(models.Model):
    name = models.CharField(max_length=100, default='', verbose_name='Nombre')
    register_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    only_volunteer = models.BooleanField(default=False, verbose_name='Es Para Voluntario')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menu'
        ordering = ['name']

        permissions = (
            ('index_menu', 'Can List Menu'),
        )


class ExtractionRefreshment(models.Model):
    extraction = models.OneToOneField(Extraction, unique=True, related_name='extractionrefreshment',
                                      on_delete=models.PROTECT, verbose_name=u'Extracción')
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT, verbose_name='Menu de Refrigerio')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Responsable')
    register_at = models.DateField(default=datetime.date.today, verbose_name='Fecha de registro')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Fecha de Creación')

    def __unicode__(self):
        return "%s %s" % (self.extraction, self.menu)

    def __str__(self):
        return "%s %s" % (self.extraction, self.menu)

    class Meta:
        verbose_name = 'Refrigerio'
        verbose_name_plural = 'Refrigerios'
        ordering = ['created_at', 'extraction']
        unique_together = ['extraction', 'menu']

        permissions = (
            ('index_extractionrefreshment', 'Can List ExtractionRefreshment'),
        )
