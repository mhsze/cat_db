from django import forms
from wagtail.admin.widgets import AdminDateInput

from catapp import models


class HomeForm(forms.ModelForm):
    class Meta:
        model = models.Home
        fields = ["name", "address", "type"]


class CatForm(forms.ModelForm):
    class Meta:
        model = models.Cat
        fields = ["name", "gender", "date_of_birth", "description", "breed", "owner"]
        widgets = {"date_of_birth": AdminDateInput()}
