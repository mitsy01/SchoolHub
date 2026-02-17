from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile, Action, Position, Subject


class UserForm(UserCreationForm):
    username = forms.CharField(max_length=50, min_length=2, help_text="Введіть логін", label="Логін")
    first_name = forms.CharField(min_length=2, max_length=50, help_text="Введіть ім'я")
    last_name = forms.CharField(max_length=100, min_length=2, help_text="Введіть прізвище", label="Прізвище")
    email = forms.EmailField(required=False, help_text="Введіть адресу електроню пошти")
    password1 = forms.CharField(help_text="Введіть свій пароль", label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(help_text="Повторіть пароль", label="Підтвердити пароль", widget=forms.PasswordInput)
    
    class Meta: 
        model = User
        fields = ["username","first_name", "last_name", "email", "password1", "password2"]

        
class UserFormEdit(forms.ModelForm):
    username = forms.CharField(
        max_length=50,
        min_length=2,
        widget=forms.TextInput(attrs={"placeholder": "Введіть логін"})
    )
    first_name = forms.CharField(
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Введіть ім'я"})
    )
    last_name = forms.CharField(
        max_length=100,
        min_length=2,
        widget=forms.TextInput(attrs={"placeholder": "Введіть прізвище"})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"placeholder": "Введіть email"})
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

        
        
class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = "__all__"
        
        
class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = "__all__"
        
        
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"
        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ["user", "positions", "classroom"]
        widgets = {
            "phone_number": forms.TextInput(attrs={"placeholder": "Введіть номер телефону", "class": "form-control"}),
            "bio": forms.Textarea(attrs={"placeholder": "Про себе", "class": "form-control"}),
            "avatar": forms.FileInput(attrs={"class": "form-control"})
        }

        

class SignInForm(forms.Form):
    username = forms.CharField(max_length=50, min_length=2, help_text="Введіть логін", label="Логін")
    password = forms.CharField(
        help_text="Введіть свій пароль",
        label="Пароль",
        widget=forms.PasswordInput,
        )