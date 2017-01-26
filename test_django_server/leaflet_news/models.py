from __future__ import unicode_literals
from djgeojson.fields import PointField
from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.gis.db import models as gismodels

class NewsPost(models.Model):
    title = models.CharField(max_length=350)
    city = models.CharField(max_length=100)
    tags = models.CharField(max_length=350)
    link = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    geom = PointField()
    objects = gismodels.GeoManager()


    @property
    def popupContent(self):
      return '<p>{}</p><p><{}</p>'.format(
          self.title,
          self.link)