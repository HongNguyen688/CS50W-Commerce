# Importing necessary modules
from django.contrib.auth import authenticate, login, logout  
from django.db import IntegrityError  
from django.http import HttpResponse, HttpResponseRedirect  
from django.shortcuts import render 
from django.urls import reverse  
from .models import User, Category, Listing, CommentReview, Bid  


def index(request):
    # Get all listings that are marked as active
    activeList = Listing.objects.filter(isActive=True)
    # Get all categories to show them on the homepage
    categories = Category.objects.all()
    
    return render(request, "auctions/index.html", {
        "activelistings": activeList,  
        "wholeCategory": categories  
    })


def create_listing(request):
    if request.method == "POST": 
        # Extract form data
        newtitle = request.POST["title"]
        imagelink = request.POST["imagelink"]
        descriptions = request.POST["description"]
        newprice = request.POST["price"]
        category = request.POST["category"]
        categoryGetData = Category.objects.get(name=category)  
        owner = request.user  # Get the logged-in user 

        # Create a new Listing instance and save it to the database
        newListing = Listing(
            title=newtitle,
            imageUrl=imagelink,
            description=descriptions,
            price=float(newprice),
            category=categoryGetData,
            creator=owner
        )
        newListing.save() 

        # Create an initial bid with the starting price and save it
        bidprice = Bid(bidprice=float(newprice), user=owner, listing=newListing)
        bidprice.save()

        # Update the listing price to reflect the initial bid
        newListing.price = bidprice.bidprice
        newListing.save()

        return HttpResponseRedirect(reverse(index))  
    
    else:  
        categories = Category.objects.all()  
        return render(request, "auctions/createlisting.html", {
            "wholeCategory": categories  
        })


def addBidprice(request, category_id):
    newbidprice = float(request.POST["bidprice"])  # Get the new bid price from the form

    # Get the listing by ID
    listData = Listing.objects.get(id=category_id)
    isCreator = request.user.username == listData.creator.username  
    isWatchlist = request.user in listData.watchlist.all() 
    allReview = CommentReview.objects.filter(listing=listData)  

    # Get the current highest bid for the listing
    highestbid = Bid.objects.filter(listing=listData).order_by('-bidprice').first()
    
    # Check if the new bid is higher than the current highest bid
    if highestbid and newbidprice <= highestbid.bidprice:
        return render(request, "auctions/listing.html", {
            "listing": listData,
            "note": "Failed to update the bid.",
            "isCreator": isCreator,
            "WatchList": isWatchlist,
            "allReview": allReview,
            "updatenote": False
        })

    # If the new bid is valid, save it
    newBid = Bid(listing=listData, user=request.user, bidprice=newbidprice)
    newBid.save()
    listData.price = newbidprice 
    listData.save()

    return render(request, "auctions/listing.html", {
        "listing": listData,
        "note": "Your bid has been successfully updated.",
        "isCreator": isCreator,
        "WatchList": isWatchlist,
        "allReview": allReview,
        "updatenote": True
    })


def close_auction(request, category_id):
    listData = Listing.objects.get(id=category_id)  
    listData.isActive = False  
    listData.save()
    isWatchlist = request.user in listData.watchlist.all()  # Check if the listing is in the user's watchlist
    allReview = CommentReview.objects.filter(listing=listData)  # Get all reviews for the listing

    # Get the highest bid for the listing
    highestbid = Bid.objects.filter(listing=listData).order_by('-bidprice').first()  
    isCreator = request.user.username == listData.creator.username  
    isWinner = False  

    # Determine if the current user is the winner
    if highestbid:
        isWinner = highestbid.user == request.user  

    return render(request, "auctions/listing.html", {
        "listing": listData,
        "isCreator": isCreator,
        "isWinner": isWinner,
        "note": "The auction has successfully closed.",
        "WatchList": isWatchlist,
        "allReview": allReview,
        "updatenote": True
    })


def listingPage(request, category_id):
    listData = Listing.objects.get(id=category_id)  
    isWatchlist = request.user in listData.watchlist.all() 
    allReview = CommentReview.objects.filter(listing=listData) 
    isCreator = request.user.username == listData.creator.username  

    # Check if the auction is closed and if the user is the winner
    isWinner = None
    if not listData.isActive: 
        highestbid = Bid.objects.filter(listing=listData).order_by('-bidprice').first() 
        if highestbid:
            isWinner = highestbid.user == request.user  

    return render(request, "auctions/listing.html", {
        "listing": listData,
        "WatchList": isWatchlist,
        "allReview": allReview,
        "isCreator": isCreator,
        "isWinner": isWinner
    })


def watch_list(request):
    byUser = request.user  
    listingData = byUser.watchListing.all()  
    return render(request, "auctions/watchlist.html", {
        "activelistings": listingData  
    })


def addTolist(request, category_id):
    productData = Listing.objects.get(id=category_id)  
    byUser = request.user 
    productData.watchlist.add(byUser) 

    return HttpResponseRedirect(reverse("listing", args=(category_id, )))  


def removeInlist(request, category_id):
    productData = Listing.objects.get(id=category_id)  
    byUser = request.user  
    productData.watchlist.remove(byUser)  
    return HttpResponseRedirect(reverse("listing", args=(category_id, ))) 

def comment_review(request, category_id):
    byUser = request.user  
    productData = Listing.objects.get(id=category_id)  
    review = request.POST['newReview']  

    newReview = CommentReview(  
        # Create a new review object
        user=byUser,
        listing=productData,
        content=review
    )
    
    newReview.save()  

    return HttpResponseRedirect(reverse("listing", args=(category_id, )))  


def showCategory(request, category_name):
    category = Category.objects.get(name=category_name)  
    activeList = Listing.objects.filter(isActive=True, category=category)  
    categories = Category.objects.all()  
    return render(request, "auctions/index.html", {
        "activelistings": activeList,  
        "wholeCategory": categories  
    })


def login_view(request):
    if request.method == "POST":  
        username = request.POST["username"]  
        password = request.POST["password"]  
        user = authenticate(request, username=username, password=password)  # Attempt to authenticate the user

        if user is not None:  
            login(request, user)  
            return HttpResponseRedirect(reverse("index"))  
        else: 
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."  
            })
    else:  
        return render(request, "auctions/login.html")  



def logout_view(request):
    logout(request)  
    return HttpResponseRedirect(reverse("index"))  



def register(request):
    if request.method == "POST":  
        username = request.POST["username"]  
        email = request.POST["email"] 

        # Ensure the password and confirmation match
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."  
            })

        try:
            # Create the new user
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."  
            })

        login(request, user)  
        return HttpResponseRedirect(reverse("index")) 
    else:
        return render(request, "auctions/register.html")  
