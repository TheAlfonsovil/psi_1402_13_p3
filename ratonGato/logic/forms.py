from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')
        help_texts = {
            'username': None,
            'email': None,
        }

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    repeat_password = forms.CharField(widget=forms.PasswordInput())
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
        repeat_password_form = cleaned_data.get('repeat_password')
        if password_form != repeat_password_form:
            raise forms.ValidationError('Password and Repeat password are not the same|La clave y su repetición no coinciden')
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
           raise forms.ValidationError("A user with that username already exists|Usuario duplicado")
        if len(password_form)<5:
           raise forms.ValidationError("This password is too short. It must contain at least 6 characters.")
        return cleaned_data

#class Move_Form(forms.ModelForm):
#    origin = forms.CharField(widget=forms.C())
#    target = forms.CharField(widget=forms.PasswordInput())
#    class Meta:
#        model = User
#        fields = ('username', 'password')
