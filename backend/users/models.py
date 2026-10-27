# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.db import models

DEPARTMENTS = (
    ('LP', 'LA PAZ'), ('OR', 'ORURO'), ('PO', u'POTOSÍ'), ('CO', 'COCHABAMBA'), ('CH', 'CHUQUISACA'),
    ('TA', 'TARIJA'), ('PA', 'PANDO'), ('BE', 'BENI'), ('SC', 'SANTA CRUZ'), ('', ''))

GENDER = (('F', 'FEMENINO'), ('M', 'MASCULINO'))
TYPE_INSTITUTION = (('PU', 'PUBLICO'), ('PR', u'PRIVADO'), ('SS', 'SEGURIDAD SOCIAL'),)


class Institution(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    nit = models.CharField(max_length=25, blank=True, null=True, verbose_name='NIT')
    logo = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name='Logo')
    address = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Dirección')
    phone = models.IntegerField(blank=True, null=True, verbose_name=u'teléfono')
    type = models.CharField(default='PU', max_length=2, choices=TYPE_INSTITUTION, verbose_name='Tipo')
    department = models.CharField(max_length=2, default='PO', choices=DEPARTMENTS, verbose_name='Departamento')
    register_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    def __unicode__(self):
        return "%s" % self.name

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Institución'
        verbose_name_plural = 'Instituciones'
        unique_together = ('name', 'department')

        permissions = (
            ('index_institution', 'Can List Institution'),
        )


class Employee(models.Model):
    institution = models.ForeignKey(Institution, blank=True, null=True, verbose_name='Institución',
                                    on_delete=models.PROTECT)
    user = models.OneToOneField(User, unique=True, blank=True, null=True, on_delete=models.CASCADE)
    ci = models.BigIntegerField(unique=True, verbose_name='CI')
    first_name = models.CharField(max_length=100, default='', verbose_name='Nombres')
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Apellido Paterno')
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Apellido Materno')
    gender = models.CharField(max_length=2, choices=GENDER, verbose_name=u'Género')
    home_address = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Dirección')
    mobile_phone = models.BigIntegerField(blank=True, null=True, verbose_name='Nro. de Celular')
    register_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    code_licence = models.CharField(max_length=25, blank=True, null=True, verbose_name='Nro. Matrícula')

    def __unicode__(self):
        return "%s %s %s" % (self.middle_name, self.last_name, self.first_name)

    def __str__(self):
        return "%s %s %s" % (self.middle_name, self.last_name, self.first_name)

    def as_json(self):
        return dict(
            id=self.id,
            ci=self.ci,
            first_name=self.first_name,
            middle_name=self.middle_name,
            last_name=self.last_name,
            register_at=self.register_at.isoformat(),
            code_licence=self.code_licence,
            gender=self.gender,
            home_address=self.home_address,
            mobile_phone=self.mobile_phone
        )

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['first_name', 'middle_name', 'last_name']

        permissions = (
            ('index_employee', 'Can List Employee'),
        )


class Medical(models.Model):
    institution = models.ForeignKey(Institution, verbose_name='Institución', on_delete=models.PROTECT)
    first_name = models.CharField(max_length=100, default='', verbose_name='Nombres')
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Apellido Paterno')
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Apellido Materno')
    register_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    def __unicode__(self):
        return "%s %s %s" % (self.middle_name, self.last_name, self.first_name)

    def __str__(self):
        return "%s %s %s" % (self.middle_name, self.last_name, self.first_name)

    class Meta:
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'
        ordering = ['middle_name', 'last_name', 'first_name']

        permissions = (
            ('index_medical', 'Can List Medical'),
        )


class Patient(models.Model):
    institution = models.ForeignKey(Institution, blank=True, null=True, on_delete=models.PROTECT,
                                    verbose_name='Institución')
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nombres')
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Apellido Paterno')
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Apellido Materno')
    phone = models.IntegerField(blank=True, null=True, verbose_name=u'Teléfono')
    ci = models.CharField(max_length=20, unique=True, null=True, verbose_name='Doc. de Ident./DNI')
    is_real_birthdate = models.BooleanField(default=True, verbose_name='Es fecha de nacimiento real ?')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Fecha Nacimiento')
    gender = models.CharField(max_length=2, choices=GENDER, verbose_name=u'Género')
    register_at = models.DateField(default=datetime.date.today, verbose_name='Fecha de registro')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    def __unicode__(self):
        return "%s %s %s" % (self.middle_name, self.last_name, self.first_name)

    def __str__(self):
        return "%s %s %s" % (self.middle_name, self.last_name, self.first_name)

    class Meta:
        verbose_name = 'Pacientes'
        verbose_name_plural = 'Pacientes'

        permissions = (
            ('index_patient', 'Can List patient'),
        )
