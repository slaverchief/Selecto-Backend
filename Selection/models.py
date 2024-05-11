from django.db import models
from django.db.models import CheckConstraint, Q


class TGUser(models.Model):
    auth_id = models.IntegerField()


class Selection(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(TGUser, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name


class Char(models.Model):
    name = models.CharField(max_length=50)
    selection = models.ForeignKey(to='Selection', on_delete=models.CASCADE)
    priority = models.IntegerField()

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(priority__lte=10, priority__gte=1), name='priority_higher_1_less_10',
            ),
        ]

    def __str__(self):
        return self.name


class Option(models.Model):
    name = models.CharField(max_length=50)
    selection = models.ForeignKey(to=Selection, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class OptionChar(models.Model):
    value = models.FloatField()
    char = models.ForeignKey('Char', on_delete=models.CASCADE)
    option = models.ForeignKey('Option', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.option.name} | {self.char.name}'

    class Meta:
        verbose_name = 'Option char'
        verbose_name_plural = 'Option chars '
        unique_together = ('char', 'option',)

        constraints = [
            CheckConstraint(
                check=Q(value__lte=10, value__gte=1), name='char_value_higher_1_less_10',
            ),
        ]



# Create your models here.
