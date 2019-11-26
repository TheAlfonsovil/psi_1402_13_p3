from __future__ import unicode_literals
from datetime import datetime
import django
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from . import constants

ERROR_COUNTER = "Insert not allowed|Inseción no permitida"

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
    #moves = []
    


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
    game = models.ForeignKey(Game, null=False, on_delete=models.CASCADE, related_name='moves')
    player = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    date = models.DateField(default=django.utils.timezone.now)
    valid_fields = [0, 2, 4, 6, 9, 11, 13, 15, 16, 18, 20, 22, 25, 27, 29,
                    31, 32, 34, 36, 38, 41, 43, 46, 47, 48, 50, 52, 54, 57, 59, 61, 63]
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
                    #self.game.moves.append(1)
                    if self.game.cat1 == self.origin:
                        self.game.cat1 = self.target
                    if self.game.cat2 == self.origin:
                        self.game.cat2 = self.target
                    if self.game.cat3 == self.origin:
                        self.game.cat3 = self.target
                    if self.game.cat4 == self.origin:
                        self.game.cat4 = self.target
                    self.game.cat_turn = not self.game.cat_turn 
                    self.game.save()
                    return super(Move, self).save(*args, **kwargs) #valid move

                elif (self.origin in self.borde_dcha) and (self.target == self.origin + 7):
                    #self.game.moves.append(1)
                    if self.game.cat1 == self.origin:
                        self.game.cat1 = self.target
                    if self.game.cat2 == self.origin:
                        self.game.cat2 = self.target
                    if self.game.cat3 == self.origin:
                        self.game.cat3 = self.target
                    if self.game.cat4 == self.origin:
                        self.game.cat4 = self.target
                    self.game.cat_turn = not self.game.cat_turn
                    self.game.save()
                    return super(Move, self).save(*args, **kwargs) #valid move

                elif (self.origin in self.borde_bot):
                    if self.target not in self.valid_fields:
                        raise ValidationError("Invalid cell for a cat or the mouse|Gato o ratón en posición no válida")
                    raise ValidationError("Move not allowed|Movimiento no permitido does not match ['Error']")

                elif (self.target == self.origin + 9) or (self.target == self.origin + 7):
                    #self.game.moves.append(1)
                    if self.game.cat1 == self.origin:
                        self.game.cat1 = self.target
                    if self.game.cat2 == self.origin:
                        self.game.cat2 = self.target
                    if self.game.cat3 == self.origin:
                        self.game.cat3 = self.target
                    if self.game.cat4 == self.origin:
                        self.game.cat4 = self.target
                    self.game.cat_turn = not self.game.cat_turn
                    self.game.save()
                    return super(Move, self).save(*args, **kwargs) #valid move
                else:
                    if self.target not in self.valid_fields:
                        raise ValidationError("Invalid cell for a cat or the mouse|Gato o ratón en posición no válida")
                    raise ValidationError("Move not allowed|Movimiento no permitido does not match ['Error']")
            elif (self.player == self.game.mouse_user):
                if ((self.origin in self.borde_izq_mouse) and
                   ((self.target == self.origin + 9) or (self.target == self.origin - 7))):
                    #self.game.moves.append(1)
                    if self.game.mouse == self.origin:
                        self.game.mouse = self.target
                    self.game.cat_turn = not self.game.cat_turn
                    self.game.save()
                    return super(Move, self).save(*args, **kwargs) #valid move

                elif ((self.origin in self.borde_dcha) and
                   ((self.target == self.origin + 7) or (self.target == self.origin - 9))):
                    #self.game.moves.append(1)
                    if self.game.mouse == self.origin:
                        self.game.mouse = self.target
                    self.game.cat_turn = not self.game.cat_turn
                    self.game.save()
                    return super(Move, self).save(*args, **kwargs) #valid move

                elif ((self.origin in self.borde_bot_mouse) and 
                   ((self.target == self.origin - 7) or (self.target == self.origin - 9))): 
                    #self.game.moves.append(1)
                    if self.game.mouse == self.origin:
                        self.game.mouse = self.target
                    self.game.cat_turn = not self.game.cat_turn
                    self.game.save()
                    return super(Move, self).save(*args, **kwargs) #valid move
                
                elif ((self.origin in self.borde_top_mouse) and 
                   ((self.target == self.origin + 7) or (self.target == self.origin + 9))): 
                    #self.game.moves.append(1)
                    if self.game.mouse == self.origin:
                        self.game.mouse = self.target
                    self.game.cat_turn = not self.game.cat_turn
                    self.game.save()
                    return super(Move, self).save(*args, **kwargs) #valid move  

                elif ((self.origin in self.esquina_ti) and (self.target == self.origin + 9)): 
                    #self.game.moves.append(1)
                    if self.game.mouse == self.origin:
                        self.game.mouse = self.target
                    self.game.cat_turn = not self.game.cat_turn
                    self.game.save()
                    return super(Move, self).save(*args, **kwargs) #valid move   

                elif ((self.origin in self.esquina_bd) and (self.target == self.origin - 9)): 
                    #self.game.moves.append(1)
                    if self.game.mouse == self.origin:
                        self.game.mouse = self.target
                    self.game.cat_turn = not self.game.cat_turn
                    self.game.save()
                    return super(Move, self).save(*args, **kwargs) #valid move    
            
                elif ((self.target == self.origin + 9) or (self.target == self.origin + 7) or
                   (self.target == self.origin - 9) or (self.target == self.origin - 7)):
                    #self.game.moves.append(1)
                    if self.game.mouse == self.origin:
                        self.game.mouse = self.target
                    self.game.cat_turn = not self.game.cat_turn
                    self.game.save()
                    return super(Move, self).save(*args, **kwargs) #valid move
                else:
                    if self.target not in self.valid_fields:
                        raise ValidationError("Invalid cell for a cat or the mouse|Gato o ratón en posición no válida")
                    raise ValidationError("Move not allowed|Movimiento no permitido does not match ['Error']")
            else:
                if self.target not in self.valid_fields:
                    raise ValidationError("Invalid cell for a cat or the mouse|Gato o ratón en posición no válida")
                raise ValidationError("Move not allowed|Movimiento no permitido does not match ['Error']")
        if self.target not in self.valid_fields:
            raise ValidationError("Invalid cell for a cat or the mouse|Gato o ratón en posición no válida")
        raise ValidationError("Move not allowed|Movimiento no permitido does not match ['Error']")
        
    def __str__(self):
        return self #mirar en los test de models como se imprime

class CounterManager(models.Manager):

    def inc(self):
        objs = Counter.objects.all()
        if not objs or not objs[0]:
            obj = Counter(value=1)
            super(Counter, obj).save()
            return 1

        else:
            obj = objs[0]
            current = obj.value + 1
            obj.value = current
            super(Counter, obj).save()
            return current

    def create(self, *args, **kwargs):
        raise ValidationError(ERROR_COUNTER)

    def get_current_value(self):
        objs = Counter.objects.all()
        if not(not objs or not objs[0]):
            counter = objs[0]
            return counter.value
        else:
            counter = Counter(value=0)
            super(Counter, counter).save()
            return 0


class Counter(models.Model):
    objects = CounterManager()
    value = models.IntegerField(blank=True, null=True)
    
    def _str_(self):
        return str(self.value)

    def save(self, *args, **kwargs):
        raise ValidationError(ERROR_COUNTER)

