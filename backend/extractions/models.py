import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from donations.models import Donation
from users.models import Employee

ARM = (('I', 'IZQUIERDA'), ('D', 'DERECHA'))
TYPE_PLACE = (('PF', 'PUESTO FIJO'), ('PM', 'PUESTO MOVIL'))
TYPE_BAG = (
    ('SIMPLE', 'SIMPLE'),
    ('DOBLE', 'DOBLE'),
    ('TRIPLE', 'TRIPLE'),
    ('CUADRUPLE', 'CUADRUPLE'),
    ('CUADRUPLE_CON_FILTRO', 'CUADRUPLE CON FILTRO'),
    ('SET_AFERESIS', 'SET DE AFERESIS'),
)
BAGS_QUANTITY_BY_TYPE = {
    'SIMPLE': 1,
    'DOBLE': 2,
    'TRIPLE': 3,
    'CUADRUPLE': 4,
    'CUADRUPLE_CON_FILTRO': 4,
    'SET_AFERESIS': 2,
}


class TypeAnticoagulant(models.Model):
    name = models.CharField(max_length=15, verbose_name='Nombre')

    def __unicode__(self):
        return "%s" % (self.name)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = 'Tipo de Anticoagulante'
        verbose_name_plural = 'Tipos de Anticoagulantes'
        ordering = ['name']

        permissions = (
            ('index_typeanticoagulant', 'Can List TypeAnticoagulant'),
        )


class Extraction(models.Model):
    TYPE_BAG = TYPE_BAG
    BAGS_QUANTITY_BY_TYPE = BAGS_QUANTITY_BY_TYPE

    donation = models.OneToOneField(Donation, unique=True, related_name='extraction', on_delete=models.PROTECT,
                                    verbose_name='Donación')
    type_place = models.CharField(max_length=2, default='PF', choices=TYPE_PLACE, verbose_name='Lugar de Extracción')
    bags_quantity = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)],
                                             verbose_name='Cantidad de bolsas')
    type_bag = models.CharField(max_length=24, choices=TYPE_BAG, default='SIMPLE',
                                verbose_name='Tipo de bolsa')
    lot = models.CharField(max_length=15, verbose_name='Nro. de Lote')
    tubing = models.CharField(max_length=15, null=True, verbose_name='Nro. de Tubuladura')
    barcode = models.CharField(max_length=10, null=True, verbose_name='Código de barras')
    weight = models.FloatField(null=True, verbose_name='Peso')
    arm = models.CharField(max_length=2, null=True, choices=ARM, verbose_name='Brazo')
    initial_time = models.TimeField(verbose_name=u'Hora Inicial de Extracción')
    end_time = models.TimeField(blank=True, null=True, verbose_name=u'Hora Conclusion de Extracción')
    total_time = models.FloatField(blank=True, null=True, verbose_name='Tiempo Total')
    typeanticoagulant = models.ForeignKey(TypeAnticoagulant, on_delete=models.PROTECT, verbose_name='Tipo de Anticoagulante')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Responsable')
    register = models.ForeignKey(Employee, default=1, related_name='%(class)s_register', on_delete=models.PROTECT,
                                 verbose_name='Registrador')
    observations = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    register_at = models.DateField(default=datetime.date.today, verbose_name='Fecha de registro')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Fecha de Creación de Sistema')

    def __unicode__(self):
        return "%s %s" % (self.donation, self.employee)

    def __str__(self):
        return "%s %s" % (self.donation, self.employee)

    class Meta:
        verbose_name = u'Extracción'
        verbose_name_plural = 'Extracciones'
        ordering = ['created_at', 'donation']

        permissions = (
            ('index_extraction', 'Can List Extraction'),
        )

        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(type_bag='SIMPLE', bags_quantity=1) |
                    models.Q(type_bag='DOBLE', bags_quantity=2) |
                    models.Q(type_bag='TRIPLE', bags_quantity=3) |
                    models.Q(type_bag='CUADRUPLE', bags_quantity=4) |
                    models.Q(type_bag='CUADRUPLE_CON_FILTRO', bags_quantity=4) |
                    models.Q(type_bag='SET_AFERESIS', bags_quantity=2)
                ),
                name='extraction_type_bag_quantity_valid',
            ),
        ]

    def save(self, *args, **kwargs):
        try:
            self.bags_quantity = self.BAGS_QUANTITY_BY_TYPE[self.type_bag]
        except KeyError:
            raise ValueError('El tipo de bolsa seleccionado no es válido.')
        super(Extraction, self).save(*args, **kwargs)


