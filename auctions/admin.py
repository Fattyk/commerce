from django.contrib import admin

from .models import Listing, User, Watch, Bid
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "c_price", "image")

admin.site.register(Listing, ListingAdmin)
admin.site.register(User)
admin.site.register(Watch)
admin.site.register(Bid)
