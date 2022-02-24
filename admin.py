from django.contrib import admin
from .models import Blog,MyBlog


# Register your models here.

@admin.register(Blog)
class AdminBlog(admin.ModelAdmin):
    list_display = ['id', 'username', 'title', 'distription', 'current_time', 'update_time']


@admin.register(MyBlog)
class AdminMyblog(admin.ModelAdmin):
    list_display = ['id','title','image','discription','author_id']