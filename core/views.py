from .models import (
    Address,
    Cart,
    CartItem,
    Category,
    Coupon,
    FoodItem,
    Order,
    OrderItem,
    Restaurant,
    Wishlist,
)

from django.db.models import Q
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    Address,
    Cart,
    CartItem,
    Category,
    Coupon,
    FoodItem,
    Order,
    OrderItem,
    Restaurant,
    Wishlist,
)


# =========================================================
# HOME
# =========================================================
def home(request):
    search = request.GET.get("search", "").strip()
    cuisine = request.GET.get("cuisine", "").strip()
    price = request.GET.get("price", "").strip()
    category_name = request.GET.get("category", "").strip()

    restaurants = Restaurant.objects.all()
    for restaurant in restaurants:
        restaurant.bg_food = (
            FoodItem.objects
            .filter(
                restaurant=restaurant,
                is_available=True
            )
            .exclude(image="")
            .first()
        )
    categories = Category.objects.filter(is_active=True)

    # Get distinct cuisines for the filter dropdown
    cuisines = (
        Restaurant.objects
        .exclude(cuisine="")
        .values_list("cuisine", flat=True)
        .distinct()
    )

    # Start with all available food items
    food_items = FoodItem.objects.select_related(
        "restaurant",
        "category"
    ).filter(
        is_available=True
    )

    # -------------------------------------------------
    # SEARCH FILTER
    # Searches BOTH food name and restaurant name
    # -------------------------------------------------
    if search:
        food_items = food_items.filter(
            Q(name__icontains=search) |
            Q(restaurant__name__icontains=search)
        )

    # -------------------------------------------------
    # CUISINE FILTER
    # -------------------------------------------------
    if cuisine:
        food_items = food_items.filter(
            restaurant__cuisine__icontains=cuisine
        )

    # -------------------------------------------------
    # CATEGORY FILTER
    # -------------------------------------------------
    if category_name:
        food_items = food_items.filter(
            category__name__iexact=category_name
        )

    # -------------------------------------------------
    # PRICE FILTER
    # -------------------------------------------------
    if price:
        if price == "under_200":
            food_items = food_items.filter(
                price__lt=200
            )

        elif price == "200_500":
            food_items = food_items.filter(
                price__gte=200,
                price__lte=500
            )

        elif price == "above_500":
            food_items = food_items.filter(
                price__gt=500
            )

    # -------------------------------------------------
    # CATEGORY FOOD COUNT
    # -------------------------------------------------
    for category in categories:
        category.food_count = FoodItem.objects.filter(
            category=category,
            is_available=True
        ).count()

        category.bg_food = (
            FoodItem.objects
            .filter(
                category=category,
                is_available=True
            )
            .exclude(image="")
            .first()
        )
    # -------------------------------------------------
    # RENDER HOME PAGE
    # -------------------------------------------------
    return render(
        request,
        "core/home.html",
        {
            "restaurants": restaurants,
            "categories": categories,
            "cuisines": cuisines,
            "food_items": food_items,

            "search": search,
            "selected_cuisine": cuisine,
            "selected_price": price,
            "selected_category": category_name,
        }
    )

def search_results(request):
    search = request.GET.get("search", "").strip()
    cuisine = request.GET.get("cuisine", "").strip()
    price = request.GET.get("price", "").strip()
    category_name = request.GET.get("category", "").strip()

    food_items = FoodItem.objects.select_related(
        "restaurant",
        "category"
    ).filter(
        is_available=True
    )

    # Search food name OR restaurant name
    if search:
        food_items = food_items.filter(
            Q(name__icontains=search) |
            Q(restaurant__name__icontains=search)
        )

    # Cuisine
    if cuisine:
        food_items = food_items.filter(
            restaurant__cuisine__icontains=cuisine
        )

    # Category
    if category_name:
        food_items = food_items.filter(
            category__name__iexact=category_name
        )

    # Price
    if price:
        if price == "under_200":
            food_items = food_items.filter(
                price__lt=200
            )

        elif price == "200_500":
            food_items = food_items.filter(
                price__gte=200,
                price__lte=500
            )

        elif price == "above_500":
            food_items = food_items.filter(
                price__gt=500
            )

    return render(
        request,
        "core/search_results.html",
        {
            "food_items": food_items,
            "search": search,
            "selected_cuisine": cuisine,
            "selected_price": price,
            "selected_category": category_name,
        }
    )

# =========================================================
# RESTAURANT DETAIL
# =========================================================

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(
        Restaurant,
        pk=pk
    )

    food_items = FoodItem.objects.filter(
        restaurant=restaurant
    ).select_related(
        "category"
    )

    wishlist_ids = set()

    if request.user.is_authenticated:
        wishlist_ids = set(
            Wishlist.objects.filter(
                user=request.user
            ).values_list(
                "food_item_id",
                flat=True
            )
        )

    return render(
        request,
        "core/restaurant_detail.html",
        {
            "restaurant": restaurant,
            "food_items": food_items,
            "wishlist_ids": wishlist_ids,
        }
    )


