from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator


class Metar(models.Model):
    RAW_TEXT_RE = r'\A([A-Z]([A-Z]|[0-9]){2,3} [1-3])'
    STATION_ID_RE = r'[A-Z]([A-Z]|[0-9]){2,3}'
    WX_STRING_RE = r'\A[-\+]?[A-Z]{2,10}'
    METAR = 'METAR'
    SPECI = 'SPECI'
    METAR_TYPE_CHOICES = [
        (METAR, 'METAR'),
        (SPECI, 'SPECI')
    ]
    raw_text = models.TextField(
        validators=[RegexValidator(RAW_TEXT_RE)]
    )
    station_id = models.CharField(
        max_length=4,
        validators=[RegexValidator(STATION_ID_RE)]
    )
    observation_time = models.DateTimeField()
    temp_c = models.FloatField(
        validators=[
            MaxValueValidator(70),
            MinValueValidator(-60)
        ]
    )
    dewpoint_c = models.FloatField(
        validators=[
            MaxValueValidator(70),
            MinValueValidator(-60)
        ]
    )
    wind_dir_degrees = models.PositiveSmallIntegerField(
        default=360,
        validators=[MaxValueValidator(360)]
    )
    wind_speed_kt = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(150)]
    )
    wind_gust_kt = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(150)]
    )
    visibility_m = models.PositiveSmallIntegerField(
        default=9999,
        validators=[MaxValueValidator(9999)]
    )
    altim_in_hg = models.FloatField(
        validators=[
            MaxValueValidator(32.5),
            MinValueValidator(25.1)
        ]
    )
    wx_string = models.CharField(
        blank=True,
        max_length=16,
        validators=[RegexValidator(WX_STRING_RE)]
    )
    cloud_ceiling = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    vert_vis_ft = models.PositiveSmallIntegerField(
        blank=True,
        null=True
    )
    metar_type = models.CharField(
        choices=METAR_TYPE_CHOICES,
        default=METAR,
        max_length=5
    )

    class Meta:
        constraints = {
            models.UniqueConstraint(
                fields=['station_id', 'observation_time'],
                name='unique_metar'
            )
        }
