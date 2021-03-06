from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Post, Like, Comment
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm
from groups.models import Group, Groupmember
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q

# Create your views here.
@login_required
def post_comment_create_and_list_view(request):
    qs_group = Groupmember.objects.values_list('group_id', flat=True).filter(user=request.user, is_accepted=1)
    qs = Post.objects.filter(Q(group__members=request.user) & Q(group__pk__in = qs_group) | Q(group__created_by=request.user)| Q(author__friends=request.user) & Q(group__isnull = True) | Q(author__user=request.user) & Q(group__isnull = True)).distinct()
    qs_group_member = Groupmember.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False
    p_form.fields['group'].queryset = Group.objects.filter(members=request.user, pk__in=qs_group)
    profile = Profile.objects.get(user=request.user)

    if 'submit_p_form' in request.POST:
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added = True

    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()

    context = {
        'qs': qs,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'post_added': post_added,
        'qs_group_member':qs_group_member,
    }

    return render(request, 'posts/main.html', context)


@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == "POST":
        pk  = request.POST.get('user_id')
        post_id  = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile  = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        user = request.user
        sender = Profile.objects.get(user=user)
        receiverName = receiver.user.email
        senderName   = sender.user.username
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)
        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
            post_obj.save()

            like.save()
        data = {
            'value': like.value,
            'likes': post_obj.liked.all().count()
        }
        send_mail('User {} has react on your post'.format(senderName),
            'Your post: {}'.format(post_obj.content), 
            settings.EMAIL_HOST_USER,
            [receiver.user.email],
            fail_silently=False)
        return JsonResponse(data, safe=False)
    return redirect('posts:main-post-view')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post 
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:main-post-view')    
    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You must be the author of the post to be able to delete it!')
        return obj

class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm
    model = Post 
    template_name = 'posts/update.html'
    success_url= reverse_lazy('posts:main-post-view')
    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user) 
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'You must be the author of the post to be able to update it!')
            return super().form_invalid(form)

@login_required
def post_comment_delete(self, pk):
    Comment.objects.get(pk=pk).delete()
    return redirect('posts:main-post-view')