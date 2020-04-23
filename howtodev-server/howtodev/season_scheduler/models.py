from django.db import models


class Season(models.Model):

    display_name = models.CharField(max_length=200)
    start_dt = models.DateField()
    start_end = models.DateField()
