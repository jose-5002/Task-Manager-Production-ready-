from django.contrib import admin

# Register your models here.
from .models import CustomUser, Tag, Task

admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(CustomUser)
