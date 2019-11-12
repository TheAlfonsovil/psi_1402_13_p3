from __future__ import unicode_literals
from datetime import datetime
import django
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
"""
class User(models.Model):

    username = models.CharField(unique=True, max_length=128)
    password = models.CharField(unique=True, max_length=128)

    def save(self, *arg, **kwargs):
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self #mirar en los test de models como se imprime
"""
class GameStatus():
	CREATED = 0
	ACTIVE = 1
	FINISHED = 2
	STATUS = {0: "Created",
			1: "Active",
			2: "Finished",
			}
class Game(models.Model):
    cat_user = models.ForeignKey(User, null=False, related_name='games_as_cat', on_delete=models.CASCADE)
    mouse_user = models.ForeignKey(User,blank=True, null=True, related_name='games_as_mouse', on_delete=models.CASCADE)
    cat1 = models.IntegerField(null=False, default=0)
    cat2 = models.IntegerField(null=False, default=2)
    cat3 = models.IntegerField(null=False, default=4)
    cat4 = models.IntegerField(null=False, default=6)
    mouse = models.IntegerField(null=False, default=59)
    cat_turn = models.BooleanField(null=False, default=True)
    status = models.IntegerField(null=False, default=GameStatus.CREATED)
    #sin implementar -- solved creo
    MIN_CELL = 0
    MAX_CELL = 63
    # Moves???
    moves = []
    def save(self, *args, **kwargs):
        valid_fields = [0, 2, 4, 6, 9, 11, 13, 15, 16, 18, 20, 22, 25, 27, 29,
                    31, 32, 34, 36, 38, 41, 43, 46, 47, 48, 50, 52, 54, 57, 59, 61, 63]
        if self.cat_user != None and self.mouse_user != None and GameStatus.CREATED == self.status:
        	self.status = GameStatus.ACTIVE
        if (self.cat1 in valid_fields) and (self.cat2 in valid_fields) and (self.cat3 in valid_fields) and (self.cat4 in valid_fields) and (self.mouse in valid_fields):
            return super(Game, self).save(*args, **kwargs)
        else:
            raise ValidationError("Invalid cell for a cat or the mouse|Gato o ratón en posición no válida")
    def full_clean(self):
        valid_fields = [0, 2, 4, 6, 9, 11, 13, 15, 16, 18, 20, 22, 25, 27, 29,
                    31, 32, 34, 36, 38, 41, 43, 46, 47, 48, 50, 52, 54, 57, 59, 61, 63]
        if (self.cat1 in valid_fields) and (self.cat2 in valid_fields) and (self.cat3 in valid_fields) and (self.cat4 in valid_fields) and (self.mouse in valid_fields):
            return super(Game, self).full_clean()
        else:
            raise ValidationError("Invalid cell for a cat or the mouse|Gato o ratón en posición no válida")
    def __str__(self):
        cadena = "(" + str(self.id) + ", " + str(GameStatus.STATUS[(self.status)]) + ")\tCat ["
        if self.cat_turn == True:
            cadena += "X"
        else:
            cadena += " "
        cadena += "] cat_user_test(" + str(self.cat1) + ", " + str(self.cat2) + ", " + str(self.cat3) + ", " + str(self.cat4) + ")"
        #if self.status == GameStatus.ACTIVE or  self.status == GameStatus.FINISHED:
        if self.mouse_user != None:
            cadena += " --- Mouse ["
            if self.cat_turn == True:
                cadena += " "
            else:
                cadena += "X"
            cadena += "] mouse_user_test(" + str(self.mouse) + ")"
        return cadena


