from django.db import models
from django.contrib import admin
from models import Request

class RequestAdmin(admin.ModelAdmin):
    list_display = ('dest','ip')
admin.site.register(Request,RequestAdmin)