from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    no = models.IntegerField()
    userType = models.BooleanField()
    age = models.IntegerField()
    password = models.CharField(max_length=100)
    bgType = models.CharField(max_length=2)
    rhValue = models.BooleanField()

    def __str__(self):
        return self.name



