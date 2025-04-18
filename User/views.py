from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from .forms import CustomUserCreationForm

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Has iniciado sesión correctamente.")
            return redirect('home')
        else:
            
            messages.error(request, "Hubo un error al iniciar sesión, intenta de nuevo.")  
            return redirect('login')    
    else:
        return render(request, "login.html")

def logout_user(request):
    django_logout(request)
    messages.success(request, "¡Cerraste sesión correctamente!")
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Te has registrado exitosamente!")
            return redirect('home')
        else:
            # if the form is not valid, show the errors to the user
            messages.warning(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})
