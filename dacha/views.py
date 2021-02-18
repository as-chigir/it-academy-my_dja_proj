from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.core.mail import send_mail

from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.contrib.auth import login

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

#  from django.views.generic import ListView

from . import constants
from . import forms
from . import models

# Create your views here.


def all_materials_(request):
    materials = models.Material.objects.all()
    return render(request, "materials/all_materials.html",
                  {"materials": materials})


# class MaterialListView(LoginRequiredMixin, ListView):
#     queryset = models.Material.objects.all()
#     context_object_name = 'materials'
#     template_name = "materials/all_materials.html"


@login_required
def detailed_material(request, year, month, day, slug):
    material = get_object_or_404(models.Material,
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day,
                                 slug=slug)
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.material = material
            comment.save()
            return redirect(material)
    else:
        form = forms.CommentForm(request.POST)

    return render(request, "materials/detailed_material.html",
                  {'material': material,
                   'form': form})


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


def create_form(request):
    if request.method == "POST":
        material_form = forms.MaterialForm(request.POST)
        if material_form.is_valid():
            new_material = material_form.save(commit=False)
            new_material.author = User.objects.first()
            new_material.slug = new_material.title.replace(" ", "-")
            new_material.save()
            return render(request,
                          'materials/detailed_material.html',
                          {"material": new_material})
    else:
        material_form = forms.MaterialForm()
        return render(request,
                      'materials/create.html',
                      {'form': material_form})


def custom_login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                usermane=cd['username'],
                password=cd['password'],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('User was logged init')
                else:
                    return HttpResponse('User not active')
            else:
                return HttpResponse('bad credentials')
    else:
        form = forms.LoginForm()
        return render(request, 'login.html', {'form': form})


@login_required
def view_profile(request):
    return render(request, 'profile.html', {'user': request.user})
