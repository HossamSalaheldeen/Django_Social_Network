from django.urls import path,re_path
from groups.views import Creategroup,Singlegroup,Listgroup,JoinGroup,LeaveGroup

app_name='groups'

urlpatterns = [
    path('new/',Creategroup.as_view(),name="create"),
    path('' ,Listgroup.as_view(),name="all"),
    path('posts/in/<slug>/',Singlegroup.as_view(),name="single"),
    path('join/<slug>/',JoinGroup.as_view(),name="join"),
    path('leave/<slug>/',LeaveGroup.as_view(),name="leave"),
]
