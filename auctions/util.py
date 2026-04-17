from .models import Listing_model, Bid_model, Comment_model, Watch_list
from datetime import datetime

def list_active_listing():
    return [listing for listing in Listing_model.objects.all().values() if listing['is_active']]

def add_listing(listing_info, request):
    current_date = datetime.now().strftime('%Y-%m-%d')
    listing = Listing_model(
        title=listing_info['title'], 
        description=listing_info['description'], 
        starting_bid=listing_info['starting_bid'],
        current_price=listing_info['starting_bid'],
        image_url=listing_info['image_url'],
        owner=request.user,
        is_active=True,
        created_at=current_date
    )
    listing.save()

def listing_info(id):
    listing_info = Listing_model.objects.get(id=id)
    return listing_info

def close_auction(id):
    listing_info = Listing_model.objects.get(id=id)
    listing_info.is_active = False
    listing_info.save()

def add_biding(amount, id, request):
    listing_info = Listing_model.objects.get(id=id)
    listing_info.current_price = amount
    listing_info.save()
    new_bid = Bid_model(user=request.user, listing=listing_info.id, amount=amount)
    new_bid.save()

def bid_count(id):
    bids = Bid_model.objects.filter(listing=id)
    current_bid = bids.order_by('amount').last()
    return {
        'count':bids.count(),
        'current_bid': current_bid,
        'bidder_name': str(current_bid.user) if current_bid else "No bids yet"
    }

def list_won_listings(request):    
    inactive_listings = Listing_model.objects.filter(is_active=False)
    won_listings = []

    for listing in inactive_listings:
        winning_bid = Bid_model.objects.filter(listing=listing.id).order_by('amount').last()
        if winning_bid and str(winning_bid.user) == str(request.user):
            won_listings.append(listing)
    return won_listings

def bid_comment(comment, id, request):
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_listing = Listing_model.objects.get(id=id)
    new_commment = Comment_model(
        user=request.user,
        listing=current_listing.id,
        content=comment, 
        created_at=current_date
    )
    new_commment.save()

def list_bid_comments(id):
    return [commment for commment in Comment_model.objects.all().values() if int(commment['listing']) == int(id)]

def add_watch_list(request, id):
    watch_list = Watch_list.objects.filter(id=id).values()
    if watch_list.count() > 0:
        return 1
    else:
        new_watch_item = Watch_list(user=request.user, listing=id)
        new_watch_item.save()

def list_watched_lists():
    watch_model = Watch_list.objects.all().values()
    watched_list = [Listing_model.objects.get(id=i['listing']) for i in watch_model]
    return watched_list

def remove_watch(id):
    watch_info = Watch_list.objects.get(listing=id)
    watch_info.delete()