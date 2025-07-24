from django.contrib import admin

from todo.models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_completed','created_at','updated_at']
    list_display_links = ['title']
    list_filter = ['title','is_completed']

