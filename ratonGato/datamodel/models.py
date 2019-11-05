from __future__ import unicode_literals
from datetime import datetime
from django.utils import timezone

from django.db import models


class User(models.Model):

    username = models.CharField(unique=True, max_length=128)
    password = models.CharField(unique=True, max_length=128)

    def save(self, *arg, **kwargs):
		super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self #mirar en los test de models como se imprime

class GameStatus(Enum):
    CREATED = 'Created' 
    ACTIVED = 'Actived'
    FINISHED = 'Finished'

class Game(models.Model):
    cat_user = models.ForeignKey(User, related_name='Jugador1')
    mouse_user = models.ForeignKey(User, related_name='Jugador2')
    cat1 = models.IntegerField(blank=False, default=0)
    cat2 = models.IntegerField(blank=False, default=2)
    cat3 = models.IntegerField(blank=False, default=4)
    cat4 = models.IntegerField(blank=False, default=6)
    mouse = models.IntegerField(default=59)
    cat_turn = models.BooleanField(blank=False, default=True)
    status = str(GameStatus(GameStatus.CREATED)) #aqui nose...
    valid_fields = {0, 2, 4, 6, 9, 11, 13, 15, 16, 18, 20, 22, 25, 27, 29,
                    31, 32, 34, 36, 38, 41, 43, 46, 47, 48, 50, 52, 54, 57, 59, 61, 63}
    
    def save(self, *arg, **kwargs):
        if (self.cat1 in self.valid_fields) and (self.cat2 in self.valid_fields)
            and (self.cat3 in self-valid_fields) and (self.cat4 in self.valid_fields)
            and (self.mouse in self.valid_fields):

            return super(Game, self).save(*args, **kwargs)

        else:
            return None

    def __str__(self):
        return self #mirar en los test de models como se imprime


class Move(models.Model):

    origin = models.IntegerField(blank=False)
    target = models.IntegerField(blank=False)
    game = models.ForeignKey(Game, related_name='game')
    player = models.ForeignKey(User, related_name='user')
    date = models.DateField(default=django.utils.timezone.now)

    borde_izq = {0,16,32,48}
    borde_dcha = {15,31,47}
    borde_top_mouse = {2,4,6}
    borde_bot = {57,59,61,63}
    borde_izq_mouse = {16,32,48}
    borde_bot_mouse = {57,59,61}
    esquina_ti = {0}
    esquina_bd = {63}

    def save(self, *arg, **kwargs):
        if (self.player = self.game.cat_user):
                if (self.origin in self.borde_izq) and (self.target = self.origin + 9):
                    return super(Move, self).save(*args, **kwargs) #valid move

                if (self.origin in self.borde_dcha) and (self.target = self.origin + 7):
                    return super(Move, self).save(*args, **kwargs) #valid move

                if (self.origin in borde_bot):
                    return None #Invalid move                

                if (self.target = self.origin + 9) or (target = self.origin + 7):
		            return super(Move, self).save(*args, **kwargs) #valid move
        elif (self.player = self.game.mouse_user):
                if (self.origin in self.borde_izq_mouse) and
                   ((self.target = self.origin + 9) or (self.target = self.origin - 7)):
                    return super(Move, self).save(*args, **kwargs) #valid move

                if (self.origin in self.borde_dcha) and
                   ((self.target = self.origin + 7) or (self.target = self.origin - 9)):
                    return super(Move, self).save(*args, **kwargs) #valid move

                if (self.origin in borde_bot_mouse) and 
                   ((self.target = self.origin - 7) or (self.target = self.origin - 9): 
                    return super(Move, self).save(*args, **kwargs) #valid move
                
                if (self.origin in borde_top_mouse) and 
                   ((self.target = self.origin + 7) or (self.target = self.origin + 9): 
                    return super(Move, self).save(*args, **kwargs) #valid move  

                if (self.origin in esquina_ti) and (self.target = self.origin + 9): 
                    return super(Move, self).save(*args, **kwargs) #valid move   

                if (self.origin in esquina_bd) and (self.target = self.origin - 9): 
                    return super(Move, self).save(*args, **kwargs) #valid move    
            
                if (self.target = self.origin + 9) or (target = self.origin + 7) or:
                   (self.target = self.origin - 9) or (target = self.origin - 7)
		            return super(Move, self).save(*args, **kwargs) #valid move

        else: 
            return None
        
    def __str__(self):
        return self #mirar en los test de models como se imprime


    
	
	


