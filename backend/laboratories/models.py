from django.db import models
from donations.models import Donation
from extractions.models import Extraction
from users.models import Employee
from django.db.models import JSONField
import datetime

CROSSES = (('-', 'Negativo'), ('+', '+'), ('++', '++'), ('+++', '+++'), ('++++', '++++'))
INVERSE_CROSSES = (('-', 'Negativo'), ('+', '+'), ('++', '++'), ('+++', '+++'), ('++++', '++++'), ('H', 'Hemólisis'))
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
CROSSES_KELL = (('-', 'Negativo'), ('+', 'Positivo'))

class Immunohematology(models.Model):
    donation = models.OneToOneField(Donation, on_delete=models.PROTECT, null=True, verbose_name='Donación')
    direct_abo = models.CharField(max_length=4, choices=BLOOD_GROUP_OPTIONS, null=True, blank=True, verbose_name='Directa ABO')
    inverse_abo = models.CharField(max_length=4, choices=BLOOD_GROUP_OPTIONS, null=True, blank=True, verbose_name='Inversa ABO')
    factor_rh = models.CharField(max_length=3, choices=RH_OPTIONS, verbose_name='Factor RH')
    phenotype = models.CharField(max_length=15, null=True, blank=True, verbose_name='Fenotipo')
    antikell = models.CharField(max_length=4, choices=CROSSES_KELL, null=True, blank=True, verbose_name='AntiKell')

    fsi = models.CharField(max_length=4, choices=CROSSES, null=True, blank=True, verbose_name='Panel 1 SAL.')
    liss = models.CharField(max_length=4, choices=CROSSES, null=True, blank=True, verbose_name='Panel 1 LISS.')
    alb = models.CharField(max_length=4, choices=CROSSES, null=True, blank=True, verbose_name='Panel 1 Albumina.')
    coombs = models.CharField(max_length=4, choices=CROSSES, null=True, blank=True, verbose_name='Panel 1 COOMBS')

    p2fsi = models.CharField(max_length=4, choices=CROSSES, null=True, blank=True, verbose_name='Panel 2 FSI.')
    p2liss = models.CharField(max_length=4, choices=CROSSES, null=True, blank=True, verbose_name='Panel 2 LISS.')
    p2alb = models.CharField(max_length=4, choices=CROSSES, null=True, blank=True,
                             verbose_name='Panel 2 Albumina.')
    p2coombs = models.CharField(max_length=4, choices=CROSSES, null=True, blank=True, verbose_name='Panel 2 COOMBS')

    p3fsi = models.CharField(max_length=4, choices=CROSSES, null=True, blank=True, verbose_name='Panel 3 FSI.')
    p3liss = models.CharField(max_length=4, choices=CROSSES, null=True, blank=True, verbose_name='Panel 3 LISS.')
    p3alb = models.CharField(max_length=4, choices=CROSSES, null=True, blank=True,
                             verbose_name='Panel 3 Albumina.')
    p3coombs = models.CharField(max_length=4, choices=CROSSES, null=True, blank=True, verbose_name='Panel 3 COOMBS')

    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Empleado')
    observations = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    register_at = models.DateField(default=datetime.date.today, verbose_name='Fecha de Registro')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Fecha de Creación')

    def __unicode__(self):
        return "%s" % self.donation

    def __str__(self):
        return "%s" % self.donation

    @property
    def exists_irregular_antibodies(self):
        positive_results = {'+', '++', '+++', '++++'}
        panel_results = (
            self.fsi, self.liss, self.alb, self.coombs,
            self.p2fsi, self.p2liss, self.p2alb, self.p2coombs,
            self.p3fsi, self.p3liss, self.p3alb, self.p3coombs,
        )
        return any(result in positive_results for result in panel_results if result is not None)

    class Meta:
        verbose_name = 'Inmunohematologia'
        verbose_name_plural = 'Inmunohematologias'

        permissions = (
            ('index_immunohematology', 'Can List Immunohematology'),
        )


TYPE_REACT = (('R', 'REACTIVO'), ('NR', 'NO REACTIVO'), ('IN', 'INDETERMINADO'))


class Immunoserology(models.Model):
    donation = models.OneToOneField(Donation, on_delete=models.PROTECT, null=True, verbose_name='Donación')
    chagas_hai = models.CharField(max_length=2, choices=TYPE_REACT, null=True, verbose_name='CHAGAS HAI')
    cheia = models.CharField(max_length=2, choices=TYPE_REACT, null=True, verbose_name='Elisa')
    rpr = models.CharField(max_length=2, choices=TYPE_REACT, null=True, verbose_name='RPR')
    hvc = models.CharField(max_length=2, choices=TYPE_REACT, null=True, verbose_name='HVC')
    hbsag = models.CharField(max_length=2, choices=TYPE_REACT, null=True, verbose_name='HBsAg')
    hiv = models.CharField(max_length=2, choices=TYPE_REACT, null=True, verbose_name='HIV')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Empleado')
    observations = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    history = JSONField(default=list, verbose_name='Historial de Cambios')
    register_at = models.DateField(default=datetime.date.today, verbose_name='Fecha de Registro')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Fecha de Creación')

    def __unicode__(self):
        return "%s" % self.donation

    def __str__(self):
        return "%s" % self.donation

    class Meta:
        verbose_name = 'Inmunoserologia'
        verbose_name_plural = 'Inmunoserologias'

        permissions = (
            ('index_immunoserology', 'Can List Immunoserology'),
        )


TYPE_TEST = (('0', 'CHAGAS WIENER'),
             ('1', 'CHAGAS BIOS CHILE'),
             ('2', 'HCV DIALAB'),
             ('3', 'HBsAg BIO-RAD '),
             ('4', 'HIV BIO-RAD'),
             ('5', 'HAI-CHAGAS'),
             ('6', 'R.P.R. SIFILIS'),
             ('7', 'TPHA SIFILIS'))


class SerologyProtocol(models.Model):
    method = models.CharField(max_length=200, verbose_name='Tecnica a procesar')
    kit = models.CharField(max_length=200, verbose_name='KIT')
    due_date_at = models.DateField(default=datetime.date.today, verbose_name='Fecha de Vencimiento')
    lot = models.CharField(max_length=200, verbose_name='Nro. de Lote')
    industry = models.CharField(max_length=200, verbose_name='Industria')
    test = models.IntegerField(default=1, verbose_name='Nro. de Prueba (Máquina)')
    values = JSONField(default=list, verbose_name='Datos')
    type = models.CharField(max_length=2, choices=TYPE_TEST, verbose_name='Tipo de Prueba')
    cutt_off = models.CharField(blank=True, null=True, max_length=15, verbose_name='Cutt Off')
    cutt_off_max = models.CharField(blank=True, null=True, max_length=15, verbose_name='Cutt Off Max')
    cutt_off_min = models.CharField(blank=True, null=True, max_length=15, verbose_name='Cutt Off Min')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Empleado')
    register_at = models.DateField(default=datetime.date.today, verbose_name='Fecha de Realización')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Fecha de Creación')

    def __unicode__(self):
        return "%s" % self.method

    def __str__(self):
        return "%s" % self.method

    class Meta:
        verbose_name = 'Protocolo de Serologia'
        verbose_name_plural = 'Protocolos de  Serologias'

        permissions = (
            ('index_serologyprotocol', 'Can List SerologyProtocol'),
        )
