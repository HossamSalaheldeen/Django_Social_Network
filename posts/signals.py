from django.db.models.signals import post_save,pre_save,post_delete, pre_delete
from django.dispatch import receiver
from .models import Like, Comment, Post, Profile
from django.conf import settings
from django.core.mail import send_mail

@receiver(post_save,sender=Comment)
def after_comment_creation(sender,instance,created,*args,**kwargs):
    if created:
        comment      = instance.body 
        sender   = Profile.objects.get(pk=instance.user_id)
        post         = Post.objects.get(pk=instance.post_id)
        receiver      = Profile.objects.get(pk=post.author_id)

        send_mail('User {} has commented on your post'.format(sender.user.username),
            'Your post is: {} \n comment is: {}'.format(post.content,comment), 
            settings.EMAIL_HOST_USER,
            [receiver.user.email],
            fail_silently=False)
    else:
        print("updating")