# =========================================================
# ADD TO CART
# =========================================================

@login_required
def add_to_cart(request, food_id):
    food_item = get_object_or_404(
        FoodItem,
        pk=food_id
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        food_item=food_item,
        defaults={
            "quantity": 1
        }
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(
        request,
        f"{food_item.name} added to your cart."
    )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home"
        )
    )


# =========================================================
# CART
# =========================================================

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = CartItem.objects.filter(
        cart=cart
    ).select_related(
        "food_item",
        "food_item__restaurant",
        "food_item__category"
    )

    subtotal = Decimal("0.00")

    # IMPORTANT:
    # Do NOT assign to item.total_price.
    # total_price is already a read-only property
    # inside the CartItem model.

    for item in cart_items:
        subtotal += (
            item.food_item.price * item.quantity
        )

    if subtotal > Decimal("0.00"):
        delivery_fee = Decimal("40.00")
    else:
        delivery_fee = Decimal("0.00")

    discount = Decimal("0.00")

    total = (
        subtotal
        + delivery_fee
        - discount
    )

    return render(
        request,
        "core/cart.html",
        {
            "cart": cart,
            "cart_items": cart_items,
            "subtotal": subtotal,
            "delivery_fee": delivery_fee,
            "discount": discount,
            "total": total,
        }
    )


# =========================================================
# INCREASE CART ITEM
# =========================================================

@login_required
def increase_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        pk=item_id,
        cart__user=request.user
    )

    cart_item.quantity += 1
    cart_item.save()

    return redirect("cart")


# =========================================================
# DECREASE CART ITEM
# =========================================================

@login_required
def decrease_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        pk=item_id,
        cart__user=request.user
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("cart")


# =========================================================
# REMOVE FROM CART
# =========================================================

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        pk=item_id,
        cart__user=request.user
    )

    cart_item.delete()

    messages.success(
        request,
        "Item removed from cart."
    )

    return redirect("cart")


# =========================================================
# CHECKOUT
# =========================================================
@login_required
def checkout(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = CartItem.objects.filter(
        cart=cart
    ).select_related(
        "food_item",
        "food_item__restaurant"
    )

    if not cart_items.exists():

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect("cart")

    addresses = Address.objects.filter(
        user=request.user
    )

    # Calculate subtotal
    subtotal = Decimal("0.00")

    for item in cart_items:

        subtotal += (
            item.food_item.price * item.quantity
        )

    # Delivery charge
    delivery_fee = Decimal("40.00")

    # Discount
    discount = Decimal("0.00")

    # Final total
    total = (
        subtotal
        + delivery_fee
        - discount
    )

    # Place order
    if request.method == "POST":

        address_id = request.POST.get(
            "address"
        )

        payment_method = request.POST.get(
            "payment_method",
            "COD"
        )

        print(
            "DEBUG address_id =",
            address_id
        )

        if not address_id:

            messages.error(
                request,
                "Please select a delivery address."
            )

            return redirect("checkout")

        address = get_object_or_404(
            Address,
            pk=address_id,
            user=request.user
        )

        # Create unique order number
        order_number = (
            f"FD{request.user.id}"
            f"{Order.objects.count() + 1001}"
        )

        with transaction.atomic():

            # Create order
            order = Order.objects.create(
                user=request.user,
                address=address,
                order_number=order_number,
                subtotal=subtotal,
                total_amount=total,
                payment_method=payment_method,
                status="PLACED"
            )

            # Create order items
            for item in cart_items:

                OrderItem.objects.create(
                    order=order,
                    food_item=item.food_item,
                    quantity=item.quantity,
                    price=item.food_item.price
                )

            # Clear cart
            cart_items.delete()

        messages.success(
            request,
            "Your order has been placed successfully."
        )

        return redirect(
            "order_success",
            order_number=order.order_number
        )

    # Checkout page
    return render(
        request,
        "core/checkout.html",
        {
            "cart": cart,
            "cart_items": cart_items,
            "addresses": addresses,
            "subtotal": subtotal,
            "delivery_fee": delivery_fee,
            "discount": discount,
            "total": total,
        }
    )

@login_required
def add_address(request):

    if request.method == "POST":

        full_name = request.POST.get(
            "full_name",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        address_line = request.POST.get(
            "address_line",
            ""
        ).strip()

        city = request.POST.get(
            "city",
            ""
        ).strip()

        state = request.POST.get(
            "state",
            ""
        ).strip()

        pincode = request.POST.get(
            "pincode",
            ""
        ).strip()

        if not full_name:
            messages.error(
                request,
                "Please enter your full name."
            )
            return redirect("add_address")

        if not phone:
            messages.error(
                request,
                "Please enter your phone number."
            )
            return redirect("add_address")

        if not address_line:
            messages.error(
                request,
                "Please enter your address."
            )
            return redirect("add_address")

        if not city:
            messages.error(
                request,
                "Please enter your city."
            )
            return redirect("add_address")

        if not state:
            messages.error(
                request,
                "Please enter your state."
            )
            return redirect("add_address")

        if not pincode:
            messages.error(
                request,
                "Please enter your pincode."
            )
            return redirect("add_address")

        Address.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address_line=address_line,
            city=city,
            state=state,
            pincode=pincode
        )

        messages.success(
            request,
            "Address added successfully!"
        )

        return redirect("checkout")

    return render(
        request,
        "core/add_address.html"
    )


# =========================================================
# DELETE ADDRESS
# =========================================================

@login_required
def delete_address(request, address_id):

    address = get_object_or_404(
        Address,
        id=address_id,
        user=request.user
    )

    if request.method == "POST":

        address.delete()

        messages.success(
            request,
            "Address deleted successfully!"
        )

    return redirect("checkout")
# =========================================================
# ORDER SUCCESS
# =========================================================

@login_required
def order_success(request, order_number):
    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user
    )

    return render(
        request,
        "core/order_success.html",
        {
            "order": order
        }
    )


