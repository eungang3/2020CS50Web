from django.contrib import admin
from .models import Listing, Bid, Comment, User, Category, Watchlist

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "title", "starting_price", "active", "current_price")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "bidder", "price")

admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Watchlist)