from pyexpat import model
from django.contrib import admin
from django.db.models import Sum,  Count
from urllib3 import Retry
from .models import Player,  Question, Choice, PlayerData, Raking
from import_export.admin import ImportExportActionModelAdmin



class Player_Admin (ImportExportActionModelAdmin):
    list_editable = ['score','time']
    list_display = ['fullname','unit','email','mobile','office_phone','state','score','time']
    search_fields = ['fullname']
    ordering = ['-score','time']
    list_per_page = 120


class Question_Admin (admin.ModelAdmin):
    list_display = ['number','name','is_current']
    search_fields = ['name']

class Choice_Admin (admin.ModelAdmin):
    list_display = ['number','answer','question','correct']
    list_filter = ['question']
    search_fields = ['answer']

class PlayerData_Admin (admin.ModelAdmin):
    list_display = ['player','question','choice_selected','score','time_score', 'timestamp']
    search_fields = ['score']

class Ranking_Admin(admin.ModelAdmin):
    list_display = ['fullname','total_score','time_score']
admin.site.register(Raking,Ranking_Admin)
admin.site.register(Player, Player_Admin)

admin.site.register(Choice, Choice_Admin)
admin.site.register(Question, Question_Admin)
admin.site.register(PlayerData, PlayerData_Admin)
