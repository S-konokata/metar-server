from django.db import models


class Metar(models.Model):
    # "calc" comment column is needed to be converted from raw text. 
    raw_text = models.TextField()
    station_id = models.CharField(max_length=4)
    observation_time = models.DateTimeField()
    temp_c = models.FloatField()
    dewpoint_c = models.FloatField()
    wind_dir_degrees = models.PositiveSmallIntegerField()
    wind_speed_kt = models.PositiveSmallIntegerField()
    wind_gust_kt = models.PositiveSmallIntegerField()
    visibility_m = models.PositiveSmallIntegerField()  # calc
    altim_in_hg = models.FloatField()  # calc
    wx_string = models.CharField(max_length=12)
    cloud_ceiling = models.PositiveIntegerField()  # calc(from other column)
    metar_type = models.CharField(max_length=5)
