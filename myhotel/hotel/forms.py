from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from .models import Employees


class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Файл")


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ['photo']
