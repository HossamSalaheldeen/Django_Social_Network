from django.urls import path,re_path
from groups.views import Creategroup,Singlegroup,Listgroup,JoinGroup,LeaveGroup, MyGroup, Accept_member, Reject_member,Set_member_pending

app_name='groups'

urlpatterns = [
    path('new/',Creategroup.as_view(),name="create"),
    path('' ,Listgroup.as_view(),name="all"),
    path('mygroups/', MyGroup, name="mygroup"),
    path('accept-member/', Accept_member, name="accept-member"),
    path('reject-member/', Reject_member, name="reject-member"),
    path('set-member-pending/', Set_member_pending, name="set-member-pending"),
    path('posts/in/<slug>/',Singlegroup.as_view(),name="single"),
    path('join/<slug>/',JoinGroup.as_view(),name="join"),
    path('leave/<slug>/',LeaveGroup.as_view(),name="leave"),
]
