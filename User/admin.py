from django.contrib import admin
from .models import Player,  Question, Choice, PlayerData

class Player_Admin (admin.ModelAdmin):
    list_display = ['fullname','unit','email','mobile','office_phone','state']
    search_fields = ['fullname']


class Question_Admin (admin.ModelAdmin):
    list_display = ['number','name','is_current']
    search_fields = ['name']

class Choice_Admin (admin.ModelAdmin):
    list_display = ['number','answer','question','correct']
    list_filter = ['question']
    search_fields = ['answer']

class PlayerData_Admin (admin.ModelAdmin):
    list_display = ['player','question','choice_selected','score','timestamp']
    search_fields = ['score']

admin.site.register(Player, Player_Admin)

admin.site.register(Choice, Choice_Admin)
admin.site.register(Question, Question_Admin)
admin.site.register(PlayerData, PlayerData_Admin)
