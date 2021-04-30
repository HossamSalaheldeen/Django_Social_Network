from django.urls import path
from .views import my_profile_view, invite_received_view, profiles_list_view, invite_profiles_list_view
app_name = 'profiles'

urlpatterns = [
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('my-invites/', invite_received_view, name='my-invites-view'),
    path('all-profiles/', profiles_list_view, name='all-profiles-view'),
    path('to-invite/', invite_profiles_list_view, name='invite-profiles-view'),
]