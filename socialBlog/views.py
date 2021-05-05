from django.http import HttpResponse
from django.shortcuts import render,redirect
from profiles.models import Profile
def home_view(request):
    user = request.user
    hello = 'Hello world'

    context = {
        'user': user,
        'hello' : hello,
    }
    return render(request, 'main/home.html', context)


def login_success(request):
    profile = Profile.objects.get(user=request.user)
    if profile.first_name == '':
        return redirect("/profiles/myprofile/")
    else:
        return redirect("/posts")