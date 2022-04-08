from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Listing, Bid, Comment, User, Category, Watchlist
from django.forms import ModelForm
from django.contrib import messages


def index(request):
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.exclude(active=False),
        "title" : "Active Listings"
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    class ListingForm(ModelForm):
        class Meta:
            model = Listing
            fields = ['title', 'starting_price', 'category', 'description' , 'img']
        def __init__(self, *args, **kwargs):
            super(ListingForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs.update({'class': 'form-control'})

    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = Listing()
            listing.title = form.cleaned_data['title']
            listing.starting_price = form.cleaned_data['starting_price']
            listing.description = form.cleaned_data['description']
            listing.img = form.cleaned_data['img']
            listing.current_price = form.cleaned_data['starting_price']
            listing.owner = request.user
            listing.category = form.cleaned_data['category']
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
        else:
            return render(request, "auctions/error.html", {
        "message" : "Something went wrong. Try again."
    })

    return render(request, "auctions/create.html", {
        "form" : ListingForm()
    })

class BidForm(ModelForm):
        class Meta:
            model = Bid
            fields = ['price']
        def __init__(self, *args, **kwargs):
            super(BidForm, self).__init__(*args, **kwargs)
            self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder':'place bid'})

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'placeholder':'Write a comment.', 'rows': 1, 'cols': 40})

def listing(request, id):
    listing = Listing.objects.get(id=id)
    watchlist = Watchlist.objects.filter(user=request.user)
    inWatchlist = False
    for item in watchlist:
        if item.listing == listing:
            inWatchlist = True
    if listing.winner == request.user:
        messages.success(request, "You won this listing!")
    return render(request, "auctions/listing.html", {
        "listing" : listing,
        "BidForm" : BidForm(),
        "CommentForm":CommentForm(),
        "comments": Comment.objects.filter(listing=listing),
        "inWatchlist": inWatchlist
    })

def comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        listing_id = request.POST['listing_id']

        if form.is_valid():
            listing = Listing.objects.get(id=listing_id)
            content = form.cleaned_data['content']
            comment = Comment()
            comment.listing = listing
            comment.content = content
            comment.user = request.user
            comment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    return render(request, "auctions/error.html", {
        "message" : "Something went wrong. Try again."
    })


def bid(request):
    if request.method == "POST":
        form = BidForm(request.POST)
        listing_id = request.POST['listing_id']
        
        if form.is_valid():
            price = form.cleaned_data['price']
            listing = Listing.objects.get(id=listing_id)

            if (price > listing.current_price):
                bid = Bid()
                bid.price = price
                bid.listing = listing
                bid.bidder = request.user
                bid.save()
                listing.current_price = price
                listing.save()
                messages.success(request, 'Successfully placed bid!')
            else:
                messages.error(request,'Bid should be higher than the current price. Try again.')    
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    return render(request, "auctions/error.html", {
        "message" : "Something went wrong. Try again."
    })
    
def close_bid(request):
    if request.method == "POST":
        messages.success(request, 'Bid is now closed.')
        listing_id = request.POST['listing_id']
        listing = Listing.objects.get(id=listing_id)
        listing.active = False
        winning_bidder_id = Bid.objects.filter(listing=listing).last().bidder.pk
        listing.winner = User.objects.get(id=winning_bidder_id)
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    return render(request, "auctions/error.html", {
        "message" : "Something went wrong. Try again."
    })
    
def my_listing(request):
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.filter(owner=request.user),
        "title" : "My Listings"
    })

def my_bid(request):
    myBids = Bid.objects.filter(bidder=request.user)
    listings = []
    for bid in myBids:
        listings.append(bid.listing)

    return render(request, "auctions/index.html", {
        "listings" : listings,
        "title" : "My Bids"
    })

def categories(request):
    return render(request, "auctions/categories.html",{
        "categories": Category.objects.all() 
    })

def category(request, title):
    categoryObj = Category.objects.get(id=title)
    return render(request, "auctions/index.html", {
        "title" : categoryObj.title,
        "listings" : Listing.objects.filter(category=categoryObj).exclude(active=False)
    })

def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST['listing_id']
        watchlist = Watchlist()
        watchlist.listing = Listing.objects.get(id=listing_id)
        watchlist.user = request.user
        watchlist.save()
        messages.success(request, 'Added to Watchlist.')
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    inWatchlist = Watchlist.objects.filter(user=request.user)
    listing_ids = []
    for listing in inWatchlist:
        listing_ids.append(listing.id)
    listings = []
    for listing_id in listing_ids:
        listings.append(Listing.objects.get(id=listing_id))
    return render(request, "auctions/index.html", {
        "title" : "Watchlist",
       "listings" : listings
    })