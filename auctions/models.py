from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing_model(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=120)
    starting_bid = models.IntegerField(default=0)
    current_price = models.IntegerField(default=0)
    image_url = models.CharField(max_length=100)
    owner = models.CharField(max_length=50)
    is_active = models.BooleanField(default=0)
    created_at = models.DateField()

class Bid_model(models.Model):
    user = models.CharField(max_length=50)
    listing = models.CharField(max_length=50)
    amount = models.IntegerField(default=0)

class Comment_model(models.Model):
    user = models.CharField(max_length=50)
    listing = models.CharField(max_length=50)
    content = models.CharField(max_length=100)
    created_at = models.DateField() 

class Watch_list(models.Model):
    user = models.CharField(max_length=50)
    listing = models.CharField(max_length=50)