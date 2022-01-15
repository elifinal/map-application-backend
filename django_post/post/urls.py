from django.urls import path
# from . import views
from .views import GeoModelDet, ClosestAreas
from rest_framework import routers

urlpatterns = [

    path('save/', GeoModelDet.as_view(), name="GeoModelDet"),
    path('posts/', GeoModelDet.as_view(), name="GeomodelDets"),
    path('places/', ClosestAreas.as_view(), name="ClosestAreas")
]
