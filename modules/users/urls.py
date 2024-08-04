from django.urls import path
from .views import ProfileDetailView


app_name = 'users'

urlpatterns = [

    path('<str:slug>/', ProfileDetailView.as_view(), name='profile_detail'),

]