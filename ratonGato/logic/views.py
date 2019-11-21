from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from datamodel import constants
from logic.forms import UserForm, UserRegister
from django.contrib.auth import logout

# COMPROBAR AQUI COMO SON LAS FUNCIONES ->
# https://psi1920-p3.herokuapp.com/mouse_cat/
 
def index(request):
    context_dict = {}
    return render(request, 'mouse_cat/index.html', context_dict)

def anonymous_required(f):
    def wrapped(request):
        if request.user.is_authenticated:
            return HttpResponseForbidden(errorHTTP(request, exception="..."))
        else:
            return f(request)
    return wrapped


def errorHTTP(request, exception=None):
    context_dict = {}
    context_dict[constants.ERROR_MESSAGE_ID] = exception
    return render(request, "mouse_cat/error.html", context_dict)



@anonymous_required
def login_service(request):
    if request.method == 'POST': #Tras clicar el boton de submit
        #recuepra datos
        username = request.POST.get('username')
        password = request.POST.get('password')
        #autentica
        user = authenticate(username=username, password=password)
        if user: #Existe
            if user.is_active:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            user_form = UserForm()
            context_dict = {'user_form': user_form,'error': True}
            return render(request,"mouse_cat/login.html", context_dict)
    else: #Si no se ha pulsado boton
        user_form = UserForm()
        context_dict = {'user_form': user_form,'error': False}
        return render(request,"mouse_cat/login.html", context_dict)

@login_required(redirect_field_name='',login_url='../')
def logout_service(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    context_dict = {}
    return render(request,"mouse_cat/logout.html", context_dict)
    

@anonymous_required
def signup_service(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            #user = authenticate(username=username, password=password)
            login(request, user)
            context_dict = {}
            return render(request,"mouse_cat/signup.html", context_dict)
        else:
            print(user_form.errors)
    else:
        user_form = UserRegister()
        context_dict = {'user_form': user_form}
        return render(request,"mouse_cat/signup.html", context_dict)


def counter_service(request):
    context_dict = {}
    return render(request,"mouse_cat/counter.html", context_dict)


def create_game_service(request):
    context_dict = {}
    return render(request,"mouse_cat/new_game.html", context_dict)


def join_game_service(request):
    context_dict = {}
    return render(request,"join_game.html", context_dict)


def select_game_service(request):
    context_dict = {}
    return render(request,"select_game.html", context_dict)


def show_game_service(request):
    context_dict = {}
    return render(request,"game.html", context_dict)

def move_service(request):
    context_dict = {}
    return render(request,"game.html", context_dict)











