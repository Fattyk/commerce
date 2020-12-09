from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Listing, Watch, Bid, Winner, Category, Comment
from django.contrib.auth.decorators import login_required
import re

# @login_required
def index(request):
    """
    View about the index page
    """
    #reverse listing with slice [::-1] such that last entry comes first
    listings = Listing.objects.all()[::-1] 
    
    for listing in listings:
        # change the image url to where static can access it
        item = re.sub("^.*/auctions/", "/auctions/", listing.image.url)
        listing.image = item   

    return render(request, "auctions/index.html",{
        "listings":listings,
        "title":"Active Listings",
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


def categories(request):
    """
    categories View
    """
    # collect all active categories using 'set' to avoid dublicate
    categories = {item.category for item in Listing.objects.all()} 

    # pair each element listing with its total occurence
    categories = [(item, len(Listing.objects.filter(category = item))) for item in categories]
    pick = "These are the active categories" if (categories) else ""
    return render(request, "auctions/categories.html", {
        "categories": categories,
        "pick":pick
    })

    
@login_required
def category(request, category):
    """
    categories View
    """  
    category = Category.objects.get(category=category) #inner category is just a string

    # Fetch all listing associated with this category and reverse the listing with slice [::-1]
    listings = Listing.objects.filter(category=category)[::-1]

    for listing in listings:
        item = re.sub("^.*/auctions/", "/auctions/", listing.image.url)
        listing.image = item   

    return render(request, "auctions/index.html",{
        "listings":listings,
        "title":f"{category.category.capitalize()} Listings",
    })


class CreateListingForm(forms.Form):
    title = forms.CharField(label="Title:", max_length=64, widget=forms.TextInput(attrs={
        "class":"form-control"
    }))
    description = forms.CharField(label="Description", max_length=100, widget=forms.Textarea(attrs={
        "class":"form-control"
    }))
    c_price = forms.IntegerField(label="Price", widget=forms.NumberInput(attrs={
        "class":"form-control"
    }))
    image = forms.ImageField(label="Upload Image:", widget=forms.ClearableFileInput(attrs={
        "class":"form-control"
    }))

    # Define a list of turples for category choices
    categories =  [(item.id, item.category) for item in Category.objects.all()]
    category = forms.ChoiceField(label="Choose Category:", choices=categories, widget=forms.Select(attrs={
        "class":"form-control"
    }))

@login_required
def createList(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST, request.FILES)
        user_id = int(request.POST.get("user_id"))
        if form.is_valid():
            category_id = int(form.cleaned_data["category"])
            category = Category.objects.get(id=category_id)
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            c_price = form.cleaned_data["c_price"]
            image = form.cleaned_data["image"]
            user = User.objects.get(id=user_id)
            save_listing = Listing(title=title, description=description, c_price=c_price, category=category, user=user)
            save_listing.save()
            save_listing.image=image
            save_listing.save()
            return HttpResponseRedirect(reverse('index'))
        return render(request, "auctions/createList.html", {
            "CreateListingForm":form
        }) 
    return render(request, "auctions/createList.html", {
        "CreateListingForm":CreateListingForm()
    })


def listing(request, id):
    listing = Listing.objects.get(id=id)
    item = re.sub("^.*/auctions/", "/auctions/", listing.image.url)
    listing.image = item
    
    if request.user.is_authenticated:
        # if request is not post
        user = request.user

        #Get this watch using the user and the specific listing
        watch = Watch.objects.filter(user=user, listing=listing)

        add_remove_watchlist = "Remove from Watchlist" if (watch) else "Add to Watchlist"

        # Find the total of all listing in bids' listing
        total_bid = listing.bid_listing.all() 
        total_bid = len(total_bid)

        # Get all comments in reverse order
        comments = listing.com_listing.all()[::-1]

        if request.method == "POST":
            bidform = BidForm(request.POST)

            # if bidform is not valid
            if not (bidform.is_valid()):
                return render(request, "auctions/listing.html",{
                    "listing": listing,
                    "add_remove_watchlist": add_remove_watchlist,
                    "bidform":  bidform,
                    "total_bid": total_bid,
                    "comments": comments
                })
            bid = bidform.cleaned_data["bid"]
            listing = Listing.objects.get(id=id)
            
            # if bid is lower than current bid return error
            if not (bid > listing.c_price):
                return render(request, "auctions/listing.html",{
                    "listing": listing,
                    "add_remove_watchlist": add_remove_watchlist,
                    "bidform":  bidform,
                    "total_bid": total_bid,
                    "comments": comments,
                    "error": f"Unacceptable! {bid} <= {listing.c_price}. Your bid must be greater than current bid: {listing.c_price}"
                })
            # since bid is greater than current bid, perform required operation
            listing.highest_bidder = request.user
            listing.c_price = bid
            listing.save()
            save_bid = Bid(user=request.user, listing=listing, bid=bid)
            save_bid.save()

        return render(request, "auctions/listing.html",{
            "listing": listing,
            "add_remove_watchlist": add_remove_watchlist,
            "bidform":  BidForm(),
            "total_bid": total_bid,
            "comments": comments
        })
    return render(request, "auctions/listing.html",{
        "listing": listing
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
    return HttpResponseRedirect(reverse('listing', args=(id,))) #args must be turple


class BidForm(forms.Form):
    bid = forms.IntegerField(label="Enter Your Bid Price:", widget=forms.NumberInput(attrs={
        "class":"form-control",
        "placeholder": "Enter Your Bid Price"
    }))


@login_required
def remove_listing(request, id):
    listing = Listing.objects.get(id=id)

    # save the highest bidder and its message
    highest_bidder = listing.highest_bidder 
    winner = Winner(user=highest_bidder, message=f"You have won {listing.title} with ${listing.c_price}")
    winner.save()
    listing.delete()
    return HttpResponseRedirect(reverse("index"))


@login_required
def comment(request, id):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        listing = Listing.objects.get(id=id)
        save_comment = Comment(user=user, listing=listing, comment=comment)
        save_comment.save()
        return HttpResponseRedirect(reverse('listing', args=(id,)))

@login_required    
def watch(request):
    """
    watch View
    """
    user = request.user # obtain user
    # get all user listing in each user in Watch model
    listings = [item.listing for item in user.owner.all()]
    for listing in listings:
        item = re.sub("^.*/auctions/", "/auctions/", listing.image.url)
        listing.image = item 
    return render(request, "auctions/index.html",{
        "listings":listings,
        "title":"My Watchlist"
    })

@login_required
def won(request):
    user = request.user
    wins = [winner.message for winner in user.bid_winner.all()[::-1]]
    return render(request, "auctions/won.html",{
        "wins":wins
    })
    