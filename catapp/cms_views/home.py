from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from wagtail.admin import messages

from catapp import forms, models


@login_required
def index(request):
    homes = models.Home.objects.all()
    return render(request, "catapp/admin/home_index.html", {"homes": homes})


@login_required
def add(request):
    if request.method == "POST":
        home_form = forms.HomeForm(request.POST)
        if home_form.is_valid():
            home_obj = home_form.save(commit=False)
            home_obj.save()
            messages.success(request, "Home {} added.".format(home_obj.name))
            return redirect("cathome:index")
        else:
            messages.error(request, "Home could not be saved due to errors")
    else:
        home_form = forms.HomeForm()

    return render(
        request, "catapp/admin/home_add.html", {"home_form": home_form, "title": "Home"}
    )


@login_required
def edit(request, home_id):
    home = get_object_or_404(models.Home, id=home_id)
    if request.method == "POST":
        form = forms.HomeForm(request.POST, instance=home)
        if form.is_valid():
            home = form.save(commit=False)
            home.save()
            messages.success(request, "Home {} updated.".format(home.name))
            return redirect("cathome:index")
        else:
            messages.error(request, "Home could not be saved due to errors")
    else:
        form = forms.HomeForm(instance=home)

    return render(
        request,
        "catapp/admin/home_add.html",
        {
            "home_form": form,
            "form_action": reverse("cathome:edit", args=[home_id]),
            "title": "Update Home",
            "del_action": reverse("cathome:delete", args=[home_id]),
        },
    )


@login_required
def delete(request, home_id):
    if request.method == "POST":
        home_obj = get_object_or_404(models.Home, id=home_id)
        home_obj.delete()
        messages.success(request, "Home {} deleted.".format(home_obj.name))
        return redirect("cathome:index")
    return HttpResponseNotAllowed(["POST"])
