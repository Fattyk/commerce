from django.contrib import admin

from .models import Listing, User, Watch, Bid, Winner
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "c_price", "image", "category", "highest_bidder", "user")

admin.site.register(Listing, ListingAdmin)
admin.site.register(User)
admin.site.register(Watch)
admin.site.register(Bid)
admin.site.register(Winner)
