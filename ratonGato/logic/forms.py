from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ('username', 'password')

class UserRegister(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_again = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')

#class Move_Form(forms.ModelForm):
#    origin = forms.CharField(widget=forms.C())
#    target = forms.CharField(widget=forms.PasswordInput())
#    class Meta:
#        model = User
#        fields = ('username', 'password')
