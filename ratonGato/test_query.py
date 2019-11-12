
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from datamodel.models import Game, GameStatus, Move
from datamodel import tests

class Test(TestCase):
    def setUp(self):
        self.users = []
        for name in ['cat_user_test', 'mouse_user_test']:
            self.users.append(self.get_or_create_user(name))

    @classmethod
    def get_or_create_user(cls, name, id=None):
        try:
            user = User.objects.get(username=name)
        except User.DoesNotExist:
            user = User.objects.create_user(username=name, password=name)
        return user

    @classmethod
    def get_array_positions(cls, game):
        return [game.cat1, game.cat2, game.cat3, game.cat4, game.mouse]



    def test1(self):
        def get_game_id(game):
            return game.id
        """ Comprobar si existe un usuario con id=10 y si no existe crearlo """
        try:
            user = User.objects.get(id=10)
        except User.DoesNotExist:
            user = User.objects.create_user(username="name1", password="name1", id=10)
            self.users.append(user)
        """ Comprobar si existe un usuario con id=11 y si no existe crearlo """
        try:
            user = User.objects.get(id=11)
        except User.DoesNotExist:
            user = User.objects.create_user(username="name2", password="name2", id=11)
            self.users.append(user)
        """ Crear  un  juego  y  asignarselo  al  usuario  con  id=10 """
        game = Game(cat_user=User.objects.get(id=10))
        #game.full_clean()
        game.save()
        """ Buscar todos los juegos con un solo usuario asignado """
        print(game)
        oneplayergames = []
        for item in Game.objects.all():
            if item.cat_user != None:
                if item.mouse_user == None:
                    oneplayergames.append(item)
            else:
                if item.mouse_user != None:
                    oneplayergames.append(item)
        print(oneplayergames)
        """ Unir al usuario con id=11 al juego con menor id encontrado en el paso anterior y comenzar la partida """
        oneplayergames.sort(key=get_game_id)
        game = oneplayergames[0]
        game.mouse_user = User.objects.get(id=11)
        game.save()
        print(game)
        """ En la partida seleccionada, mover el segundo gato pasandolo de la posicion 2a la 11 """
        Move.objects.create(game=game, player=User.objects.get(id=10), origin=2, target=11)
        print(game)
        """ En la partida seleccionada, mover el raton de la posicion 59 a la 52 """
        Move.objects.create(game=game, player=User.objects.get(id=11), origin=59, target=52)
        print(game)
        """
        game = Game(cat_user=user)
        game.full_clean()
        game.save()
        self.assertEqual(game.cat_user.id, 10)
        self.assertIsNone(game.mouse_user)
        """
