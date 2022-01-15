from django.db import models
from django.contrib.gis.db import models as gis_models
from django.utils.translation import  gettext as _
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
# Create your models here.


class GeoModel(gis_models.Model):
    HOSPITAL = 1
    MARKET = 2
    RESTAURANT = 3
    SCHOOL = 4
    PETROL_STATION = 5
    OTHERS = 6
    PLACES = [
        (HOSPITAL, _('Hastane')),
        (MARKET, _('Market')),
        (RESTAURANT, _('Restorant')),
        (SCHOOL, _('Okul')),
        (PETROL_STATION, _('Benzinlik')),
        (OTHERS, _('Diğer'))
    ]
    name = models.CharField(verbose_name=_('Ad'), max_length=250)
    type = models.CharField(max_length=250)
    desc = models.CharField(max_length=250)
    place = models.IntegerField(choices=PLACES, blank=True, null=True)
    radius = models.IntegerField(blank=True, null=True)
    poly = gis_models.PolygonField(blank=True, null=True)
    line = gis_models.LineStringField(blank=True, null=True)
    point = gis_models.PointField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Place(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, blank=True, null=True)







# class Driver(models.Model):
#     name = models.TextField()
#     license = models.TextField()
#
#     def __str__(self):
#         return self.name
#
#
# class Car(models.Model):
#     make = models.TextField()
#     model = models.TextField()
#     year = models.IntegerField()
#     vin = models.TextField()
#     owner = models.ForeignKey("Driver", on_delete=models.SET_NULL, null=True)
#
#     def __str__(self):
#         return self.model
