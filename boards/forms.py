from django import forms
from . import models


class BoardCreateForm(forms.ModelForm):
    class Meta:
        model = models.Board
        fields = ("description",)
