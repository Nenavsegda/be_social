from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponse

from main.models import Profile


def index(request):
    return render(request, 'index.html')

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

                user_object = User.objects.get(username=username)
                Profile.objects.create(user=user_object, id_user=user_object.id)
                return redirect('signup')
        else:
            messages.info(request, "Passwords don't match")
            return redirect('signup')
    else:
        return render(request, 'signup.html')
