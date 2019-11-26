from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from datamodel.models import Move

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')
        help_texts = {
            'username': None,
            'email': None,
        }
    def clean(self):
        username = self.cleaned_data['username']
        cleaned_data = self.cleaned_data
        #password_form = cleaned_data.get('password')
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists()==False:
           raise forms.ValidationError("Username/password is not valid|Usuario/clave no válidos")
        user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        if not user:
            raise forms.ValidationError("Username/password is not valid|Usuario/clave no válidos")
        return cleaned_data

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')
        help_texts = {
            'username': None,
        }
    def clean(self):
        username = self.cleaned_data['username']
        cleaned_data = self.cleaned_data
        password_form = cleaned_data.get('password')
        password2_form = cleaned_data.get('password2')
        if password_form != password2_form:
            raise forms.ValidationError('Password and Repeat password are not the same|La clave y su repetición no coinciden')
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
           raise forms.ValidationError("A user with that username already exists|Usuario duplicado")
        if len(password_form)<5:
           raise forms.ValidationError("This password is too short. It must contain at least 6 characters. This password is too common)")
        return cleaned_data



class MoveForm(forms.ModelForm):
    origin = forms.IntegerField()
    target = forms.IntegerField()
    class Meta:
        model = Move
        fields = ('origin', 'target',)











