from django.contrib import admin
from .models import Todo

# We want to be able to read the date_created as a read-only field. Right now it won't even let us see it on Django Admin
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created',)

admin.site.register(Todo, TodoAdmin)
