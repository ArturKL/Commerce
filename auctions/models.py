from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class ListingCategory(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.title}'


class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    starting_bid = models.DecimalField(max_digits=14, decimal_places=2)
    image_url = models.CharField(max_length=300, blank=True)
    category = models.ForeignKey(ListingCategory, default=39, on_delete=models.SET_DEFAULT, related_name='category')
    active = models.BooleanField(default=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    winner = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT, null=True, related_name='wins')
    subscribers = models.ManyToManyField(User, related_name='subs', blank=True)

    def __str__(self):
        return f'{self.title}'

    # Check if there are any bids
    def started(self):
        if self.bids.all():
            return True
        return False

    # Returns highest bid
    def get_highest_bid(self):
        highest_bid = self.bids.order_by('-value').first()
        return highest_bid

    # Returns current price
    def current_price(self):
        if self.started():
            return self.get_highest_bid().value
        return self.starting_bid


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    value = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return f'{self.user} bid {self.value} on {self.listing}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=1000)

