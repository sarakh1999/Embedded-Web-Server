from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models


class FileUploadForm(forms.Form):
    file_field = forms.FileField(
        required=True,
    )