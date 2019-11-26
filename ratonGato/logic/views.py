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
from logic.forms import UserForm, SignupForm, MoveForm
from django.contrib.auth import logout
from datamodel.models import Game, GameStatus, Move, CounterManager, Counter
from django.core.files import File
import json

# COMPROBAR AQUI COMO SON LAS FUNCIONES ->
# https://psi1920-p3.herokuapp.com/mouse_cat/
 
# Variables auxiliares para counter_service
c_gbl = 1
c_ses = 1

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
                    return HttpResponse("Your account is disabled.")
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
    global c_ses
    context_dict = {'user': request.user}
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    c_ses = 1
    # Take the user back to the homepage.   
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
    global c_gbl
    global c_ses
   
    # Counter.objects.all().delete()
    counter_session = c_ses  # Counter.objects.create(value=c_ses)
    counter_global = c_gbl # Counter.objects.create(value=c_gbl)
    c_gbl = c_gbl + 1
    c_ses = c_ses + 1
    context_dict = {'counter_session': counter_session, 'counter_global': counter_global}
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
    no_game_flag = 0
    context_dict = {}
    for game_aux in reversed(games):
        if game_aux.status == 0 and game_aux.cat_user != request.user:
            game = game_aux # 0 = Created
            no_game_flag = 1
            break
    if no_game_flag == 0:
        context_dict['msg_error'] = "There is no available games"
        return render(request,"mouse_cat/join_game.html", context_dict)
    game.mouse_user = request.user
    game.status = 1 # 1 = Active
    game.save()
    context_dict['game'] = game
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

        else: #lo que creiamos que era un post se ejecuta aqui como get
            request.session['game_id'] = game_id
            context_dict = {'game_id': game_id} 
            return show_game_service(request)
           	
    else:
        #POST
        request.session['game_id'] = game_id
        context_dict = {'game_id': game_id}       
        return redirect(reverse('show_game'))
        return render(request,"mouse_cat/game.html", context_dict)


@login_required(redirect_field_name='',login_url='../login_service')
def show_game_service(request):
    try:
        game_id = request.session['game_id']
    except:
        context_dict = {'msg_error': "No game selected"}
        return render(request,"mouse_cat/error.html", context_dict)
    
    games = Game.objects.order_by('id')
    gamef = {}
    for game in games:
        if game.id == game_id:
            gamef = game
            break
    board = [0] * 64
    board[game.cat1] = 1
    board[game.cat2] = 1
    board[game.cat3] = 1
    board[game.cat4] = 1
    board[game.mouse] = -1
    move_form = MoveForm()
    context_dict = {'game': gamef, 'board': board, 'move_form': move_form}
    return render(request,"mouse_cat/game.html", context_dict)

@login_required(redirect_field_name='',login_url='../login_service')
def move_service(request):
    if request.method == 'POST':
        move_form = MoveForm(data=request.POST)
        move_origin = int(request.POST.get('origin'))
        move_target = int(request.POST.get('target'))
        games = Game.objects.order_by('id')

        for game in games:
            if game.id == request.session['game_id']:
                gamef = game
                break    
        try:    
            move = Move.objects.create(game = gamef, player = request.user, origin = move_origin, target = move_target)
        except:
            return show_game_service(request)  
        return show_game_service(request)  
    else:
        return show_game_service(request)  







