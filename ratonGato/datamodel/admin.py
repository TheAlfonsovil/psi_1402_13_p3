# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from application.models import User, Game, Move

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
