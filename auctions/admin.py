from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(ListingCategory)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)