from django.urls import path
from .views import ProfileDetailView, ProfileUpdateView


app_name = 'users'

urlpatterns = [
    path('edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('<str:slug>/', ProfileDetailView.as_view(), name='profile_detail'),

]