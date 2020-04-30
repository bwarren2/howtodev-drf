from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=255)


class Employee(models.Model):
    name = models.CharField(max_length=255)
    teams = models.ManyToManyField('Team')


class Snack(models.Model):
    owner = models.ForeignKey('Employee', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
