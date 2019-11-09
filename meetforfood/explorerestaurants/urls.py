from django.urls import path,include
from rest_framework.routers import DefaultRouter

from explorerestaurants import views

routers = DefaultRouter()
routers.register('restaurants',views.RestaurantInfoViewSet)
routers.register('menu',views.MenuInfoViewSet)



urlpatterns = [
    path('',include(routers.urls))


]