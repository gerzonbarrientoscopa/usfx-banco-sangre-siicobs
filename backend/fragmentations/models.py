from django.db import models
from django.utils import timezone

from extractions.models import Extraction
from packages.models import TypeHemocomponent, TypeDiscard
from users.models import Employee, Medical

QUALITY_BAG = (('AP', 'APTO'), ('NA', 'NO APTO'))


class Fragmentation(models.Model):
    extraction = models.OneToOneField(Extraction, null=True, blank=True, related_name='fragmentation',
                                      on_delete=models.PROTECT, verbose_name='Extracción')
    register_at = models.DateTimeField(verbose_name='Hora de ingreso')
    quality_bag = models.CharField(max_length=2, choices=QUALITY_BAG, verbose_name='Calidad de bolsa')
    total_hc = models.FloatField(verbose_name='Total HC')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Responsable')
    register = models.ForeignKey(Employee, related_name='%(class)s_register', on_delete=models.PROTECT,
                                 verbose_name='Registrador')
    observations = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Registro')

    def __unicode__(self):
        return "%s" % self.extraction

    def __str__(self):
        return "%s" % self.extraction

    class Meta:
        verbose_name = 'Fraccionamiento'
        verbose_name_plural = 'Fraccionamientos'

        permissions = (
            ('index_fragmentation', 'Can List Fragmentation'),
        )


