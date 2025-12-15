from django.urls import path
from . import views

app_name = 'translator'

urlpatterns = [
    path('', views.index, name='index'),
    path('translate/', views.translate, name='translate'),
    path('success/<str:filename>/', views.success, name='success'),
    path('download/<str:filename>/', views.download, name='download'),
]

