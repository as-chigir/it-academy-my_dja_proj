from django.urls import path
from . import views


app_name = 'dacha'

urlpatterns = [
    path('', views.all_materials, name='all_materials'),
]
