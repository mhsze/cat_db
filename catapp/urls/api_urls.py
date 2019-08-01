from django.conf.urls import include, re_path
from rest_framework.routers import DefaultRouter

from ..views import BreedViewSet, CatViewSet, HomeViewSet, HumanViewSet

router = DefaultRouter()
router.register(r"home", HomeViewSet)
router.register(r"human", HumanViewSet)
router.register(r"breed", BreedViewSet)
router.register(r"cat", CatViewSet)

urlpatterns = [re_path("^", include(router.urls))]
