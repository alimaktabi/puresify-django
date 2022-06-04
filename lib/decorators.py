from django.forms import Form
from django.http import HttpResponseNotAllowed, JsonResponse


def api_post(method):
    def wrapper(request, *args, **kwargs):
        if request.method != "POST":
            return HttpResponseNotAllowed(['GET', 'POST'])
        return method(request, *args, **kwargs)

    return wrapper


def validate_form(form: type(Form)):
    def wrap(callback):
        def wrapper(request, *args, **kwargs):
            form_data = form(data=request.POST)
            if not form_data.is_valid():
                return JsonResponse(form_data.errors, status=400)

            return callback(request, *args, **kwargs, cleaned_data=form_data.cleaned_data)

        return wrapper

    return wrap
