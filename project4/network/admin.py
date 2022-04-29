from django.contrib import admin
from .models import User, Post, Like, Follower

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "writer", "content")

class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "liked_by")

class FollowerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "follower")

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Follower)