from itertools import chain

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from main.models import FollowersCount, LikePost, Post, Profile


@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following = FollowersCount.objects.filter(
        follower=request.user.username
    ).values_list('user')
    feed = list(chain(Post.objects.filter(user_name__in=user_following)))

    all_users = User.objects.all()
    followed_users = User.objects.filter(username__in=user_following)
    suggestions_qs = set(all_users) - set(followed_users)
    suggested_profiles = Profile.objects.filter(user__in=suggestions_qs).exclude(
        user=user_object
    )
    follow_suggestions = list(chain(suggested_profiles))

    context = {
        'user_profile': user_profile,
        'posts': feed,
        'follow_suggestions': follow_suggestions[:4],
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
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                user.save()

                user_login = auth.authenticate(
                    request, username=username, password=password
                )
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
        user_profile.profile_image = (
            request.FILES.get('image') or user_profile.profile_image
        )
        user_profile.bio = request.POST['bio']
        user_profile.location = request.POST['location']
        user_profile.save()
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})


@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
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
    follower = request.user.username
    is_follow = FollowersCount.objects.filter(
        follower=follower, user=username
    ).first()
    button_text = 'Unfollow' if is_follow else 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=username))
    user_following = len(FollowersCount.objects.filter(follower=username))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        is_followed = FollowersCount.objects.filter(
            follower=follower, user=user
        ).first()

        if is_followed:
            FollowersCount.objects.get(follower=follower, user=user).delete()
        else:
            FollowersCount.objects.create(follower=follower, user=user)
        return redirect('/profile/' + user)
    else:
        return redirect('/')


@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        user_ids = User.objects.filter(username__icontains=username).values_list(
            'id'
        )
        profile_qs = Profile.objects.filter(id_user__in=user_ids)
        profile_list = list(chain(profile_qs))

    context = {
        'user_profile': user_profile,
        'profile_list': profile_list,
    }
    return render(request, 'search.html', context)
