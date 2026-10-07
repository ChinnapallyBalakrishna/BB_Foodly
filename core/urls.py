from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    

    path(
        'restaurants/<int:pk>/',
        views.restaurant_detail,
        name='restaurant_detail'
    ),

    path(
        'cart/',
        views.cart_view,
        name='cart'
    ),

    path(
        'cart/add/<int:food_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/increase/<int:item_id>/',
        views.increase_cart,
        name='increase_cart'
    ),

    path(
        'cart/decrease/<int:item_id>/',
        views.decrease_cart,
        name='decrease_cart'
    ),

    path(
        'cart/remove/<int:item_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        "address/add/",
        views.add_address,
        name="add_address"
    ),

    path(
        "address/delete/<int:address_id>/",
        views.delete_address,
        name="delete_address"
    ),

    path(
        'order-success/<str:order_number>/',
        views.order_success,
        name='order_success'
    ),

    path(
        'orders/',
        views.my_orders,
        name='my_orders'
    ),

    path(
        'orders/<str:order_number>/',
        views.order_detail,
        name='order_detail'
    ),

    path(
        "orders/<str:order_number>/track/",
        views.track_order,
        name="track_order"
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # Wishlist
    path(
        'wishlist/',
        views.wishlist_view,
        name='wishlist'
    ),

    path(
        'wishlist/toggle/<int:food_id>/',
        views.toggle_wishlist,
        name='toggle_wishlist'
    ),
]