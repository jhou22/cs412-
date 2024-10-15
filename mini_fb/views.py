from django.shortcuts import render

from . models import * 
from . forms import *
from django.views.generic import ListView, DetailView, CreateView
from django.urls import *
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
    
class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status_message = Profile.objects.get(pk=self.kwargs['pk'])
        context['status_message'] = status_message
        return context
    
    def form_valid(self, form):
        
        
        
        print(f'CreateCommentView.form_valid(): form={form.cleaned_data}')
        print(f'CreateCommentView.form_valid(): self.kwargs={self.kwargs}')
        
        status_message = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = status_message
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("show_profile", kwargs=self.kwargs)
    