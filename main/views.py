from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponse

from main.models import LikePost, Post, Profile


@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    posts = Post.objects.all()
    context = {
        'user_profile': user_profile,
        'posts': posts,
    }

    return render(request, 'index.html', context)

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'This email is already taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'This username is already taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(request, username=username, password=password)
                auth.login(request, user_login)

                user_object = User.objects.get(username=username)
                Profile.objects.create(user=user_object, id_user=user_object.id)
                return redirect('settings')
        else:
            messages.info(request, "Passwords don't match")
            return redirect('signup')
    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.warning(request, 'Credentials are invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        user_profile.profile_image = request.FILES.get('image') or user_profile.profile_image
        user_profile.bio = request.POST['bio']
        user_profile.location = request.POST['location']
        user_profile.save()
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def upload(request):
    if request.method =='POST':
        user_name = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        Post.objects.create(user_name=user_name, image=image, caption=caption)
    return redirect('/')

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    is_liked = LikePost.objects.filter(username=username, post_id=post_id).first()

    if not is_liked:
        LikePost.objects.create(username=username, post_id=post_id)
        post.number_of_likes += 1
    else:
        is_liked.delete()
        post.number_of_likes -= 1

    post.save()
    return redirect('/')

@login_required(login_url='signin')
def profile(request, username):
    user_object = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user_name=username)
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
    }
    return render(request, 'profile.html', context)
