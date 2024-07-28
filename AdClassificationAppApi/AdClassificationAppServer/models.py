from django.db import models


class History(models.Model):
    datetime = models.CharField(max_length=10)
    input_string = models.CharField(max_length=100)
    output = models.CharField(max_length=15)
    objects = models.Manager()
