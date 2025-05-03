from django.contrib import admin
from .models import Qist
# Register your models here.

class Qistadmin(admin.ModelAdmin):
    list_display = ('sr','date','amount','t_id','sender','receiver')
    
    

admin.site.register(Qist,Qistadmin)