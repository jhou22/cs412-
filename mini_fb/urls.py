from django.urls import path
from .views import *

urlpatterns = [
    path(r'', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path(r'profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
    path(r'create_profile', CreateProfileView.as_view(), name="create_profile"),
    path(r'<int:pk>/create_status', CreateStatusMessageView.as_view(), name='create_status'),
]
