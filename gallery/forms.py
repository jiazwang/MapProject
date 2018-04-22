from django import forms
from django.contrib.auth.models import User

from .models import Collection, Picture


class CollectionForm(forms.ModelForm):

    class Meta:
        model = Collection
        fields = ['artist', 'collection_title', 'format', 'collection_logo']


class PictureForm(forms.ModelForm):

    class Meta:
        model = Picture
        fields = ['picture_title', 'picture_file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
