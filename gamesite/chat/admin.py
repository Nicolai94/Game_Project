from django.contrib import admin

from .models import Room, Messages


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    save_as = True
    save_on_top = True
    search_fields = ['name']

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'date_added']


