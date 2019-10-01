from django.urls import path

from profiles import views

urlpatterns = [
    path('api-view/',views.HellooApiView.as_view()),


]