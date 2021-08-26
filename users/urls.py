from django.urls.conf import path

from . import views

urlpatterns = [
    path('', views.create),
    path('login/', views.login)
]
