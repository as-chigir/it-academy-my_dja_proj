from django.shortcuts import render, get_object_or_404
from . import models

# Create your views here.


def all_materials_(request):
    materials = models.Material.objects.all()
    return render(request, 'materials/all_materials.html',
                  {'materials': materials})


def detailed_material(request, year, month, day, slug):
    materials = get_object_or_404(models.Material,
                                  publish__year=year,
                                  publish__month=month,
                                  publish__day=day,
                                  slug=slug)
    return render(request, 'materials/detailed_materials.html',
                  {'materials': materials})
