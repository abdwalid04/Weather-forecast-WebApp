from typing import ByteString
from xml.parsers.expat import model
from django.db import models
from django.contrib.auth.models import User
from django.forms import IntegerField


from distutils.command.upload import upload
from email.policy import default
from types import BuiltinMethodType
from django.db import models
from django.db.models.fields import SlugField
from django.contrib.auth.models import User
from sklearn import metrics, preprocessing

class observation(models.Model):
    observation_id = models.AutoField(primary_key=True)
    id_ville = models.IntegerField()
    nom = models.CharField(max_length=40)
    lat = models.FloatField()
    lon = models.FloatField()
    date = models.DateField()
    ech = models.IntegerField()
    t2m = models.FloatField()
    hu2m = models.FloatField()
    hu10m = models.FloatField()
    hu1000hpa = models.FloatField()
    hu925hpa = models.FloatField()
    hu850hpa = models.FloatField()
    hu700hpa = models.FloatField()
    hu500hpa = models.FloatField()
    hu300hpa = models.FloatField()
    u10ff = models.FloatField()
    u10dd = models.FloatField()
    u10ddd = models.CharField(max_length=5)
    u20ff = models.FloatField()
    u20dd = models.FloatField()
    u20ddd = models.CharField(max_length=5)
    u50ff = models.FloatField()
    u50dd = models.FloatField()
    u50ddd = models.CharField(max_length=5)
    u100ff = models.FloatField()
    u100dd = models.FloatField()
    u100ddd = models.CharField(max_length=5)
    cape = models.FloatField()
    psol = models.FloatField()
    ch = models.FloatField()
    cm = models.FloatField()
    cl = models.FloatField()
    rr = models.FloatField()
    rr_gn = models.FloatField()
    rr_cv = models.FloatField()
    rr_sn = models.FloatField()
    vcty = models.FloatField()
    tn = models.FloatField()
    tx = models.FloatField()
    gtn = models.FloatField()
    gtx = models.FloatField()

class nebulosite(models.Model):
    nebulosite_id = models.AutoField(primary_key=True)
    nebulosite = models.CharField(max_length=200,unique=True)

class prevision(models.Model):
    observation = models.OneToOneField(observation, on_delete=models.CASCADE,primary_key=True)
    nebulosite = models.ForeignKey(nebulosite, on_delete=models.CASCADE)

class validation(models.Model):
    prevision = models.OneToOneField(prevision, on_delete=models.CASCADE,primary_key=True)
    nebulosite = models.ForeignKey(nebulosite, on_delete=models.CASCADE)
    valideur = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
