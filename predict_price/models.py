from django.db import models

# Create your models here.

class Apartment(models.Model):
    gu = models.CharField(max_length=200)
    dong = models.CharField(max_length=200)
    sell = models.IntegerField(default=0)
    size = models.FloatField(default=0.0)
    floor = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    cstr_date = models.IntegerField(default=0)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Dong(models.Model):
    dong = models.CharField(max_length=200)

    def __str__(self):
        return self.dong