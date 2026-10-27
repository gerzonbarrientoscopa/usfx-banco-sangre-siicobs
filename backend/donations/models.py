from django.db import models
from django.utils import timezone
import datetime
from donors.models import Donor
from promotions.models import Event
from settings.models import Reason, Place
from siicobs_main.utils_global import get_age_from_birthday
from users.models import Patient, Employee

TYPE_DONATION = (('VA', 'VOLUNTARIA ALTRUISTA'), ('RS', 'REPOSICION SOLIDARIA'), ('RE', 'REPOSICION EXIGIDA'),
                 ('DA', 'DONACION AUTOLOGA'))

TYPE_PROCESS = (('NO', 'CONVENCIONAL'), ('NA', 'AFERESIS NORMAL'))

class Donation(models.Model):
    donor = models.ForeignKey(Donor, related_name='donations', on_delete=models.PROTECT, verbose_name='Donante')
    type_process = models.CharField(default='NO', max_length=2, choices=TYPE_PROCESS, verbose_name="Tipo de Proceso")
    age_donor = models.IntegerField(default=0, verbose_name='Edad actual del Donante')
    type_donation = models.CharField(max_length=2, choices=TYPE_DONATION, verbose_name=u'Tipo de Donación')
    last_donation_at = models.DateField(blank=True, null=True, verbose_name=u'Fecha de última Donación')
    place = models.ForeignKey(Place, on_delete=models.PROTECT, verbose_name='Lugar de Extracción')
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL,
                              verbose_name='Evento o Institución')
    patient = models.ForeignKey(Patient, null=True, blank=True, on_delete=models.PROTECT,
                                verbose_name='Nombres y Apellidos Receptor')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Responsable')
    register = models.ForeignKey(Employee, default=1, related_name='%(class)s_register', on_delete=models.PROTECT,
                                 verbose_name='Registrador')
    register_at = models.DateField(default=datetime.date.today, verbose_name=u'Fecha de Donación')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Fecha de Creación')

    def __unicode__(self):
        return "%s %s" % (self.donor, self.type_donation)

    def __str__(self):
        return "%s %s" % (self.donor, self.type_donation)

    def save(self, *args, **kwargs):
        # calculate age
        donor = Donor.objects.get(pk=self.donor_id)
        today = self.register_at
        self.age_donor = get_age_from_birthday(donor.birth_date, today)

        super(Donation, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'Donación'
        verbose_name_plural = 'Donaciones'
        ordering = ['-register_at', 'donor']
        unique_together = ('donor', 'register_at', 'employee')
        permissions = (
            ('index_donation', 'Can List Donation'),
        )

TYPE_RESOURCE = (
    ('Exam', 'Pre-Tamizaje'), ('PhysicalAnalysis', 'Tamizaje Clínico'), ('ClinicalHistory', 'Historia Clinica'))


class Rejected(models.Model):
    donation = models.OneToOneField(Donation, related_name='rejected', unique=True, on_delete=models.PROTECT,
                                    verbose_name='Donación')
    reason = models.ForeignKey(Reason, related_name='reason', on_delete=models.PROTECT, verbose_name=u'Razón ')
    observations = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Responsable')
    resource_id = models.IntegerField(default=1, verbose_name='Modelo id')
    resource = models.CharField(default='Exam', choices=TYPE_RESOURCE, max_length=25, verbose_name='Modelo')
    register_at = models.DateTimeField(default=timezone.now, verbose_name=u'Fecha de Rechazo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Fecha de Creación')

    def __unicode__(self):
        return "%s %s" % (self.donation, self.reason)

    def __str__(self):
        return "%s %s" % (self.donation, self.reason)

    class Meta:
        verbose_name = u'Diferido'
        verbose_name_plural = 'Diferidos'
        ordering = ['created_at', 'reason']

        permissions = (
            ('index_rejected', 'Can List Rejected'),
        )


class PhysicalAnalysis(models.Model):
    donation = models.OneToOneField(Donation, unique=True, related_name='physicalanalysis', on_delete=models.PROTECT,
                                    verbose_name='Donación')
    systolic = models.FloatField(null=True, blank=True, verbose_name='Sistólica')
    diastolic = models.FloatField(null=True, blank=True, verbose_name=u'Diastólica')
    pulse = models.FloatField(null=True, blank=True, verbose_name='Pulso')
    tall = models.FloatField(null=True, blank=True, verbose_name='Talla')
    weight = models.FloatField(null=True, blank=True, verbose_name='Peso')
    temperature = models.FloatField(null=True, blank=True, verbose_name='Temperatura')
    observations = models.TextField(null=True, blank=True, verbose_name='Obs.')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Responsable')
    register = models.ForeignKey(Employee, default=1, related_name='%(class)s_register', on_delete=models.PROTECT,
                                 verbose_name='Registrador')
    register_at = models.DateField(default=datetime.date.today, verbose_name='Fecha de registro')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Fecha de Creación')

    def __unicode__(self):
        return "%s %s" % (self.donation, self.employee)

    def __str__(self):
        return "%s %s" % (self.donation, self.employee)

    class Meta:
        verbose_name = u'Examen Fisico'
        verbose_name_plural = 'Examen Físicos'
        ordering = ['created_at', 'donation']

        permissions = (
            ('index_physicalanalysis', 'Can List PhysicalAnalysis'),
        )


BLOOD_GROUP = (('A-', 'A RH-'), ('A+', 'A RH+'), ('B-', 'B RH-'), ('B+', 'B RH+'), ('AB-', 'AB RH-'), ('AB+', 'AB RH+'),
               ('O-', 'O RH-'), ('O+', 'O RH+'))
TYPE_CHAGAS = (('R', 'REACTIVO'), ('NR', 'NO REACTIVO'))
TYPE_RPR = (('R', 'REACTIVO'), ('NR', 'NO REACTIVO'))


class Exam(models.Model):
    donation = models.OneToOneField(Donation, related_name='exam', on_delete=models.PROTECT,
                                    verbose_name='Donación')
    hematocrit = models.FloatField(null=True, blank=True, verbose_name='Hematocrito')
    hemoglobin = models.FloatField(null=True, blank=True, verbose_name='Hemoglobina')
    blood_group = models.CharField(max_length=3, null=True, blank=True, choices=BLOOD_GROUP,
                                   verbose_name='Grupo Sanguíneo')
    chagas = models.CharField(max_length=2, null=True, blank=True, choices=TYPE_CHAGAS, verbose_name='Chagas')
    rpr = models.CharField(max_length=2, null=True, blank=True, choices=TYPE_RPR, verbose_name='RPR')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Responsable')
    register = models.ForeignKey(Employee, default=1, related_name='%(class)s_register', on_delete=models.PROTECT,
                                 verbose_name='Registrador')
    observations = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    register_at = models.DateField(default=datetime.date.today, verbose_name='Fecha de registro')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Fecha de Creación')

    def __unicode__(self):
        return "%s %s" % (self.donation, self.employee)

    def __str__(self):
        return "%s %s" % (self.donation, self.employee)

    class Meta:
        verbose_name = u'Examen'
        verbose_name_plural = 'Examenes'
        ordering = ['created_at', 'donation']

        permissions = (
            ('index_exam', 'Can List Exam'),
        )

