from django.urls import path,include
from rest_framework.routers import DefaultRouter

from profiles import views

routers = DefaultRouter()
routers.register('hello-viewset',views.HelloViewset,base_name='hello-viewsets')
routers.register('Profile',views.UserProfileViewSet)


urlpatterns = [
    path('api-view/',views.HellooApiView.as_view()),
    path('login/',views.UserLoginApiView.as_view()),

    path('',include(routers.urls))


]