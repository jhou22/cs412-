from django.urls import path
from .views import *

urlpatterns = [
    path(r'', VotersListView.as_view(), name='voters'),
    path(r'voter/<int:pk>', VoterDetailView.as_view(), name='voter'),
    path(r'graph', GraphView.as_view(), name='graph')
]
