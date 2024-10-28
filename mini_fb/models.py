import random
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
    
    def get_friends(self):
        
        '''get all friends for a profile'''
        friends = []

        first_list = Friend.objects.filter(profile1=self)
        for f in first_list:
            friends.append(f.profile2)

        second_list = Friend.objects.filter(profile2=self)
        for s in second_list:
            friends.append(s.profile1)

        return friends

    def add_friend(self, other):
        '''adds friend using urls'''
        if other == self:
            return
        if (self is None):
            return
        if (other is None):
            return
        if len(list(Friend.objects.filter(profile1=self, profile2=other))) != 0:
            return
        if len(list(Friend.objects.filter(profile2=self, profile1=other))) != 0:
            return
        friend = Friend(profile1=self, profile2=other)
        friend.save()
    def get_friend_suggestions(self):
        '''gets friend suggestions for a profile'''
        friends = []
        first_list = Friend.objects.filter(profile1=self)
        for f in first_list:
            friends.append(f.profile2)

        second_list = Friend.objects.filter(profile2=self)
        for s in second_list:
            friends.append(s.profile1)
        list2 = Profile.objects.all()
        suggestions = []
        number = 0
        for item in list2:
            if item not in friends and item != self:
                suggestions.append(item)
                number+=1
            
            if number >= 5:
                break
                
        
        return suggestions
    
    def get_news_feed(self):
        
        '''Gets statusmessages for this profile and its friends'''
        all_status_messages = []
        all_status_messages.extend(list(self.get_status_messages()))
        friends = self.get_friends()
        for friend in friends:
            all_status_messages.extend(list(friend.get_status_messages()))
        
        all_status_messages.sort(reverse=True, key=lambda value: value.timestamp)
        return all_status_messages
            
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
    
class Friend(models.Model):
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}'