from turtle import title
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.title}"

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", blank=True, null=True)
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=6, decimal_places=2)
    img = models.URLField(max_length=200, blank=True, default="https://res.cloudinary.com/dxeibizaf/image/upload/v1616122317/auctions/29_ykmfm6.jpg")
    active = models.BooleanField(default=True)
    current_price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.listing} {self.price}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.user} {self.content}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE) 