# =========================================================
# MY ORDERS
# =========================================================

@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related(
        "items",
        "items__food_item"
    )

    return render(
        request,
        "core/my_orders.html",
        {
            "orders": orders
        }
    )


# =========================================================
# ORDER DETAIL
# =========================================================

@login_required
def order_detail(request, order_number):
    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user
    )

    order_items = OrderItem.objects.filter(
        order=order
    ).select_related(
        "food_item"
    )

    return render(
        request,
        "core/order_detail.html",
        {
            "order": order,
            "order_items": order_items,
        }
    )


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        if not username:
            messages.error(
                request,
                "Username is required."
            )

            return redirect("register")

        if not password:
            messages.error(
                request,
                "Password is required."
            )

            return redirect("register")

        if password != confirm_password:
            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect("register")

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect("register")

        if email and User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Email already exists."
            )

            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(
            request,
            user
        )

        messages.success(
            request,
            "Account created successfully."
        )

        return redirect("home")

    return render(
        request,
        "core/register.html"
    )


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            messages.success(
                request,
                f"Welcome back, {user.username}."
            )

            return redirect("home")

        messages.error(
            request,
            "Invalid username or password."
        )

        return redirect("login")

    return render(
        request,
        "core/login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect("home")


# =========================================================
# WISHLIST
# =========================================================

@login_required
def wishlist_view(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related(
        "food_item",
        "food_item__restaurant",
        "food_item__category"
    )

    return render(
        request,
        "core/wishlist.html",
        {
            "wishlist_items": wishlist_items
        }
    )


# =========================================================
# TOGGLE WISHLIST
# =========================================================

@login_required
def toggle_wishlist(request, food_id):

    food_item = get_object_or_404(
        FoodItem,
        pk=food_id
    )

    wishlist_item = Wishlist.objects.filter(
        user=request.user,
        food_item=food_item
    ).first()

    if wishlist_item:

        wishlist_item.delete()

        messages.success(
            request,
            f"{food_item.name} removed from favorites."
        )

    else:

        Wishlist.objects.create(
            user=request.user,
            food_item=food_item
        )

        messages.success(
            request,
            f"{food_item.name} added to favorites."
        )

    referer = request.META.get(
        "HTTP_REFERER",
        ""
    )

    if "/wishlist/" in referer:
        return redirect("wishlist")

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home"
        )
    )
# =========================================================
# TRACK ORDER
# =========================================================

@login_required
def track_order(request, order_number):

    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user
    )

    tracking_steps = [
        {
            "status": "PLACED",
            "title": "Order Placed",
            "description": "Your order has been received successfully.",
            "icon": "📝",
        },
        {
            "status": "CONFIRMED",
            "title": "Order Confirmed",
            "description": "The restaurant has confirmed your order.",
            "icon": "✅",
        },
        {
            "status": "PREPARING",
            "title": "Preparing Your Food",
            "description": "The restaurant is preparing your delicious food.",
            "icon": "👨‍🍳",
        },
        {
            "status": "OUT_FOR_DELIVERY",
            "title": "Out for Delivery",
            "description": "Your food is on the way to you.",
            "icon": "🛵",
        },
        {
            "status": "DELIVERED",
            "title": "Delivered",
            "description": "Your order has been delivered. Enjoy your meal!",
            "icon": "🎉",
        },
    ]

    status_order = [
        "PLACED",
        "CONFIRMED",
        "PREPARING",
        "OUT_FOR_DELIVERY",
        "DELIVERED",
    ]

    current_status = order.status

    if current_status == "CANCELLED":

        for step in tracking_steps:
            step["completed"] = False
            step["current"] = False

    else:

        if current_status not in status_order:
            current_status = "PLACED"

        current_index = status_order.index(
            current_status
        )

        for index, step in enumerate(tracking_steps):

            step["completed"] = index <= current_index
            step["current"] = index == current_index

    return render(
        request,
        "core/track_order.html",
        {
            "order": order,
            "tracking_steps": tracking_steps,
        }
    )