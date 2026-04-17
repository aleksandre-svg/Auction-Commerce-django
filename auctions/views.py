from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User

from .util import list_active_listing, add_listing, listing_info, close_auction, add_biding, bid_count, list_won_listings, bid_comment, list_bid_comments, add_watch_list, list_watched_lists, remove_watch


def index(request):
    context = {
        'active_listings':list_active_listing(),
        'won_listings':list_won_listings(request)
    }
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
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
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
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

def create_listing(request):
    if request.method == 'POST':
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["startingbid"]
        image_url = request.POST["image"]
        add_listing({"title":title, "description":description, "starting_bid":starting_bid, "image_url":image_url}, request)
        return render(request, 'auctions/create.html')
    else:
        return render(request, 'auctions/create.html')

def listing(request, id):
    context = {
        'listing':listing_info(id),
        'error':{
            'exists':False,
            'message':''
        },
        'bid_count':bid_count(id),
        'comments':list_bid_comments(id)
    }
    if request.method == 'POST':
        if 'place_bid' in request.POST:
            new_bid = int(request.POST['newbid'])
            if new_bid >= context['listing'].starting_bid and new_bid > context['listing'].current_price:
                add_biding(new_bid, id, request)
                context['listing'] = listing_info(id)
            else:
                context['error'] = {
                    'exists': True,
                    'message':'the amount is not enough for bidding'
                }
        elif 'close_bid' in request.POST:
            close_auction(id)
            return HttpResponseRedirect(reverse("index"))
        elif 'comment_bid' in request.POST:
            comment = request.POST['comment_bid']
            bid_comment(comment, id, request)
            context['comments'] = list_bid_comments(id)
        elif 'watch' in request.POST:
            add_watch_list(request, id)
        elif 'remove_watch' in request.POST:
            remove_watch(id)
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'auctions/listing.html', context)
    else:
        return render(request, 'auctions/listing.html', context)


def watch_view(request):
    context = {
        'watch':list_watched_lists()
    }
    return render(request, 'auctions/watchlist.html', context)