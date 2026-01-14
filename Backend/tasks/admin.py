from django.contrib import admin

# Register your models here.
from .models import Task, Tag, CustomUser
admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(CustomUser)