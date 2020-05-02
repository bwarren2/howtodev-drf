"URLconf for exercise"

from django.urls import include, path
from rest_framework import routers
from . import apis

router = routers.DefaultRouter()
router.register('employees', apis.EmployeeModelViewSet)

urlpatterns = [
    path('', include(router.urls))
]
