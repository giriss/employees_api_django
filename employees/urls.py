from django.urls.conf import path

from . import views

urlpatterns = [
    path('', views.index),
    path('<int:pk>/', views.resource),
    path('<int:pk>/picture/', views.picture),
]
