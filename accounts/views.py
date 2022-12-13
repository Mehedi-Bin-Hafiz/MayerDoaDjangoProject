from django.shortcuts import render

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout


def owner_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_superuser:
                return redirect('admin:index')
            login(request, user)
            return render(request, 'options.html')
        else:
            return render(request, 'login.html', {'error_message': 'Incorrect username or password.'})
    else:
        return render(request, 'login.html')



def owner_logout(request):
    logout(request)
    return redirect('accounts:ownerLogin')