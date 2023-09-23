from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import ListingForm


def index(request):
    active_listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        'listings': active_listings
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


@login_required()
def new_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            user = request.user
            form.seller = user
            form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'auctions/newlisting.html', {
                'form': form
            })
    else:
        return render(request, 'auctions/newlisting.html', {
            'form': ListingForm
        })


def listing_view(request, listing_id):
    listing = Listing.objects.filter(id=listing_id).first()
    if listing:
        comments = listing.comments.all()
        return render(request, 'auctions/listing.html', {
            'listing': listing,
            'comments': comments
        })
    else:
        return render(request, 'auctions/error.html', {
            'message': 'Listing not found.'
        })


@login_required
def bid(request, listing_id):
    if request.method == 'POST':
        bid_value = float(request.POST['value'])
        listing = Listing.objects.filter(id=listing_id).first()
        if listing:
            # Check if bid is valid
            if listing.started() and bid_value > float(listing.get_highest_bid().value) or\
                    not listing.started() and bid_value >= float(listing.starting_bid):
                new_bid = Bid(value=bid_value, user=request.user, listing=listing)
                new_bid.save()
                return HttpResponseRedirect(reverse('listing', args=[listing_id]))
            else:
                return render(request, 'auctions/listing.html', {
                    'listing': Listing.objects.get(pk=listing_id),
                    'message': "Invalid bid."
                })
        else:
            return render(request, 'auctions/error.html', {
                'message': 'Listing not found.'
            })
    else:
        return render(request, 'auctions/listing.html', {
            'listing': Listing.objects.get(pk=listing_id),
            'message': "Invalid bid."
        })


def close(request, listing_id):
    listing = Listing.objects.filter(id=listing_id).first()
    if listing:
        if listing.bids.all():
            winner = listing.get_highest_bid().user
            listing.winner = winner
        listing.active = False
        listing.save()
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    else:
        return render(request, 'auctions/error.html', {
            'message': 'Listing not found.'
        })

@login_required
def watch(request, listing_id):
    listing = Listing.objects.filter(id=listing_id).first()
    if listing:
        user = request.user
        if listing.subscribers.filter(id=user.id).first():
            listing.subscribers.remove(user)
        else:
            listing.subscribers.add(user)
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    else:
        return render(request, 'auctions/error.html', {
            'message': 'Listing not found.'
        })


@login_required
def watchlist(request):
    user = request.user
    listings = user.subs.all()
    return render(request, 'auctions/watchlist.html', {
        'listings': listings
    })


@login_required
def comment(request, listing_id):
    listing = Listing.objects.filter(id=listing_id).first()
    if listing:
        if request.method == 'POST':
            content = request.POST['content']
            user = request.user
            new_comment = Comment(listing=listing,
                                  user=user,
                                  content=content)
            new_comment.save()
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    else:
        return render(request, 'auctions/error.html', {
            'message': 'Listing not found.'
        })


def categories(request):
    category_list = ListingCategory.objects.all()
    return render(request, 'auctions/categories.html', {
        'categories': category_list
    })


def category_view(request, category_id):
    category = ListingCategory.objects.filter(pk=category_id).first()
    if category:
        listings = category.listings.filter(active=True).all()
        return render(request, 'auctions/category.html', {
            'category': category,
            'listings': listings
        })