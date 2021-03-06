from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import authenticate, login
from courses.models import Enrollment
from .forms import RegisterForm, EditAccountForm


@login_required
def dashboard(request):
    template_name = 'dashboard.html'
    return render(request, template_name, {})


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


@login_required
def edit(request):
    template_name = 'edit.html'
    form = EditAccountForm()
    context = {}
    
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Os dados da sua conta foram alterados com sucesso')
            return redirect('/contas')
    
    else:
        form = EditAccountForm(instance=request.user)
    
    context['form'] = form
    return render(request, template_name, context)


@login_required
def edit_password(request):
    template_name = 'edit_password.html'
    context = {}

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            context['success'] = True
    
    else:
        form = PasswordChangeForm(user=request.user)
    
    context['form'] = form
    return render(request, template_name, context) 
