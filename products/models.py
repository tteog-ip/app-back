from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=20)
    class Meta:
        db_table='regions'

class Location(models.Model):
    name = models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    class Meta:
        db_table='locations'

class Type(models.Model):
    name = models.CharField(max_length=20)
    class Meta:
        db_table = 'types'

class AptStatus(models.Model):
    status = models.CharField(max_length=20)
    class Meta:
        db_table = 'apt_status'

class Apt(models.Model):
    name         = models.CharField(max_length=300)
    address        = models.CharField(max_length=300)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    thumbnail_image_url = models.URLField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    open_date = models.DateTimeField()
    quantity = models.IntegerField()
    area = models.IntegerField()
    status = models.ForeignKey(AptStatus, on_delete=models.CASCADE)
    class Meta:
        db_table='apt'
    
class Image(models.Model):
    url       = models.URLField(max_length=300)
    apt   = models.ForeignKey(Apt, on_delete=models.CASCADE)
    class Meta:
        db_table='images'
