import uuid
from dateutil.relativedelta import relativedelta
from django.db import models
from fragmentations.models import ItemFragmentation
from users.models import Employee, Institution, Medical, Patient

TYPE_PAYMENT = (('CA', 'EFECTIVO'), ('AC', 'CUENTAS POR COBRAR'))
TYPE_AGE = (('Y', 'Años'), ('D', 'Días'), ('M', 'Meses'),)
STATUS_DISTRIBUTION = (
    ('NEW', 'NUEVO'), ('IN_PROGRESS', 'EN PROCESO'), ('DELIVERED', 'ENTREGADO'), ('CANCELED', 'CANCELADO'),
    ('REFUNDED', 'DEVUELTO'),
    ('PARTIAL_REFUNDED', 'PARCIALMENTE DEVUELTO'))


class Distribution(models.Model):
    uuid = models.UUIDField(unique=True, null=True, editable=False)
    patient = models.ForeignKey(Patient, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Paciente')
    age_patient = models.IntegerField(default=0, verbose_name='Edad actual del Paciente')
    age_patient_type = models.CharField(max_length=1, default='Y', choices=TYPE_AGE, verbose_name='Tipo de Edad')
    register_at = models.DateTimeField(verbose_name='Hora de ingreso')
    service_transfunctional = models.CharField(max_length=255, null=True, blank=True,
                                               verbose_name='Servicio Transfusional')
    medical = models.ForeignKey(Medical, on_delete=models.PROTECT, verbose_name='Médico Solicitante')
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, verbose_name='Institución')
    is_donation = models.BooleanField(default=False, verbose_name='Donación')
    is_delivered = models.BooleanField(default=False, verbose_name='Esta entregado?')
    status = models.CharField(max_length=20, choices=STATUS_DISTRIBUTION, default='DELIVERED', verbose_name='Estado')
    type_payment = models.CharField(max_length=2, default='CA', choices=TYPE_PAYMENT, verbose_name='Tipo de Pago')
    invoice_number = models.BigIntegerField(null=True, blank=True, verbose_name='Número de Factura')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Empleado')
    observations = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name=u'Fecha de Entrega')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Fecha de Creación')

    def __unicode__(self):
        return "%s %s [%s]" % (self.register_at, self.patient, self.medical)

    def __str__(self):
        return "%s %s [%s]" % (self.register_at, self.patient, self.medical)

    class Meta:
        verbose_name = 'Distribución'
        verbose_name_plural = 'Distribuciones'

        permissions = (
            ('index_distribution', 'Can List Distribution'),
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uuid = uuid.uuid4()

        if self.patient and self.patient.birth_date and self.register_at:
            registered_date = self.register_at.date()
            age = relativedelta(registered_date, self.patient.birth_date)
            if age.years > 0:
                self.age_patient = age.years
                self.age_patient_type = 'Y'
            elif age.months > 0:
                self.age_patient = age.months
                self.age_patient_type = 'M'
            else:
                self.age_patient = max(age.days, 0)
                self.age_patient_type = 'D'

        super(Distribution, self).save(*args, **kwargs)


class DistributionItemFragmentation(models.Model):
    distribution = models.ForeignKey(Distribution, on_delete=models.PROTECT, verbose_name='Distribución',
                                     related_name='itemfragmentations')
    itemfragmentation = models.ForeignKey(ItemFragmentation, related_name='distributionitemfragmentations',
                                          on_delete=models.PROTECT, verbose_name='Item de Fraccionamiento')

    def __unicode__(self):
        return "%s" % self.distribution

    def __str__(self):
        return "%s" % self.distribution

    class Meta:
        verbose_name = 'Distribución de Item de Fraccionamiento'
        verbose_name_plural = 'Distribuciones de Items de Fraccionamiento'

        permissions = (
            ('index_distributionitemfragmentation', 'Can List Distribution Items Fragmentation'),
        )


class DistributionItemFragmentationRefunded(models.Model):
    register_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    distributionitemfragmentation = models.OneToOneField(DistributionItemFragmentation, on_delete=models.PROTECT,
                                                         verbose_name='Distribución')
    reason = models.TextField(verbose_name="Razon")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Fecha de Creación')

    def __unicode__(self):
        return "%s" % self.distributionitemfragmentation

    def __str__(self):
        return "%s" % self.distributionitemfragmentation

    class Meta:
        verbose_name = 'Devolución de Distribución de Item de Fraccionamiento'
        verbose_name_plural = 'Devoluciones de Distribución de Item de Fraccionamiento'

        permissions = (
            ('index_distributionitemfragmentationrefunded', 'Can List Distribution Items Fragmentation Refunded'),
        )
