from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=100)
    email        = models.CharField(max_length=250, unique=True)
    password     = models.CharField(max_length=300)
    class Meta:
        db_table = 'users'
