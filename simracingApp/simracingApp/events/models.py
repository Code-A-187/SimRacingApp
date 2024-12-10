from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(blank=True, default='')
    start_date = models.DateField()
    end_date = models.DateField()
    race_time = models.TimeField(help_text="Race start time")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='events'
    )
    subscribers = models.ManyToManyField(
        UserModel,
        related_name='subscribed_events',
        blank=True
    )

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title
