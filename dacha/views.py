from django.shortcuts import render
from . import models

# Create your views here.


def all_materials(request):
    all_materials = models.Material.objects.all()
    return render(request, 'materials/all_materials.html',
                  {'materials': all_materials})