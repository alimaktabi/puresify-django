from django.contrib.auth import authenticate, login, get_user_model
from django.http import JsonResponse
from django.shortcuts import redirect, render

from auth.forms import LoginForm, RegistrationForm
from lib.decorators import api_post, validate_form


User = get_user_model()


@api_post
@validate_form(LoginForm)
def login_callback(request, *, cleaned_data):

    user = authenticate(request, username=cleaned_data["phone_number"], password=cleaned_data["password"])

    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'logged in successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid username or password'}, status=401)


@api_post
@validate_form(RegistrationForm)
def register_callback(request, *, cleaned_data):
    user = User(
        phone_number=cleaned_data["phone_number"],
        first_name=cleaned_data["first_name"],
        last_name=cleaned_data["last_name"],
    )

    user.set_password(cleaned_data["password"])
    user.save()

    login(request, user)

    return JsonResponse({'success': 'User created successfully'}, status=201)



