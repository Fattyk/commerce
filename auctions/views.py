from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Listing, Watch, Bid, Winner, Category
from django.contrib.auth.decorators import login_required
import re

# @login_required
def index(request):
    listings = Listing.objects.all()[::-1] #reverse listing with slice [::-1] such that last entry comes first
    if listings:
        # Generate categories
        code_categories = [item.category for item in listings]
        readable_categories = [Listing.value[item] for item in code_categories]    
        items = zip(listings, readable_categories)
    else:  
        items = zip([],[])
    for listing in listings:
        item = re.sub("^.*/auctions/", "/auctions/", listing.image.url)
        listing.image = item   
    return render(request, "auctions/index.html",{
        "listings":items,
        "title":"Active Listings",
    })

def won(request):
    user = request.user
    wins = [winner.message for winner in user.bid_winner.all()[::-1]]
    return render(request, "auctions/won.html",{
        "wins":wins
    })

def categories(request):
    categories = [category for category in Listing.choice.keys()]
    if categories:
        length = [len(Listing.objects.filter(category = val)) for val in Listing.value.keys()]
        cat = zip(categories, length)  # cat = [(category,val) for category,val in zip(categories, length)]
        pick = "These are the active categories"
        if max(length)==0:
            cat = zip([],[])
            pick = ""
    else:
        cat = zip([],[])
        pick = ""

    return render(request, "auctions/categories.html", {
        "categories": cat,
        "pick":pick
    })
@login_required
def category(request, category):
    category = category.upper()
    cat = category
    category = Listing.choice[category] # Fetch this category key from Listing class
    categories = Listing.objects.filter(category = category) # Fetch all listing associated with this category key and reverse the listing with slice [::-1] such that last entry comes first
    if categories:
        # Generate categories
        code_categories = [item.category for item in categories]
        readable_categories = [Listing.value[item] for item in code_categories]    
        items = zip(categories, readable_categories)
        for listing in categories:
            item = re.sub("^.*/auctions/", "/auctions/", listing.image.url)
            listing.image = item
    else:
        items = zip([],[])           
    return render(request, "auctions/index.html",{
        "listings":items,
        "title":f"{cat} Listings"
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
    # category = [item.category for item in Category.objects.all()] # [(k, v) for k,v in enumerate(category)]
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
            category = Category.objects.get(category_id)
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            c_price = form.cleaned_data["c_price"]
            image = form.cleaned_data["image"]
            user = User.objects.get(id=user_id)
            save_listing = Listing(title=title, description=description, c_price=c_price, category=category, user=user)
            save_listing.save()
            save_listing.image=image
            save_listing.save()
            
            return HttpResponse("Success")
        return render(request, "auctions/createList.html", {
            "CreateListingForm":form
        }) 
    return render(request, "auctions/createList.html", {
        "CreateListingForm":CreateListingForm()
    })


class BidForm(forms.Form):
    bid = forms.IntegerField(label="Bid")

@login_required
def bid(request, id):
    if request.method == "POST":
        
        # bid = request.POST.get("bid")
        bidform = BidForm(request.POST)

        if bidform.is_valid():
            bid = bidform.cleaned_data["bid"]
            # total bidder so far:
            listing = Listing.objects.get(id=id)
            if (bid>listing.c_price):
                listing.highest_bidder = request.user
                listing.c_price = bid
                listing.save()
                save_bid = Bid(user=request.user, listing=listing, bid=bid)
                save_bid.save()
                return HttpResponseRedirect(reverse('listing', args=(id,)))

            return HttpResponse("Bid must be greater than current bid")
        return HttpResponse("In valid form input")
    
    return HttpResponse("Error You have to Submit the form")


@login_required
def remove_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    highest_bidder = listing.highest_bidder 
    winner = Winner(user=highest_bidder, message=f"You have won {listing.title} with ${listing.c_price}")
    winner.save()
    listing.delete()
    return HttpResponseRedirect(reverse("index"))

def listing(request, id):
    user = request.user
    if user.is_authenticated:
        listing = Listing.objects.get(id=id)
        watch = Watch.objects.filter(user=user, listing=listing)
        add_remove_watchlist = "Remove from Watchlist" if (watch) else "Add to Watchlist"
        total_bid = listing.bid_listing.all() #Fetch all listing in listing of bids
        total_bid = len(total_bid)
        return render(request, "auctions/listing.html",{
            "listing":listing,
            "add_remove_watchlist":add_remove_watchlist,
            "bidform": BidForm(),
            "total_bid": total_bid
        })
    return render(request, "auctions/listing.html")


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
    # Generate categories
    code_categories = [item.listing.category for item in user_items]
    readable_categories = [Listing.value[item] for item in code_categories]    
    items = zip(watch, readable_categories)
    
    return render(request, "auctions/index.html",{
        "listings":items,
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
