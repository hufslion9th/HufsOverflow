from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import StackoverflowUser


class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=254, help_text='필수입니다. 유효한 이메일 주소를 알려주십시오.')

    class Meta:
        model = StackoverflowUser
        fields = ('username', 'name', 'email', 'password1', 'password2',)
