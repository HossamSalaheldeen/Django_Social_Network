from django.urls import path
from .views import (
    my_profile_view,
    invite_received_view,
    profiles_list_view,
    invite_profiles_list_view,
    ProfileListView,
    send_invatation
)
app_name = 'profiles'

urlpatterns = [
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('my-invites/', invite_received_view, name='my-invites-view'),
    path('all-profiles/', ProfileListView.as_view(), name='all-profiles-view'),
    path('to-invite/', invite_profiles_list_view, name='invite-profiles-view'),
    path('send-invite/', send_invatation, name='send-invite')
]