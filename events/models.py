from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_url = models.URLField(max_length=2048)
    image1 = models.TextField(blank=True, null=True)
    image2 = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
