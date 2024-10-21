from django.shortcuts import render

from . models import * 
from . forms import *
from django.views.generic import *
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
        '''
        Gets context
        '''
        context = super().get_context_data(**kwargs)
        status_message = Profile.objects.get(pk=self.kwargs['pk'])
        context['status_message'] = status_message
        print(status_message)
        return context
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new StatusMessage object.
        '''
        status_message = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = status_message
        sm = form.save()
        files = self.request.FILES.getlist('files')
        for file in files:
            image = Image()
            image.image = file
            image.status_message = sm
            image.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        '''
        goes back to show_profile
        '''
        return reverse("show_profile", kwargs=self.kwargs)

class UpdateProfileView(UpdateView):
    form_class = UpdateProfileForm
    model = Profile
    template_name = "mini_fb/update_profile_form.html"
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
        '''
        print(f'UpdateProfileView: form.cleaned_data={form.cleaned_data}')
        return super().form_valid(form)
    
class DeleteStatusMessageView(DeleteView):
    template_name = "mini_fb/delete_status_form.html"
    model = StatusMessage
    context_object_name = 'status_message'
    
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''
        # get the pk for this comment
        pk = self.kwargs.get('pk')
        status_message = StatusMessage.objects.filter(pk=pk).first() # get one object from QuerySet
        
        # find the profile to which this StatusMessage is related by FK
        profile = status_message.profile
        
        # reverse to show the article page
        return reverse('show_profile', kwargs={'pk':profile.pk})

class UpdateStatusMessageView(UpdateView):
    template_name = "mini_fb/update_status_form.html"
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    context_object_name = 'status_message'

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