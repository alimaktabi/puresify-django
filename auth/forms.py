from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class RegistrationForm(forms.Form):
    password = forms.CharField(max_length=20)
    password_confirmation = forms.CharField(max_length=20)
    phone_number = forms.CharField(max_length=11)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")
        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number already exists")
        return phone_number


class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("phone_number")
        password = cleaned_data.get("password")

        if not User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("User does not exist")
        user = User.objects.get(phone_number=phone_number)

        if not user.check_password(password):
            raise forms.ValidationError("Incorrect password")
        return cleaned_data
