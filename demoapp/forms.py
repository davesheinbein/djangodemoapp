from django import forms
from .models import Visitor
from django.contrib.auth.forms import AuthenticationForm

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['name', 'email', 'phone', 'favorite_thing_to_cook', 'additional_comments']
        exclude = ['created_by']

class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)
