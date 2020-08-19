from django.db import models

# Create your models here.


class ItemModel(models.Model):
    name = models.CharField(max_length=100)
    productname = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    stocknum = models.IntegerField()

    def __str__(self):
        return self.name
