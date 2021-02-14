from django.urls import path
from . import views


app_name = 'dacha'

urlpatterns = [
    path('', views.all_materials_, name='all_materials_'),
    path('<int:year>/'
         '<int:month>/'
         '<int:day>/'
         '<slug:slug>/',
         views.detailed_material, name='detailed_material'),
    path('<int:material_id>/'
         'share/',
         views.share_material, name='share_material'),
]
