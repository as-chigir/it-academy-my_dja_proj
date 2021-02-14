from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.core.mail import send_mail

from . import constants
from . import forms
from . import models

# Create your views here.


def all_materials_(request):
    materials = models.Material.objects.all()
    return render(request, "materials/all_materials.html",
                  {"materials": materials})


def detailed_material(request, year, month, day, slug):
    material = get_object_or_404(models.Material,
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day,
                                 slug=slug)
    return render(request, "materials/detailed_material.html",
                  {'material': material})


def share_material(request, material_id):
    material = get_object_or_404(models.Material, id=material_id)
    sent = False
    if request.method == "POST":
        form = forms.EmailMaterialForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            material_uri = request.build_absolute_uri(
                material.get_absolute_url(),
            )
            subject = constants.SHARE_EMAIL_SUBJECT.format(
                cd['name'],
                material.title,
            )
            body = constants.SHARE_EMAIL_BODY.format(
                title=material.title,
                uri=material_uri,
                comment=cd['comment'],
            )
            send_mail(subject, body, 'admin@my.com', [cd['to_email'], ])
            sent = True

    else:
        form = forms.EmailMaterialForm()

    return render(request, 'materials/share.html',
                  {'material': material, 'form': form, 'sent': sent})
