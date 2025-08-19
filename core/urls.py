from django.urls import path
from .views import *

# Create your urls here.

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dids/', ProjectsView.as_view(), name='projects'),
    path('dids/<int:pk>/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
]