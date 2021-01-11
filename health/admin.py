from django.contrib import admin
from .models import *
# Register your models here.

class FoodAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Main_food._meta.fields]

class ProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Profile_user._meta.fields]

class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'url_field')

class Daily_foodAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Daily_food._meta.fields]

class MessageAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Messages._meta.fields]

admin.site.register(Main_food, FoodAdmin)
admin.site.register(Profile_user, ProfileAdmin)
admin.site.register(Daily_food, Daily_foodAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Messages, MessageAdmin)