class TypeIrregularAntiBody(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    text_bag = models.CharField(max_length=100, null=True, verbose_name='Texto en Bolsa')
    recommendation = models.TextField(null=True, blank=True, verbose_name='Recomendación')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')

    def __unicode__(self):
        return "%s" % self.name

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Tipo de Anticuerpo Irregular'
        verbose_name_plural = 'Tipos de Anticuerpos Irregulares'
        ordering = ['name']

        permissions = (
            ('index_typeirregularantibody', 'Can List Type Irregular AntiBody'),
        )


STATUS_ITEM = (('LAB', 'EN LABORATORIO'), ('LIB', 'LIBERADO'), ('END', 'EN DISTRIBUCION'), ('DIS', 'DISTRIBUIDO'),
               ('DES', 'DESCARTADO'))


class ItemFragmentation(models.Model):
    donor_code = models.IntegerField(default=1, verbose_name='Código de Donante')
    fragmentation = models.ForeignKey(Fragmentation, related_name='itemfragmentations', on_delete=models.PROTECT,
                                      verbose_name='Fraccionamiento')
    typehemocomponent = models.ForeignKey(TypeHemocomponent, related_name='typehemocomponent', on_delete=models.PROTECT,
                                          verbose_name='Tipo de Hemocomponente')
    typediscard = models.ForeignKey(TypeDiscard, null=True, blank=True, related_name='typediscard',
                                    on_delete=models.PROTECT, verbose_name='Tipo de Descarte')
    type_irregular_antibody = models.ForeignKey(TypeIrregularAntiBody, null=True, blank=True,
                                                related_name='type_irregular_antibody',
                                                on_delete=models.PROTECT, verbose_name='Tipo de Descarte')
    expiration_date = models.DateTimeField(verbose_name='Fecha de Expiración')
    is_satellite_bag = models.BooleanField(null=True, verbose_name='Es bolsa Satelite')
    is_max_expiration_days = models.BooleanField(default=False, verbose_name='Es Maxima Duración  en dias')
    weight = models.FloatField(verbose_name='Peso (Volumen)')
    status = models.CharField(max_length=3, default='LAB', choices=STATUS_ITEM, verbose_name='Estado')
    observations = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    lot = models.CharField(max_length=15, null=True, verbose_name='Nro. de Lote')
    tubing = models.CharField(max_length=15, null=True, verbose_name='Nro. de Tubuladura')
    register_at = models.DateField(auto_now_add=True, verbose_name='Fecha Registro')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')

    def __unicode__(self):
        return "%s - %s - %s " % (self.donor_code, self.typehemocomponent, self.typediscard)

    def __str__(self):
        return "%s - %s - %s " % (self.donor_code, self.typehemocomponent, self.typediscard)

    class Meta:
        verbose_name = 'Item de Fraccionamiento'
        verbose_name_plural = 'Items de Fraccionamientos'
        ordering = ['typehemocomponent__name']

        permissions = (
            ('index_itemfragmentation', 'Can List Items Fragmentation'),
            ('changetype_itemfragmentation', 'Change Type Item Fragmentation'),
        )


class Discard(models.Model):
    itemfragmentation = models.OneToOneField(ItemFragmentation, on_delete=models.PROTECT, related_name='discard',
                                             verbose_name='Item Fragmentación')
    reason = models.TextField(verbose_name='Causas de Descarte')
    observations = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Responsable')
    register = models.ForeignKey(Employee, related_name='%(class)s_register', on_delete=models.PROTECT,
                                 verbose_name='Registrador')
    register_at = models.DateField(default=timezone.now, verbose_name='Fecha Registro')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')

    def __unicode__(self):
        return "%s" % self.itemfragmentation

    def __str__(self):
        return "%s" % self.itemfragmentation

    class Meta:
        verbose_name = 'Descarte'
        verbose_name_plural = 'Descartes'
        ordering = ['-register_at']

        permissions = (
            ('index_discard', 'Can List Discard'),
        )


class Release(models.Model):
    itemfragmentation = models.OneToOneField(ItemFragmentation, on_delete=models.PROTECT, related_name='release',
                                             verbose_name='Item Fragmentación')
    observations = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Responsable')
    register = models.ForeignKey(Employee, related_name='%(class)s_register', on_delete=models.PROTECT,
                                 verbose_name='Registrador')
    register_at = models.DateField(default=timezone.now, verbose_name='Fecha Registro')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')

    def __unicode__(self):
        return "%s" % self.itemfragmentation

    def __str__(self):
        return "%s" % self.itemfragmentation

    class Meta:
        verbose_name = 'Liberación'
        verbose_name_plural = 'Liberaciones'
        ordering = ['-register_at']

        permissions = (
            ('index_release', 'Can List Release'),
        )


STATUS_RR = ((1, 'NUEVO'), (2, 'EN PROCESO'), (3, 'LIBERADO'))


class ReleaseRequest(models.Model):
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    status = models.CharField(max_length=2, choices=STATUS_RR, verbose_name='Estado')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Responsable')
    attendant = models.ForeignKey(Employee, related_name='%(class)s_attendant', on_delete=models.PROTECT,
                                  verbose_name='Encargado')
    medical = models.ForeignKey(Medical, on_delete=models.PROTECT, verbose_name='Médico Solicitante')
    register_at = models.DateTimeField(default=timezone.now, verbose_name='Fecha Registro')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')

    def __unicode__(self):
        return "%s" % self.description

    def __str__(self):
        return "%s" % self.description

    class Meta:
        verbose_name = 'Solicitud de Liberación'
        verbose_name_plural = 'Solicitudes de Liberaciones'
        ordering = ['-register_at']

        permissions = (
            ('index_releaserequest', 'Can List Release Request'),
        )


class ReleaseTypeHemocomponent(models.Model):
    release = models.ForeignKey(ReleaseRequest, related_name='typeHemocomponents', on_delete=models.PROTECT,
                                verbose_name='Solicitud de Liberación')
    typehemocomponent = models.ForeignKey(TypeHemocomponent, on_delete=models.PROTECT,
                                          verbose_name='Tipo de Hemocomponente')
    quantity_request = models.BigIntegerField(verbose_name='Cantidad Solicitada')
    quantity_release = models.BigIntegerField(verbose_name='Cantidad Liberada')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')

    def __unicode__(self):
        return "%s" % self.typehemocomponent

    def __str__(self):
        return "%s" % self.typehemocomponent

    class Meta:
        verbose_name = 'Liberación de Hemocomponente'
        verbose_name_plural = 'Liberación de Hemocomponentes'
        ordering = ['typehemocomponent__name']

        permissions = (
            ('index_releasetypehemocomponent', 'Can List Release TypeHemocomponent'),
        )