class Move(models.Model):

    origin = models.IntegerField(null=False)
    target = models.IntegerField(null=False)
    game = models.ForeignKey(Game, related_name='game', on_delete=models.CASCADE)
    player = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    date = models.DateField(default=django.utils.timezone.now)

    borde_izq = {0,16,32,48}
    borde_dcha = {15,31,47}
    borde_top_mouse = {2,4,6}
    borde_bot = {57,59,61,63}
    borde_izq_mouse = {16,32,48}
    borde_bot_mouse = {57,59,61}
    esquina_ti = {0}
    esquina_bd = {63}

    def save(self, *args, **kwargs):
        if self.game.status == GameStatus.ACTIVE:
            if (self.player == self.game.cat_user):
                    if (self.origin in self.borde_izq) and (self.target == self.origin + 9):
                        self.game.moves.append(1)
                        self.game.save()
                        return super(Move, self).save(*args, **kwargs) #valid move

                    if (self.origin in self.borde_dcha) and (self.target == self.origin + 7):
                        self.game.moves.append(1)
                        self.game.save()
                        return super(Move, self).save(*args, **kwargs) #valid move

                    if (self.origin in self.borde_bot):
                        raise ValidationError("Move not allowed|Movimiento no permitido does not match ['Error']") #Invalid move                

                    if (self.target == self.origin + 9) or (self.target == self.origin + 7):
                        self.game.moves.append(1)
                        self.game.save()
                        return super(Move, self).save(*args, **kwargs) #valid move
            elif (self.player == self.game.mouse_user):
                    if ((self.origin in self.borde_izq_mouse) and
                       ((self.target == self.origin + 9) or (self.target == self.origin - 7))):
                        self.game.moves.append(1)
                        self.game.save()
                        return super(Move, self).save(*args, **kwargs) #valid move

                    if ((self.origin in self.borde_dcha) and
                       ((self.target == self.origin + 7) or (self.target == self.origin - 9))):
                        self.game.moves.append(1)
                        self.game.save()
                        return super(Move, self).save(*args, **kwargs) #valid move

                    if ((self.origin in self.borde_bot_mouse) and 
                       ((self.target == self.origin - 7) or (self.target == self.origin - 9))): 
                        self.game.moves.append(1)
                        self.game.save()
                        return super(Move, self).save(*args, **kwargs) #valid move
                    
                    if ((self.origin in self.borde_top_mouse) and 
                       ((self.target == self.origin + 7) or (self.target == self.origin + 9))): 
                        self.game.moves.append(1)
                        self.game.save()
                        return super(Move, self).save(*args, **kwargs) #valid move  

                    if ((self.origin in self.esquina_ti) and (self.target == self.origin + 9)): 
                        self.game.moves.append(1)
                        self.game.save()
                        return super(Move, self).save(*args, **kwargs) #valid move   

                    if ((self.origin in self.esquina_bd) and (self.target == self.origin - 9)): 
                        self.game.moves.append(1)
                        self.game.save()
                        return super(Move, self).save(*args, **kwargs) #valid move    
                
                    if ((self.target == self.origin + 9) or (self.target == self.origin + 7) or
                       (self.target == self.origin - 9) or (self.target == self.origin - 7)):
                        self.game.moves.append(1)
                        self.game.save()
                        return super(Move, self).save(*args, **kwargs) #valid move
            else:
                raise ValidationError("Move not allowed|Movimiento no permitido does not match ['Error']")
        raise ValidationError("Move not allowed|Movimiento no permitido does not match ['Error']")
        
    def __str__(self):
        return self #mirar en los test de models como se imprime

class Counter(models.Model):
    value = models.IntegerField(null=False, default=0)
    #id = models.AutoField(primary_key=True)
    class __Counter():
        def __init__(self):
            val = models.IntegerField(null=False, default=0)
        def __str__(self):
            return "Counter: " + str(val)
    def __init__(self,value=0):
        #models.Model.__init__(self)
        super(Counter, self).__init__()
        setattr(self, 'value', value)
        self.save()
        #if not Counter.value:
        # Counter.value = Counter.__Counter()
    
    """def leer(self):
        return Counter.instance.val
    def incrementar(self, name):
        Counter.instance.val+=1
    def actualizar(self, newval):
        Counter.instance.val=newval"""
    def save(self, *args, **kwargs):
        if(getattr(self, 'id')!=1):
            raise ValidationError("Insert not allowed|Inseción no permitida")
        #Raisear el validationError si mete un objeto con primary key distinto de 1
        return super(Counter, self).save(*args, **kwargs)



    
	
	


