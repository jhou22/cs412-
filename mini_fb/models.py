from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=False)
    def get_absolute_url(self) -> str:
        return reverse("show_profile", kwargs={'pk': self.pk})
    
    def get_status_messages(self):
        messages = StatusMessage.objects.filter(profile=self)
        return reversed(messages)
    
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    def __str__(self):
        '''Return a string representation of this object.'''
        return f'{self.message}'