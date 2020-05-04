"URLconf for exercise"

from django.urls import include, path
from rest_framework_nested import routers
from . import apis

router = routers.DefaultRouter()
router.register('employees', apis.EmployeeModelViewSet)
router.register('snacks', apis.SnackModelViewSet)

subsnacks_router = routers.NestedDefaultRouter(router, 'employees', lookup='employee')
subsnacks_router.register('snacks', apis.SubSnackModelViewSet, basename='employee-snacks')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(subsnacks_router.urls)),
]
