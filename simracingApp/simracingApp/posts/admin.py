from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'author', 'created_at', 'likes_count']
    list_filter = ['created_at', 'author']
    search_fields = ['content']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    def likes_count(self, obj):
        """Return number of likes for the post"""
        return obj.likes.count()
    likes_count.short_description = 'Likes'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'author', 'post', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['content']
    ordering = ['-created_at']
    readonly_fields = ['created_at']