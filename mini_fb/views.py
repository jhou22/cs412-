from django.shortcuts import redirect, render
# Jianhui Hou, jhou22@bu.edu, all views functions

from . models import * 
from . forms import *
from django.views.generic import *
from django.urls import *
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'
    
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'
    
class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    def get_context_data(self, **kwargs: any):
        context = super().get_context_data(**kwargs)
        user_form = UserCreationForm()
        context['user_form'] = user_form
        return context
    def form_valid(self, form):
        if self.request.POST:
            user_form = UserCreationForm(self.request.POST)
            user = user_form.save()
            form.instance.user = user
            # login(self.request, user)
            return super().form_valid(form)
        return super().form_valid(form)
    
    
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    
    def get_object(self, queryset = ...):
        # print("statusMessage")
        return Profile.objects.get(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        '''
        Gets context
        '''
        context = super().get_context_data(**kwargs)
        status_message = Profile.objects.get(user=self.request.user)
        print("STATUSMESSAGE")
        print()
        context['status_message'] = status_message
        print(status_message)
        return context
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new StatusMessage object.
        '''
        status_message = Profile.objects.get(user=self.request.user)
        form.instance.profile = status_message
        sm = form.save()
        files = self.request.FILES.getlist('files')
        for file in files:
            image = Image()
            image.image = file
            image.status_message = sm
            image.save()
        return super().form_valid(form)
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_success_url(self):
        '''
        goes back to show_profile
        '''
        return reverse("show_profile", kwargs=self.kwargs)

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    form_class = UpdateProfileForm
    model = Profile
    template_name = "mini_fb/update_profile_form.html"
    
    def get_object(self, queryset = ...):
        return Profile.objects.get(user=self.request.user)
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
        '''
        print(f'UpdateProfileView: form.cleaned_data={form.cleaned_data}')
        return super().form_valid(form)
    
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    template_name = "mini_fb/delete_status_form.html"
    model = StatusMessage
    context_object_name = 'status_message'
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''
        # get the pk for this comment
        pk = self.kwargs.get('pk')
        status_message = StatusMessage.objects.filter(pk=pk).first() # get one object from QuerySet
        
        # find the profile to which this StatusMessage is related by FK
        profile = status_message.profile
        
        # reverse to show the article page
        return reverse('show_profile', kwargs={'pk':profile.pk})

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    template_name = "mini_fb/update_status_form.html"
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    context_object_name = 'status_message'
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''
        # get the pk for this comment
        pk = self.kwargs.get('pk')
        status_message = StatusMessage.objects.filter(pk=pk).first() # get one object from QuerySet
        
        # find the article to which this StatusMessage is related by FK
        profile = status_message.profile
        
        # reverse to show the article page
        return reverse('show_profile', kwargs={'pk':profile.pk})
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'UpdateProfileView: form.cleaned_data={form.cleaned_data}')
        return super().form_valid(form)
    
class CreateFriendView(LoginRequiredMixin, View):
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def dispatch(self, request, *args, **kwargs):
        print(kwargs.get('pk'))
        p1 = Profile.objects.get(user=self.request.user)
        p2 = Profile.objects.get(pk=kwargs.get('other_pk'))
        p1.add_friend(p2)
        return redirect(reverse('show_profile', kwargs={'pk':kwargs.get('pk')}))
    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_object(self, queryset = ...):
        return Profile.objects.get(user=self.request.user)

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'
    print("here")
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_object(self, queryset = ...):
        return Profile.objects.get(user=self.request.user)