from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('checking')
        else:
            return render(request, 'authorization/login.html')

    if request.method == 'GET' and request.user.is_authenticated:
        return redirect('checking')

    return render(request, 'authorization/login.html')
