from django import forms
from .models import Visitor, Profile, Article, Tag, Category, Author, Book
from django.contrib.auth.forms import AuthenticationForm

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['name', 'email', 'phone', 'favorite_thing_to_cook', 'additional_comments']
        exclude = ['created_by']

class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'tags']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'publication_date']
