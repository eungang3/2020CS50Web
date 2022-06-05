from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django import forms

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

@login_required
def profile(request, writerid):
    if request.method == "GET":
    # check if logged-in user follows this writer
    # if so, don't render 'follow' button on html
        isFollowing = Follower.objects.filter(user=request.user.id, following=writerid).exists()
        following = Follower.objects.filter(user=writerid)
        follower = Follower.objects.filter(following=writerid)
        return render(request, "network/profile.html", {
            'writerid': writerid,
            'username': User.objects.get(id=writerid).username,
            'followings': following, 
            'followingNum': len(following),
            'followers': follower,
            'followerNum': len(follower), 
            'isFollowing' : isFollowing
        })
    
    # when user clicks follow/unfollow button
    else: 
        # in case user clicked follow button
        if (request.POST['follow'] == 'y'):
            # update Follower table
            followerUserObj = User.objects.get(id=request.user.id)
            followingUserObj = User.objects.get(id=writerid)
            followerObj = Follower(
                user = followerUserObj,
                following = followingUserObj
            )
            followerObj.save()

        # in case user clicked unfollow button
        else:
            # delete Follower row from the table
            Follower.objects.filter(user=request.user.id, following=writerid).delete()

        return HttpResponseRedirect(reverse("profile", args=(writerid,)))

@login_required
def following(request):
    return render(request, "network/following.html")


# functions for api calls 

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
    if request.method == "GET":
        if posttype == 'all':
            posts = Post.objects.all()
            return JsonResponse([post.serialize() for post in posts], safe=False)
    
        elif posttype == 'following':
            followings = Follower.objects.filter(user=request.user).values('following')
            followingIds = [following['following'] for following in followings]
            posts = []
            for followingId in followingIds:
                posts_raw = Post.objects.filter(writer=followingId).values()
                for post_raw in posts_raw:
                    writerid = post_raw['writer_id']
                    post_raw['writer'] = User.objects.get(id=writerid).username
                    post_raw['writerid'] = writerid
                    posts.append(post_raw) 
            result = sorted(posts, key=lambda x:x['id'])
            return JsonResponse(result, safe=False)
    
    else:
        return JsonResponse({"error": "Invalid post type."}, status=400)

def load_profile_posts(request, id):
    if request.method =='GET':
        posts = Post.objects.filter(writer=id)
        return JsonResponse([post.serialize() for post in posts], safe=False)
    else: 
        return JsonResponse({"error": "Invalid post type."}, status=400)
