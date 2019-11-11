# -*- coding: utf-8 -*-
from django.contrib import admin
from datamodel.models import Game, Move
admin.site.register(Game)
admin.site.register(Move)
#Supuestamente vacio






"""

from __future__ import unicode_literals


from datamodel.models import User, Game, Move

# Register your models here.
class UserAdmin(admin.ModelAdmin):
	display = ('username')

admin.site.register(User, UserAdmin)

class GameAdmin(admin.ModelAdmin):
	display = ('', '', '')

admin.site.register(Game, GameAdmin)

class MoveAdmin(admin.ModelAdmin):
	list_display = ('', '', '')

admin.site.register(Move, MoveAdmin)
"""