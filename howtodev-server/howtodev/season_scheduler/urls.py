from rest_framework import routers
from season_scheduler import apiviews

router = routers.DefaultRouter()
router.register(r'seasons', apiviews.SeasonViewSet, basename='students')

urlpatterns = router.urls
