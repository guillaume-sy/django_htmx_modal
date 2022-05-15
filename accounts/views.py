from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def authen(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have login'))
            return redirect('product_index')
        else:
            messages.success(request, ('Failed to login- Try again'))
            return redirect('authen')
    else:
        return render(request, "authen.html", {})


@login_required(login_url='/authen/')
def logout_user(request):
    logout(request)
    messages.success(request, ('You have logout'))
    return redirect('homepage')
