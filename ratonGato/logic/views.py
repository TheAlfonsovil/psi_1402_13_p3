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
from logic.forms import UserForm, SignupForm
from django.contrib.auth import logout
from datamodel.models import Game, GameStatus, Move
from django.core.files import File
import json

# COMPROBAR AQUI COMO SON LAS FUNCIONES ->
# https://psi1920-p3.herokuapp.com/mouse_cat/
 
def index(request):
    context_dict = {}
    return render(request, 'mouse_cat/index.html', context_dict)

def anonymous_required(f):
    def wrapped(request):
        if request.user.is_authenticated:
            return HttpResponseForbidden(errorHTTP(request, exception="403"))
        else:
            return f(request)
    return wrapped


def errorHTTP(request, exception=None):
    context_dict = {}
    context_dict['msg_error']="Action restricted to anonymous users|Servicio restringido a usuarios anónimos"
    context_dict[constants.ERROR_MESSAGE_ID] = exception
    return render(request, "mouse_cat/error.html", context_dict)



@anonymous_required
def login_service(request):
    if request.method == 'POST': #Tras clicar el boton de submit
        user_form = UserForm(data=request.POST)
        #recuepra datos
        username = request.POST.get('username')
        password = request.POST.get('password')
        #autentica
        if user_form.is_valid():
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
        else:
            context_dict = {'user_form': user_form}
            return render(request,"mouse_cat/login.html", context_dict)
    else: #Si no se ha pulsado boton
        user_form = UserForm()
        context_dict = {'user_form': user_form}
        return render(request,"mouse_cat/login.html", context_dict)

@login_required(redirect_field_name='',login_url='../')
def logout_service(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    context_dict = {'user': "user"}
    return render(request,"mouse_cat/logout.html", context_dict)
    

@anonymous_required
def signup_service(request):
    if request.method == 'POST':
        user_form = SignupForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            #user = authenticate(username=username, password=password)
            login(request, user)
            context_dict = {}
            return render(request,"mouse_cat/signup.html", context_dict)
        else:
            context_dict = {'user_form': user_form}
            return render(request,"mouse_cat/signup.html", context_dict)
    else:
        user_form = SignupForm()
        context_dict = {'user_form': user_form}
        return render(request,"mouse_cat/signup.html", context_dict)


def counter_service(request):
	
    context_dict = {}
    return render(request,"mouse_cat/counter.html", context_dict)

@login_required(redirect_field_name='',login_url='../login_service')
def create_game_service(request):
    game = Game(cat_user=request.user)
    game.save()
    context_dict = {'game': game}
    return render(request,"mouse_cat/new_game.html", context_dict)

@login_required(redirect_field_name='',login_url='../login_service')
def join_game_service(request):
    games = Game.objects.order_by('id')
    for game_aux in reversed(games):
        if game_aux.status == 0:
            game = game_aux #Created
            break
    game.mouse_user = request.user
    game.status = 1 #Active
    game.save()
    context_dict = {'game': game}
    return render(request,"mouse_cat/join_game.html", context_dict)

@login_required(redirect_field_name='',login_url='../login_service')
def select_game_service(request, game_id = -1):
    if request.method == 'GET':  
        if game_id == -1:
            as_cat = Game.objects.filter(cat_user = request.user, status=GameStatus.ACTIVE)
            as_mouse = Game.objects.filter(mouse_user = request.user, status=GameStatus.ACTIVE)
            context_dict = {}
            context_dict['as_cat'] = as_cat
            context_dict['as_mouse'] = as_mouse
            return render(request,"mouse_cat/select_game.html", context_dict)
        request.session['game_id'] = game_id
       	return redirect(reverse('show_game'))
    else:
        #POST request redirect
        #game_id = request.POST.get('game.id')
        request.session['game_id'] = game_id
        context_dict = {'game_id': game_id}
        return render(request,"mouse_cat/game.html", context_dict)

@login_required(redirect_field_name='',login_url='../login_service')
def show_game_service(request):
    game_id = request.session['game_id']
    games = Game.objects.order_by('id')
    gamef = {}
    print(game_id)
    print(request.user)
    print(request.user.id)
    for game in games:
        if game.id == game_id:
            gamef = game
            break
    print(gamef)
    board = [0] * 64
    board[game.cat1] = 1
    board[game.cat2] = 1
    board[game.cat3] = 1
    board[game.cat4] = 1
    board[game.mouse] = -1
    context_dict = {'game': gamef, 'board': board}
    return render(request,"mouse_cat/game.html", context_dict)

@login_required(redirect_field_name='',login_url='../login_service')
def move_service(request):
    if request.method == 'POST':
        print(request)
        games = Game.objects.order_by('id')
        for game in games:
            if game.cat_user.id == request.user.id:
	            gamef = game
	            break
        move = Move.objects.create(game=gamef, player=request.user, origin=request.form[0], target=request.form[1])
        move.save()
        context_dict = {'game': gamef, 'move_form': MoveForm()}
        return render(request,"mouse_cat/game.html", context_dict)
    else:
        context_dict = {}
        return render(request,"mouse_cat/game.html", context_dict)
#dos cadenas de caracteres con el nombre del usuario y su clav
# jugador, juego, posici ́on inicial y final del movimient









