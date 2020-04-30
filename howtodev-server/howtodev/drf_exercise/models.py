"Some toy models"

from django.db import models


class Team(models.Model):
    "A group of Employees."
    name = models.CharField(max_length=255)


class Employee(models.Model):
    "A person working at a fake company."
    name = models.CharField(max_length=255)
    teams = models.ManyToManyField('Team')


class Snack(models.Model):
    "A consumable owned by an employee."

    owner = models.ForeignKey('Employee', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
