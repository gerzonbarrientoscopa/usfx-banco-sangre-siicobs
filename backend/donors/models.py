# encoding:utf-8
from django_countries.fields import CountryField
from django.db import models
from settings.models import Place
from siicobs_main.utils_global import get_age_from_birthday
from users.models import Employee
import datetime

GENDER = (('F', 'FEMENINO'), ('M', 'MASCULINO'))

CIVIL_STATUS = (
    ('SO', 'SOLTERO/A'), ('CO', 'COMPROMETIDO/A'), ('CA', 'CASADO/A'), ('DI', 'DIVORCIADO/A'), ('VI', 'VIUDO/A'),
    ('CON', 'CONCUBINO/A'))

DEPARTMENTS = (
    ('LP', 'LA PAZ'), ('OR', 'ORURO'), ('PO', u'POTOSÍ'), ('CO', 'COCHABAMBA'), ('CH', 'CHUQUISACA'),
    ('TA', 'TARIJA'), ('PA', 'PANDO'), ('BE', 'BENI'), ('SC', 'SANTA CRUZ'), ('', ''))

DEGREE_INSTRUCTION = (
    ('SIN_EST', 'SIN ESTUDIOS'),
    ('PRI', 'PRIMARIA'),
    ('SEC', 'SECUNDARIA'),
    ('BAC', 'BACHILLER'),
    ('UNIV', 'UNIVERSITARIA'),
    ('PROF', 'PROFESIONAL')
)
BLOOD_GROUP_OPTIONS = (
    ('O', 'O'),
    ('A1', 'A1'),
    ('A2', 'A2'),
    ('B', 'B'),
    ('A1B', 'A1B'),
    ('A2B', 'A2B')
)
RH_OPTIONS = (
    ('RH+', 'RH (Positivo)'),
    ('RHD', 'RH Debil'),
    ('RH-', 'RH (Negativo)')
)


class Donor(models.Model):
    code = models.IntegerField(unique=True, db_index=True, verbose_name='Código del Donante')
    code_other = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'Códigos Secundarios')
    image = models.FileField(upload_to='images', null=True, blank=True, verbose_name='Imagen')
    civil_status = models.CharField(max_length=3, choices=CIVIL_STATUS, verbose_name='Estado Civil', null=True)
    first_name = models.CharField(max_length=50, default='', db_index=True, verbose_name='Nombres')
    middle_name = models.CharField(max_length=50, default='', db_index=True, null=True, blank=True,
                                   verbose_name='Apellido Paterno')
    last_name = models.CharField(max_length=100, default='', db_index=True, null=True, blank=True,
                                 verbose_name='Apellido Materno')
    ci = models.CharField(max_length=20, unique=True, null=True, verbose_name='Doc. de Ident./DNI')
    ci_extension = models.CharField(max_length=2, choices=DEPARTMENTS, null=True, blank=True,
                                    verbose_name='Extensión de CI')
    birth_date = models.DateField(verbose_name='Fecha Nacimiento', null=True)
    age = models.IntegerField(verbose_name='Edad', null=True)
    gender = models.CharField(max_length=2, choices=GENDER, verbose_name=u'Sexo', null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    can_donate = models.BooleanField(default=True, verbose_name='Puede Donar')
    is_volunteer = models.BooleanField(default=False, verbose_name='Es voluntario')

    residence = models.CharField(max_length=100, blank=True, null=True, verbose_name='Domicilio')
    zone = models.CharField(max_length=100, blank=True, null=True, verbose_name='Zona')
    province = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ciudad/Provincia')
    department = models.CharField(max_length=2, choices=DEPARTMENTS, verbose_name='Departamento', null=True)
    country = CountryField(blank_label='(Seleccione País)', verbose_name=u'País', null=True)

    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'Teléfono')
    mobile_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Tel. Celular')
    family_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'Tel. Familiar')
    profession = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Profesion/Ocupación')
    degree_instruction = models.CharField(max_length=15, choices=DEGREE_INSTRUCTION,
                                          verbose_name=u'Grado Intrucción', null=True)

    job = models.CharField(max_length=100, blank=True, null=True, verbose_name='Trabajo')
    job_address = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Dirección')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name=u'Correo Electrónico')
    group_abo = models.CharField(null=True, blank=True, max_length=3, choices=BLOOD_GROUP_OPTIONS,
                                 verbose_name='Grupo ABO')
    factor_rh = models.CharField(null=True, blank=True, max_length=3, choices=RH_OPTIONS, verbose_name='Factor RH')

    def __unicode__(self):
        return "%s - %s %s %s" % (self.code, self.middle_name, self.last_name, self.first_name)

    def __str__(self):
        return "%s - %s %s %s" % (self.code, self.middle_name, self.last_name, self.first_name)

    class Meta:
        verbose_name = 'Donante'
        verbose_name_plural = 'Donantes'
        unique_together = ['code']
        ordering = ['code', 'first_name', 'middle_name', 'last_name', ]

        permissions = (
            ('index_donor', 'Can List Donor'),
            ('enable_rejected_donor', 'Enabled Rejected Donor'),
        )

    def save(self, *args, **kwargs):
        # calculate age
        if self.birth_date:
            self.age = get_age_from_birthday(self.birth_date)

        super(Donor, self).save(*args, **kwargs)


class DonorHistory(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.PROTECT, verbose_name='Donante')
    reason = models.TextField(verbose_name=u'Razón')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Responsable')
    register_at = models.DateField(default=datetime.date.today, verbose_name=u'Fecha de Donación')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Fecha de Creación')

    def __unicode__(self):
        return "%s %s" % (self.donor, self.reason)

    def __str__(self):
        return "%s %s" % (self.donor, self.reason)

    class Meta:
        verbose_name = u'Historial cambio donante'
        verbose_name_plural = 'Historial cambios donante'
        ordering = ['-register_at', 'donor']
        permissions = (
            ('index_donorhistory', 'Can list donorhistory'),
        )
