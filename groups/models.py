from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User=get_user_model()

from django import template
register=template.Library()

class Group(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(allow_unicode=True,unique=True)
    description=models.TextField(blank=True,default='')
    description_html=models.TextField(editable=False,default='',blank=True)

    members=models.ManyToManyField(User,through="Groupmember", blank=True)
    created_by = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)


    def __str__(self):
        return self.name

    def save(self, *args,**kwargs):
        is_new = True if not self.id else False
        self.slug=slugify(self.name)
        self.description_html=self.description
        super(Group, self).save(*args,**kwargs)
        if is_new:
            Groupmember.objects.create(group_id=self.id, user=self.created_by, is_accepted=1)

    def get_absolute_url(self):
        return reverse("groups:single", kwargs={"slug": self.slug})

    def join_requests(self):
        return Groupmember.objects.filter(group=self, is_accepted=None)
    
    def joined_request(self):        
        return Groupmember.objects.filter(group=self)
    
    def rejected_request(self):        
        return Groupmember.objects.filter(group=self, is_accepted=0)
    
    # def reject_requests(self, request):
    #     print('============================')
    #     # print(request.user)
    #     print('============================')
    #     return Groupmember.objects.filter(group=self, is_accepted=0 , user= self.members)
    
    # def accept_requests(self):
    #     return Groupmember.objects.filter(group=self, is_accepted=1)

    # class Meta:
    #     ordering =['name']


class Groupmember(models.Model):
    group=models.ForeignKey(Group,related_name='membership',on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name='user_groups',on_delete=models.CASCADE)
    is_accepted=models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        unique_together=('group','user')