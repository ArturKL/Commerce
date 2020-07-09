from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class ListingCategory(models.Model):
    title = models.CharField(max_length=64)


class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    starting_bid = models.DecimalField(max_digits=14, decimal_places=2)
    image_url = models.CharField(max_length=300, blank=True)
    catergory = models.ForeignKey(ListingCategory, on_delete=models.SET_NULL, related_name='category', null=True)
    active = models.BooleanField(default=True)
    subscribers = models.ManyToManyField(User, related_name='subscriptions', blank=True)


class Bid(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    value = models.DecimalField(max_digits=14, decimal_places=2)


class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=1000)

