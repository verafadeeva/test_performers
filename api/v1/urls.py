from django.urls import include, path
from rest_framework import routers
from api.v1 import views

app_name = 'api_v1'

router = routers.DefaultRouter()
router.register(r'singers', views.SingerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
