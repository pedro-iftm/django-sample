from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.conf import settings

def register(request):
    template_name = 'register.html'
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_REDIRECT_URL)

    context = {'form':  form}

    return render(request, template_name, context)