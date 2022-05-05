from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like, Follower

def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def compose(request):
    # Composing a new post must be via POST
    if request.method != 'POST':
        return JsonResponse({"error" : "POST request required."}, status=400)

    # Get contents of post
    data = json.loads(request.body)
    writer = request.user
    content = data.get("content", "")
    if content == "":
        return JsonResponse({
            "error": "Content is empty."
        }, status=400)

    # Create post in db
    post = Post()
    post.writer = writer
    post.content = content
    post.save()

    return JsonResponse({"message": "post made successfully."}, status=201)
    
def load_posts(request, posttype):
    if posttype == 'all':
        posts = Post.objects.all()
    
    elif posttype == 'following':
        # TO do
        posts = Post.objects.all()
    
    else:
        return JsonResponse({"error": "Invalid post type."}, status=400)
    return JsonResponse([post.serialize() for post in posts], safe=False)
