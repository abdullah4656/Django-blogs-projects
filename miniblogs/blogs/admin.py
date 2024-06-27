from django.contrib import admin
from blogs.models import Post
@admin.register(Post)
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','desc']
