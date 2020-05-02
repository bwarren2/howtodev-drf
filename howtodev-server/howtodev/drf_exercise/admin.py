"Exercise admin"

from django.contrib import admin
from drf_exercise import models

admin.site.register(models.Employee)
admin.site.register(models.Team)
admin.site.register(models.Snack)
