from django.contrib import admin
from blog.models import Post

# Register your models here.
# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 출력할 내용을 등록
    list_display = ['title','slug','author','publish','status']