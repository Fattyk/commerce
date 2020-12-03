from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Watch
from django.contrib.auth.decorators import login_required
import re

# @login_required
def index(request):
    listings = Listing.objects.all()[::-1] #reverse listing with slice [::-1] such that last entry comes first
    if listings:       
        for listing in listings:
            item = re.sub("^.*/auctions/", "/auctions/", listing.image.url)
            listing.image = item   
    return render(request, "auctions/index.html",{
        "listings":listings,
        "title":"Active Listings"
    })

@login_required
def createList(request):
    return render(request, "auctions/createList.html")

# @login_required
def listing(request, id):
    listing = Listing.objects.get(id=id)
    # listings = Listing.objects.all()
    # for item in listings:
    #     if item.id == id:
    #         listing = item
    user = request.user
    watch = Watch.objects.filter(user=user, listing=listing)
    # if watch:
    #     add_remove_watchlist  = "I have you"
    # else:
    #     add_remove_watchlist = "I don't have you"
    
    add_remove_watchlist = "Remove from Watchlist" if (watch) else "Add to Watchlist"

    return render(request, "auctions/listing.html",{
        "listing":listing,
        "add_remove_watchlist":add_remove_watchlist
    })
@login_required
def add_remove_watch(request, id):
    listing = Listing.objects.get(id=id)
    user = request.user
    watch = Watch.objects.filter(user=user, listing=listing)
    if watch:
        watch.delete()
    else:
        watch = Watch(user=user, listing=listing)
        watch.save()
    return HttpResponseRedirect(reverse('listing', args=(id,)))


@login_required    
def watch(request):
    user = request.user # obtain user
    user_items = user.owner.all() # get all user input in Watch model
    # watch = [x.watchlist for x in watchlist]
    watch = []
    for item in user_items:
            item = item.listing
            image = re.sub("^.*/auctions/", "/auctions/", item.image.url)
            item.image = image
            watch.append(item)
    
    return render(request, "auctions/index.html",{
        "listings":watch,
        "title":"Watchlist"
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
