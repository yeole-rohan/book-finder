from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from . import forms


@login_required(login_url="/user/login/")
def profile(request):
    if request.method =="POST":
        form = forms.ShopProfileForm(request.POST or None, instance=request.user)
        if form.is_valid():
            form = form.save()
            return redirect('user:profile')
    else:
        form = forms.ShopProfileForm(instance=request.user)
    return render(request, "profile.html", {'form' :form})

def shopLogin(request):
    if request.user.is_authenticated:
        return redirect("search:search")
    if request.method == "POST":
        loginForm = AuthenticationForm(request, data=request.POST or None)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("search:search")
        # else:
        #     print(loginForm.errors)
        #     messages.error(request, "Credentials are not valid.")
    else:
        loginForm = AuthenticationForm()
    return render(request, "login.html", {'form': loginForm})

def register(request):
    if request.user.is_authenticated:
        return redirect("search:search")
    if request.method =="POST":
        form = forms.SignupForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            username = request.POST.get('username')
            password = request.POST.get('password1')
            form.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('search:search')
            else:
                return redirect('user:shopLogin')
    else:
        form = forms.SignupForm()
    return render(request, "register.html", {'form' :form})