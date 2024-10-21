from django.db import models
from django.urls import reverse

# Jianhui Hou, jhou22@bu.edu, all models
class Profile(models.Model):
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=False)
    def get_absolute_url(self) -> str:
        '''
        gets the show_profile url for this profile
        '''
        return reverse("show_profile", kwargs={'pk': self.pk})
    
    def get_status_messages(self):
        '''
        gets list of status messages from earliest to latest
        '''
        messages = StatusMessage.objects.filter(profile=self)
        return reversed(messages)
    
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    def __str__(self):
        '''Return a string representation of this object.'''
        return f'{self.message}'
    
    def get_images(self):
        '''
        gets images for a specific statusmessage
        '''
        images = Image.objects.filter(status_message=self)
        return images
    
    
class Image(models.Model):
    image = models.ImageField(blank=True)
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)