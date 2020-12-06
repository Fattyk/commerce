from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/auctions/images/<filename>
    return f"auctions/static/auctions/images/{filename}"

class Listing(models.Model):
    KEY_NAME = ["FOOD", "FASHION", "TOYS", "ELECTRONICS", "HOME", "SOLAR", "EDUCATION", "TECHNOLOGY", "PLANTS", "ANIMALS"]
    
    VALUE_SYS = ["FOD","FAS","TOY","ELC","HOM","SLR","EDU","TEC","PLT","ANI"]

    choice = {key:value for (key,value) in zip(KEY_NAME, VALUE_SYS)}
    value = {value:key for (key,value) in choice.items()}
    CATEGORIES = [(v, k) for (k,v) in choice.items()]
    
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=100)
    c_price = models.IntegerField()
    image = models.ImageField(upload_to=image_directory_path)
    category = models.CharField(max_length=3, blank=True, choices=CATEGORIES, default=CATEGORIES[0][0])
    highest_bidder = models.ForeignKey(User, blank=True, null= True, on_delete=models.CASCADE, related_name="highest_bidder")
    user = models.ForeignKey(User, blank=True, null= True, on_delete=models.CASCADE, related_name="uploader")
    # highest_bidder = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"{self.title} {self.description} {self.c_price} {self.image} {self.category} {self.highest_bidder} {self.user}"



class Watch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist")
    def __str__(self):
        return f"{self.user} {self.listing}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_owner")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_listing")
    bid = models.IntegerField()
    def __str__(self):
        return f"{self.user} {self.listing} {self.bid}"