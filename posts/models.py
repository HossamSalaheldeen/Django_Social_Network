from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile
from groups.models import Group
# Create your models here.

#Post Model
class Post(models.Model):
    content = models.TextField()
    image   = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    liked   = models.ManyToManyField(Profile, blank=True, related_name='likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author  = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    group   = models.ForeignKey(Group,related_name='posts',null=True,blank=True,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.content[:20])

    def num_likes(self):
        return self.liked.all().count()

    def num_comments(self):
        return self.comment_set.all().count()
    
    def user_groups(self):
        return self.group.members.all()

    class Meta:
        ordering = ('-created',)
        
        

#Comment Model
class Comment(models.Model):
    user    = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)
    body    = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

#Like Model
class Like(models.Model): 
    user    = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)
    value   = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"

class BadWord(models.Model):

    word   = models.CharField(max_length=100)
    
    def __str__(self):
        return self.word
    
    