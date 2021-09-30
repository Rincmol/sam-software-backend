from django import forms
from django.forms import fields
from Sam.models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"