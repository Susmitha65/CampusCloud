from django.urls import path
from . import views

app_name = 'result_analysis'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
]
