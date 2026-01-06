# Import the necessary modules for registering models in the Django admin site.
from django.contrib import admin  
from .models import User, Category, Listing, CommentReview, Bid  

admin.site.register(User)  
admin.site.register(Category)  
admin.site.register(Listing)  
admin.site.register(CommentReview)  
admin.site.register(Bid)  
