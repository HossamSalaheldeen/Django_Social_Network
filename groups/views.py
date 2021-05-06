from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import CreateView,DetailView,ListView,RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from groups.models import Group
from django.urls import reverse_lazy,reverse
from django.shortcuts import get_object_or_404
from .models import Group,Groupmember
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from . import models
from .forms import GroupModelForm
from .filters import GroupFilter

# Create your views here.
class Creategroup(CreateView):
    model=Group
    template_name = 'groups/group_form.html'
    form_class = GroupModelForm
    def get_form_kwargs(self):
        kwargs = super(Creategroup, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class Singlegroup(DetailView):
    model=Group
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member'] = Groupmember.objects.all()
        
        return context


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
        print('=======(0)======')
        
        try:
            print(self.request.GET.get('user_id'))
            Groupmember.objects.create(user=self.request.user, group=group, is_accepted=None)

        except IntegrityError:
            messages.warning(self.request,"Warning! You are not a user!")
        else:
            messages.success(self.request,"You are now a member!")
        return super().get(request,*args,**kwargs)
    
    # def accept_member(self, request):
    #     Groupmember.objects.create(user=self.request.GET.get('user_id'), group=self.request.GET.get('group_id'))
    #     print('==============================')
    #     print(self.request.GET.get('user_id'))
    #     print('==============================')
    #     print(self.request.GET.get('user_id'))
    #     print('==============================')
    #     if value:
    #         value.update(is_accepted = 1)
    #         value.save()
    #         messages.success(self.request,"Member Added Successfully")
        

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
    
    def remove_member(self, request):
        value = models.Groupmember.objects.get(user=self.request.GET.get('user_id'), group=self.request.GET.get('group_id'))
        if value:
            value.update(is_accepted = 0)
            value.save()
            messages.success(self.request,"Member Removed Successfully")
        
def MyGroup(request):
    query = request.GET.get("group_name", None)
    if query is None:
        groups = Group.objects.filter(created_by=request.user)
    else:
        group_name=request.GET.get('group_name')
        groups = Group.objects.filter(name=group_name, created_by=request.user)
    context = {'object_list': groups,}
    return render(request, "groups/mygroups.html", context=context) 


def Accept_member(request):
        # value = Groupmember.objects.filter(Q(user=request.GET.get('user')) & Q(group=request.GET.get('group')))
    
        value = Groupmember.objects.filter(user_id=int(request.GET.get('user_id')), group_id=int(request.GET.get('group_id')))
        group = Group.objects.get(pk=int(request.GET.get('group_id')))
        print('==============================')
        print(group)
        print('==============================')
        
        print(request.GET.get('user_id'))
        print('==============================')
        print(request.GET.get('group_id'))
        print('==============================')
        
        if value:
            value[0].is_accepted = 1
            value[0].save()
            messages.success(request,"Member Added Successfully")
            context = {'object_list': value,}
            return redirect('/groups/posts/in/' + group.slug)
        
        
def Reject_member(request):
        value = Groupmember.objects.filter(user_id=int(request.GET.get('user_id')), group_id=int(request.GET.get('group_id')))
        group = Group.objects.get(pk=int(request.GET.get('group_id')))

        if value:
            value[0].is_accepted = 0
            value[0].save()
            messages.success(request,"Member Added Successfully")
            context = {'object_list': value,}
            return redirect('/groups/posts/in/' + group.slug)