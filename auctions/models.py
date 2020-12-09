from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

def image_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/auctions/images/<filename>
        return f"auctions/static/auctions/images/{filename}"

class Category(models.Model):
    """
    Category class
    """
    category = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return f"{self.category}"

# ["FOOD", "FASHION", "TOYS", "ELECTRONICS", "HOME", "SOLAR", "EDUCATION", "TECHNOLOGY", "PLANTS", "ANIMALS"]
class Listing(models.Model):
    # user_cat = Category.objects.all() #or ["FOOD", "FASHION", "TOYS", "ELECTRONICS", "HOME", "SOLAR", "EDUCATION", "TECHNOLOGY", "PLANTS", "ANIMALS"]
    # KEY_NAME = [item.category for item in user_cat]
    
    # VALUE_SYS = [num for num,text in enumerate(KEY_NAME)]

    # choice = {key:value for (key,value) in zip(KEY_NAME, VALUE_SYS)}
    # value = {value:key for (key,value) in choice.items()}
    # CATEGORIES = [(v, k) for (k,v) in choice.items()]
    
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=300)
    c_price = models.IntegerField()
    image = models.ImageField(upload_to=image_directory_path)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE, related_name="input_cat")
    highest_bidder = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="highest_bidder")
    user = models.ForeignKey(User, blank=True, null= True, on_delete=models.CASCADE, related_name="uploader")
    date = models.DateTimeField(auto_now_add=True, null=True)
    # highest_bidder = models.CharField(max_length=64, blank=True)
    # category = models.CharField(max_length=3, choices=CATEGORIES, null=True, blank=True)

    def __str__(self):
        return f"{self.title} {self.description} {self.c_price} {self.image} {self.category} {self.highest_bidder} {self.user}"



class Watch(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="owner")
    listing = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE, related_name="watchlist")
    def __str__(self):
        return f"{self.user} {self.listing}"

class Bid(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="bid_owner")
    listing = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE, related_name="bid_listing")
    bid = models.IntegerField()
    def __str__(self):
        return f"{self.user} {self.listing} {self.bid}"

class Winner(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="bid_winner")
    message = models.CharField(max_length=300, null=True, blank=True)
    def __str__(self):
        return f"{self.user} {self.message}"

class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="com_user")
    listing = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE, related_name="com_listing")
    comment = models.CharField(max_length=300, null=True, blank=True)
    def __str__(self):
        return f"{self.user} {self.listing} {self.comment}"
