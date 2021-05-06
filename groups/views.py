from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import CreateView,DetailView,ListView,RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from groups.models import Group
from django.urls import reverse_lazy,reverse
from django.shortcuts import get_object_or_404
from groups.models import Group,Groupmember
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from . import models
from .filters import GroupFilter
# Create your views here.
class Creategroup(CreateView):
    model=Group
    fields=('name','description')
    def form_valid(self, form):
        self.object = form.save()
        Groupmember.objects.create(group=self.object, user=self.request.user)
        Groupmember.save(self.object)
        return HttpResponseRedirect(reverse_lazy('groups:all'))

class Singlegroup(DetailView):
    model=Group

class Listgroup(ListView):
    model = Group
    def get(self, request, *args, **kwargs):
        query = request.GET.get("group_name", None)

        if query is None:
            groups = Group.objects.all()
        else:
            group_name=request.GET.get('group_name')
            groups = Group.objects.filter(name=group_name)
            
        context = {'object_list': groups,}
		
        return render(request, "groups/group_list.html", context=context)   

class JoinGroup(LoginRequiredMixin,RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug' : self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            Groupmember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,"Warning! You are not a user!")
        else:
            messages.success(self.request,"You are now a member!")
        return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin,RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug' : self.kwargs.get('slug')})
    
    def get(self, request, *args, **kwargs):

        try:
            membership=models.Groupmember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        except models.Groupmember.DoesNotExist:
            messages.warning(self.request,"Sorry you are not in this group!")
        else:
            membership.delete()
            messages.success(self.request,"You have left the group")

        return super().get(request, *args, **kwargs)