from django.db import models
from django.contrib.auth.models import User

class Feed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feeds')
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or self.url

class FeedItem(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=255)
    link = models.URLField()
    summary = models.TextField(blank=True)
    published = models.DateTimeField()
    guid = models.CharField(max_length=255)  
    read = models.BooleanField(default=False)

    class Meta:
        unique_together = ('feed', 'guid') 

    def __str__(self):
        return self.title
# Create your models here.
