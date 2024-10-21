from django.urls import path
from .views import *
# Jianhui Hou, jhou22@bu.edu, all urls
urlpatterns = [
    path(r'', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path(r'profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
    path(r'create_profile', CreateProfileView.as_view(), name="create_profile"),
    path(r'<int:pk>/create_status', CreateStatusMessageView.as_view(), name='create_status'),
    path(r'profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),
    path(r'status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete_status_message'),
    path(r'status/<int:pk>/update', UpdateStatusMessageView.as_view(), name='update_status_message'),
]