class SelfExclusion(models.Model):
    extraction = models.OneToOneField(Extraction, unique=True, related_name='selfexclusion',
                                      on_delete=models.PROTECT,
                                      verbose_name='Estracción')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Responsable')
    observations = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    register = models.ForeignKey(Employee, related_name='%(class)s_register', on_delete=models.PROTECT,
                                 verbose_name='Registrador')
    register_at = models.DateField(default=datetime.date.today, verbose_name='Fecha de registro')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Fecha de Creación')

    def __unicode__(self):
        return "%s %s" % (self.extraction, self.employee)

    def __str__(self):
        return "%s %s" % (self.extraction, self.employee)

    class Meta:
        verbose_name = u'Autoexclusion'
        verbose_name_plural = 'Autoexclusiones'
        ordering = ['created_at', 'extraction']

        permissions = (
            ('index_selfexclusion', 'Can list selfexclusion'),
        )


LEVEL_OPTIONS = (('LOW', 'LEVE'), ('MEDIUM', 'MODERADA'), ('HIGH', 'SEVERA'))


class TypeAdverseReaction(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    level = models.CharField(max_length=6, default='LOW', choices=LEVEL_OPTIONS, verbose_name="Categoría")
    show_in_conventional = models.BooleanField(default=True, verbose_name="Mostrar en Donación convencional")
    show_in_apheresis = models.BooleanField(default=False, verbose_name="Mostrar en Aféresis")

    def __unicode__(self):
        return "%s" % self.name

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = u'Tipo de reacción adversa'
        verbose_name_plural = 'Tipos de reacciones adversas'
        ordering = ['name']

        permissions = (
            ('index_typeadversereaction', 'Can List TypeAdverseReaction'),
        )


EVOLUTION = (('RR', 'RECUPERACION RAPIDA'), ('RL', 'RECUPERACION LENTA'), ('HO', 'HOSPITALIZACION'))
DETECTION = (('TD', 'DURANTE LA DONACION'), ('AD', 'DESPUES DE LA DONACION'))
EXTRACTION_PLACE = (('PF', 'PUESTO FIJO'), ('UM', 'UNIDAD MOVIL'))


class AdverseReaction(models.Model):
    extraction = models.OneToOneField(Extraction, unique=True, related_name='adversereaction', on_delete=models.PROTECT,
                                      verbose_name='Donación')
    type = models.ManyToManyField(TypeAdverseReaction, verbose_name='Tipo de Reacción Adversa')
    extraction_place = models.CharField(max_length=2, choices=EXTRACTION_PLACE, verbose_name='Lugar de Extracción')
    evolution = models.CharField(max_length=3, choices=EVOLUTION, verbose_name='Evolución')
    detection = models.CharField(max_length=2, choices=DETECTION, verbose_name='Detección')
    behavior_taken = models.TextField(null=True, blank=True, verbose_name='Conducta Tomada')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Responsable')
    observations = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    register_at = models.DateTimeField(default=datetime.date.today, verbose_name='Fecha de registro')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Fecha de Creación')

    def __unicode__(self):
        return "%s %s" % (self.extraction, self.employee)

    def __str__(self):
        return "%s %s" % (self.extraction, self.employee)

    class Meta:
        verbose_name = u'Reaccion Adversa'
        verbose_name_plural = 'Reacciones Adversas'
        ordering = ['created_at', 'extraction']

        permissions = (
            ('index_adversereaction', 'Can List AdverseReaction'),
        )
