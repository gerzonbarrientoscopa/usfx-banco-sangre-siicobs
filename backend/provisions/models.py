from django.db import models
import datetime

from donors.models import Donor
from users.models import Patient
from users.models import Employee


class Provision(models.Model):
    donor = models.ForeignKey(Donor, related_name='provisions', on_delete=models.PROTECT, verbose_name='Donante')
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, verbose_name='Paciente')
    register_at = models.DateField(default=datetime.date.today, verbose_name='Fecha de registro')
    quantity = models.BigIntegerField(verbose_name='Cantidad')
    description = models.TextField(null=True, blank=True, verbose_name='Descripcion')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Responsable')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    def __unicode__(self):
        return "%s" % self.register_at

    def __str__(self):
        return "%s" % self.register_at

    class Meta:
        verbose_name = 'Disposición'
        verbose_name_plural = 'Disposiciónes'

        permissions = (
            ('index_provision', 'Can List Provision'),
        )