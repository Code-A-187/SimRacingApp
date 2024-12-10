from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class Post(models.Model):
    content = models.TextField()
    image_url = models.URLField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    likes = models.ManyToManyField(
        UserModel,
        related_name='liked_posts',
        blank=True,
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Post by {self.author.username} at {self.created_at}'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on post {self.post.id}'
