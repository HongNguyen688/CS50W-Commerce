from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name="index"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name="createlisting"),
    path("category/all", views.index, name="showAllCategory"),
    path("listing/<int:category_id>/", views.listingPage, name="listing"),
    path("addbid/<int:category_id>/", views.addBidprice, name="addbid"),
    path("closeAuction/<int:category_id>/", views.close_auction, name="closeAuction"),
    path("addReview/<int:category_id>/", views.comment_review, name="addReview"),
    path("addProduct/<int:category_id>/", views.addTolist, name="addProduct"),
    path("removeProduct/<int:category_id>/", views.removeInlist, name="removeProduct"),
    path("watchlist", views.watch_list, name="watchlist"),
    path("category/<str:category_name>/", views.showCategory, name="showCategory"),
]


