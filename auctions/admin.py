from django.contrib import admin
from .models import *


class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'starting_bid', 'category', 'image_url', 'active')


admin.site.register(User)
admin.site.register(ListingCategory)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)