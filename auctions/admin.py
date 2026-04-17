from django.contrib import admin
from .models import Listing_model, Comment_model, Bid_model

# Register your models here.
admin.site.register(Listing_model)
admin.site.register(Bid_model)
admin.site.register(Comment_model)