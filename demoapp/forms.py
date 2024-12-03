from django import forms
from .models import Visitor

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['name', 'email', 'phone', 'favorite_thing_to_cook', 'additional_comments']
        exclude = ['created_by']
