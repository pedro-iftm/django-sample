from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from .forms import RegisterForm


def register(request):
    template_name = 'register.html'
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('/')

    context = {'form':  form}

    return render(request, template_name, context)
