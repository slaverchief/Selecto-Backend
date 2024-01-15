from django.db import models


class Selection(models.Model):
    name = models.CharField(max_length=50)


class Char(models.Model):
    name = models.CharField(max_length=50)
    selection = models.ForeignKey(to='Selection', on_delete=models.CASCADE)
    priority = models.IntegerField()


class Option(models.Model):
    name = models.CharField(max_length=50)


class OptionChar(models.Model):
    value = models.FloatField()
    char = models.ForeignKey('Char', on_delete=models.CASCADE)
    option = models.ForeignKey('Option', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Option char'
        verbose_name_plural = 'Option chars '

# Create your models here.
