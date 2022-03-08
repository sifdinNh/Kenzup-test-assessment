from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User


# Register your models here.
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirmation de mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username','first_name','last_name','balance')

    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("les mots de passe no correspondent pas")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = User
        fields = ('email','last_name','first_name','balance', 'password', 'is_active', 'is_superuser', 'is_staff')

    def clean_password(self):
        return self.initial["password"]