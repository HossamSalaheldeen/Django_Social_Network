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
<<<<<<< HEAD
    members=models.ManyToManyField(User,through="Groupmember", blank=True)
    created_by = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
=======
    created_by= models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    members=models.ManyToManyField(User, through="Groupmember", blank=True)
>>>>>>> aefc3f0606f2f674df1aedcfd36eb278de0f7caa

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

    class Meta:
        ordering =['name']


class Groupmember(models.Model):
    group=models.ForeignKey(Group,related_name='membership',on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name='user_groups',on_delete=models.CASCADE)
<<<<<<< HEAD
    is_accepted= models.BooleanField(default=0) 
=======
    is_accepted=models.BooleanField(default=False, null=True)
>>>>>>> aefc3f0606f2f674df1aedcfd36eb278de0f7caa

    def __str__(self):
        return self.user.username
    
    class Meta:
        unique_together=('group','user')