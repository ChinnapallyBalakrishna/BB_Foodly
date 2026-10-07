from django.contrib import admin

from .models import (
    Restaurant,
    Category,
    FoodItem,
    Address,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Review,
    Coupon,
    Wishlist,
)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "cuisine",
        "city",
        "rating",
        "delivery_time",
        "is_open",
        "is_active",
    )
    list_filter = (
        "cuisine",
        "city",
        "is_open",
        "is_active",
    )
    search_fields = (
        "name",
        "cuisine",
        "city",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "restaurant",
        "category",
        "price",
        "is_vegetarian",
        "is_available",
        "is_popular",
    )
    list_filter = (
        "category",
        "restaurant",
        "is_vegetarian",
        "is_available",
        "is_popular",
    )
    search_fields = (
        "name",
        "restaurant__name",
        "category__name",
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "phone",
        "city",
        "state",
        "pincode",
        "is_default",
    )
    list_filter = (
        "city",
        "state",
        "is_default",
    )
    search_fields = (
        "full_name",
        "phone",
        "city",
        "pincode",
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "created_at",
        "updated_at",
    )
    search_fields = ("user__username",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "cart",
        "food_item",
        "quantity",
    )
    search_fields = (
        "cart__user__username",
        "food_item__name",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "user",
        "restaurant",
        "total_amount",
        "payment_method",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "payment_method",
        "restaurant",
    )
    search_fields = (
        "order_number",
        "user__username",
        "restaurant__name",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "food_name",
        "price",
        "quantity",
    )
    search_fields = (
        "order__order_number",
        "food_name",
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "restaurant",
        "rating",
        "created_at",
    )
    list_filter = (
        "rating",
        "restaurant",
    )
    search_fields = (
        "user__username",
        "restaurant__name",
        "comment",
    )


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "discount_percentage",
        "max_discount",
        "minimum_order_amount",
        "is_active",
        "valid_from",
        "valid_until",
    )
    list_filter = ("is_active",)
    search_fields = ("code",)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "food_item",
        "created_at",
    )
    search_fields = (
        "user__username",
        "food_item__name",
    )
    list_filter = (
        "food_item__restaurant",
        "food_item__category",
    )