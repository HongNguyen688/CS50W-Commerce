# Import AbstractUser class from Django to extend the default User model
from django.contrib.auth.models import AbstractUser  
from django.db import models 

class User(AbstractUser):
    pass 


class Category(models.Model):
    # Name field for the category (e.g., 'Electronics', 'Clothing')
    name = models.CharField(max_length=100)  
    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=255)
    imageUrl = models.CharField(max_length=1000)  
    description = models.TextField()  
    price = models.FloatField()  
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")  
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")  
    isActive = models.BooleanField(default=True)  
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchListing")

    def __str__(self):
        return self.title

    
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingPrice")  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userPrice")  
    bidprice = models.FloatField()

    def __str__(self):
        return f"{self.user} bid ${self.bidprice:.2f} on {self.listing}"


class CommentReview(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingReview")  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userReview")  
    content = models.TextField()

    def __str__(self):
        return f"Comment by {self.user} on {self.listing}"

