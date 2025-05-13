from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from .forms import CustomUserCreationForm
import re
from django.conf import settings

# FR11 Login system
def login_user(request):
    
    """
    Handles user login.
    If the request method is POST, it authenticates the user with the provided credentials.
    If the credentials are valid, the user is logged in and redirected to the home page.
    Otherwise, an error message is displayed, and the user is redirected to the login page.
    """
    
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
    
# FR11 Logout system
def logout_user(request):
    """
    Handles user logout.
    Logs out the current user and redirects them to the home page with a success message.
    """
    django_logout(request)
    messages.success(request, "¡Cerraste sesión correctamente!")
    return redirect('home')

# FR12 Register system #(FR16) Moderation system  #
def register(request):
    """
    Handles user registration.
    If the request method is POST, it validates the form data and creates a new user.
    If the form is valid, the user is logged in and redirected to the home page with a success message.
    If the form is not valid, it displays the errors to the user within the registration card.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Offensive content validation
            username = form.cleaned_data.get('username', '').lower()

            # Check for prohibited words
            offensive_word_found = any(
                bad_word in username 
                for bad_word in settings.OFFENSIVE_WORDS
            )

            # Check for evasion patterns
            offensive_pattern_found = any(
                re.search(pattern, username, re.IGNORECASE)
                for pattern in settings.OFFENSIVE_PATTERNS
            )

            # If offensive content is found, add error to the username field
            if offensive_word_found or offensive_pattern_found:
                form.add_error('username', 'El nombre de usuario contiene lenguaje inapropiado. Por favor elige otro.')
            else:
                # If validation passes, save the user
                user = form.save()
                login(request, user)
                messages.success(request, "¡Te has registrado exitosamente!")
                return redirect('home')
        else:
            # If the form is not valid, errors will be displayed below fields
            messages.warning(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})
