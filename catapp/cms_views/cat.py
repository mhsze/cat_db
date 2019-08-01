from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from wagtail.admin import messages

from catapp import forms, models


@login_required
def index(request):
    cats = models.Cat.objects.all()
    return render(request, "catapp/admin/cat_index.html", {"cats": cats})


@login_required
def add(request):
    if request.method == "POST":
        cat_form = forms.CatForm(request.POST)
        if cat_form.is_valid():
            cat_obj = cat_form.save(commit=False)
            cat_obj.save()
            messages.success(request, "Cat {} added.".format(cat_obj.name))
            return redirect("cat:index")
        else:
            messages.error(request, "Cat could not be saved due to errors")
    else:
        cat_form = forms.CatForm()

    return render(
        request, "catapp/admin/cat_add.html", {"cat_form": cat_form, "title": "Cat"}
    )


@login_required
def edit(request, cat_id):
    cat = get_object_or_404(models.Cat, id=cat_id)
    if request.method == "POST":
        form = forms.CatForm(request.POST, instance=cat)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.save()
            messages.success(request, "Cat {} updated.".format(cat.name))
            return redirect("cat:index")
        else:
            messages.error(request, "Cat could not be saved due to errors")
    else:
        form = forms.CatForm(instance=cat)

    return render(
        request,
        "catapp/admin/cat_add.html",
        {
            "cat_form": form,
            "form_action": reverse("cat:edit", args=[cat_id]),
            "title": "Update Cat",
            "del_action": reverse("cat:delete", args=[cat_id]),
        },
    )


@login_required
def delete(request, cat_id):
    if request.method == "POST":
        cat_obj = get_object_or_404(models.Cat, id=cat_id)
        cat_obj.delete()
        messages.success(request, "Cat {} deleted.".format(cat_obj.name))
        return redirect("cat:index")
    return HttpResponseNotAllowed(["POST"])
