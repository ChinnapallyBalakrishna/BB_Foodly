from django.core.management.base import BaseCommand
from core.models import Restaurant, Category, FoodItem


class Command(BaseCommand):
    help = "Create Foodly demo restaurants, categories and food items."

    def handle(self, *args, **kwargs):

        self.stdout.write(
            self.style.WARNING(
                "Creating Foodly demo data..."
            )
        )

        # ============================================================
        # CATEGORIES
        # ============================================================

        category_names = [
            "Pizza",
            "Burgers",
            "Biryani",
            "Indian",
            "Chinese",
            "Desserts",
            "Beverages",
        ]

        categories = {}

        for name in category_names:

            category, created = Category.objects.get_or_create(
                name=name,
                defaults={
                    "is_active": True,
                }
            )

            categories[name] = category

        # ============================================================
        # RESTAURANTS
        # ============================================================

        restaurants_data = [

            {
                "name": "Spice Garden",
                "description": "Authentic Indian dishes prepared with fresh ingredients.",
                "address": "Banjara Hills",
                "city": "Hyderabad",
                "phone": "9876543210",
                "cuisine": "Indian",
                "rating": 4.6,
                "delivery_time": 30,
                "delivery_fee": 40,
            },

            {
                "name": "Pizza Palace",
                "description": "Freshly baked pizzas with classic and premium toppings.",
                "address": "Madhapur",
                "city": "Hyderabad",
                "phone": "9876543211",
                "cuisine": "Pizza",
                "rating": 4.5,
                "delivery_time": 25,
                "delivery_fee": 30,
            },

            {
                "name": "Biryani House",
                "description": "Hyderabadi-style biryanis with rich spices and authentic flavours.",
                "address": "Tolichowki",
                "city": "Hyderabad",
                "phone": "9876543212",
                "cuisine": "Biryani",
                "rating": 4.8,
                "delivery_time": 35,
                "delivery_fee": 40,
            },

            {
                "name": "Dragon Wok",
                "description": "Popular Chinese favourites made fresh to order.",
                "address": "Hitech City",
                "city": "Hyderabad",
                "phone": "9876543213",
                "cuisine": "Chinese",
                "rating": 4.4,
                "delivery_time": 30,
                "delivery_fee": 35,
            },

            {
                "name": "Burger Hub",
                "description": "Juicy burgers, crispy sides and delicious combos.",
                "address": "Kukatpally",
                "city": "Hyderabad",
                "phone": "9876543214",
                "cuisine": "Burgers",
                "rating": 4.5,
                "delivery_time": 25,
                "delivery_fee": 30,
            },

            {
                "name": "Sweet Treats",
                "description": "Cakes, brownies, ice creams and delicious desserts.",
                "address": "Jubilee Hills",
                "city": "Hyderabad",
                "phone": "9876543215",
                "cuisine": "Desserts",
                "rating": 4.7,
                "delivery_time": 20,
                "delivery_fee": 25,
            },

            {
                "name": "Fresh Sip",
                "description": "Refreshing beverages, shakes, coffees and coolers.",
                "address": "Gachibowli",
                "city": "Hyderabad",
                "phone": "9876543216",
                "cuisine": "Beverages",
                "rating": 4.3,
                "delivery_time": 20,
                "delivery_fee": 20,
            },

        ]

        restaurants = {}

        for data in restaurants_data:

            restaurant, created = Restaurant.objects.get_or_create(
                name=data["name"],
                defaults=data
            )

            if not created:

                for field, value in data.items():
                    setattr(
                        restaurant,
                        field,
                        value
                    )

                restaurant.save()

            restaurants[data["name"]] = restaurant

        # ============================================================
        # FOOD DATA
        # ============================================================

        food_data = [

            # ========================================================
            # PIZZA PALACE
            # ========================================================

            (
                "Pizza Palace",
                "Pizza",
                "Margherita Pizza",
                "Classic pizza with tomato, mozzarella and basil.",
                299,
                True,
                True
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Farmhouse Pizza",
                "Loaded with fresh vegetables and mozzarella.",
                349,
                True,
                True
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Paneer Tikka Pizza",
                "Indian-style pizza topped with paneer tikka.",
                379,
                True,
                True
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Chicken Tikka Pizza",
                "Tender chicken tikka with cheese and herbs.",
                399,
                False,
                True
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Chicken Pepperoni Pizza",
                "Classic chicken pepperoni pizza with melted cheese.",
                429,
                False,
                True
            ),

            (
                "Pizza Palace",
                "Pizza",
                "BBQ Chicken Pizza",
                "Smoky BBQ chicken with onions and cheese.",
                449,
                False,
                False
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Cheese Burst Pizza",
                "Extra cheese with a rich cheese-filled crust.",
                399,
                True,
                True
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Mexican Veg Pizza",
                "Spicy vegetables, jalapenos and cheese.",
                359,
                True,
                False
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Double Cheese Pizza",
                "Extra mozzarella and cheddar cheese.",
                329,
                True,
                False
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Chicken Supreme Pizza",
                "Chicken, peppers, onions and premium cheese.",
                479,
                False,
                True
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Veggie Delight Pizza",
                "Fresh vegetables with herbs and mozzarella.",
                339,
                True,
                False
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Cheese Margherita Pizza",
                "Classic tomato and mozzarella pizza with extra cheese.",
                319,
                True,
                True
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Paneer Makhani Pizza",
                "Creamy paneer makhani toppings with mozzarella cheese.",
                399,
                True,
                True
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Tandoori Paneer Pizza",
                "Tandoori paneer, onions and capsicum with cheese.",
                389,
                True,
                True
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Chicken Tandoori Pizza",
                "Tandoori chicken pieces with onions and mozzarella.",
                429,
                False,
                True
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Peri Peri Chicken Pizza",
                "Spicy peri peri chicken with cheese and vegetables.",
                449,
                False,
                True
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Chicken Sausage Pizza",
                "Chicken sausage, cheese and herbs on a crispy base.",
                419,
                False,
                False
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Corn Cheese Pizza",
                "Sweet corn and extra mozzarella cheese.",
                329,
                True,
                False
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Capsicum Onion Pizza",
                "Fresh capsicum and onions with Italian herbs.",
                319,
                True,
                False
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Spicy Paneer Pizza",
                "Spicy paneer, jalapenos and cheese on a crispy base.",
                379,
                True,
                True
            ),

            (
                "Pizza Palace",
                "Pizza",
                "Ultimate Chicken Pizza",
                "Loaded chicken pizza with multiple toppings and cheese.",
                499,
                False,
                True
            ),

            # ========================================================
            # BURGER HUB
            # ========================================================

            (
                "Burger Hub",
                "Burgers",
                "Classic Veg Burger",
                "Crispy vegetable patty with fresh vegetables.",
                149,
                True,
                True
            ),

            (
                "Burger Hub",
                "Burgers",
                "Classic Chicken Burger",
                "Crispy chicken patty with lettuce and sauce.",
                189,
                False,
                True
            ),

            (
                "Burger Hub",
                "Burgers",
                "Cheese Burger",
                "Classic burger with a generous cheese slice.",
                179,
                True,
                True
            ),

            (
                "Burger Hub",
                "Burgers",
                "Double Cheese Burger",
                "Double patty with double cheese.",
                249,
                False,
                True
            ),

            (
                "Burger Hub",
                "Burgers",
                "Paneer Burger",
                "Grilled paneer patty with fresh vegetables.",
                199,
                True,
                False
            ),

            (
                "Burger Hub",
                "Burgers",
                "Spicy Chicken Burger",
                "Spicy chicken patty with signature sauce.",
                219,
                False,
                True
            ),

            (
                "Burger Hub",
                "Burgers",
                "BBQ Chicken Burger",
                "Chicken burger with smoky BBQ sauce.",
                229,
                False,
                False
            ),

            (
                "Burger Hub",
                "Burgers",
                "Mushroom Burger",
                "Grilled mushroom patty with cheese.",
                189,
                True,
                False
            ),

            (
                "Burger Hub",
                "Burgers",
                "Crispy Chicken Burger",
                "Crunchy fried chicken with creamy sauce.",
                209,
                False,
                True
            ),

            (
                "Burger Hub",
                "Burgers",
                "Loaded Burger",
                "Loaded burger with cheese, vegetables and sauces.",
                259,
                False,
                False
            ),

            (
                "Burger Hub",
                "Burgers",
                "Burger Combo",
                "Burger served with fries and a soft drink.",
                299,
                False,
                True
            ),

            # ========================================================
            # BIRYANI HOUSE
            # ========================================================

            (
                "Biryani House",
                "Biryani",
                "Hyderabadi Chicken Biryani",
                "Classic Hyderabadi chicken dum biryani.",
                299,
                False,
                True
            ),

            (
                "Biryani House",
                "Biryani",
                "Chicken Dum Biryani",
                "Slow-cooked chicken and aromatic basmati rice.",
                299,
                False,
                True
            ),

            (
                "Biryani House",
                "Biryani",
                "Mutton Biryani",
                "Tender mutton cooked with fragrant basmati rice.",
                399,
                False,
                True
            ),

            (
                "Biryani House",
                "Biryani",
                "Egg Biryani",
                "Aromatic biryani served with boiled eggs.",
                249,
                False,
                False
            ),

            (
                "Biryani House",
                "Biryani",
                "Veg Biryani",
                "Fragrant rice cooked with fresh vegetables.",
                229,
                True,
                True
            ),

            (
                "Biryani House",
                "Biryani",
                "Paneer Biryani",
                "Paneer and aromatic rice cooked with Indian spices.",
                279,
                True,
                False
            ),

            (
                "Biryani House",
                "Biryani",
                "Fry Piece Biryani",
                "Crispy chicken pieces served with dum biryani.",
                349,
                False,
                True
            ),

            (
                "Biryani House",
                "Biryani",
                "Chicken 65 Biryani",
                "Chicken 65 pieces combined with spicy biryani rice.",
                369,
                False,
                True
            ),

            (
                "Biryani House",
                "Biryani",
                "Boneless Chicken Biryani",
                "Tender boneless chicken with fragrant rice.",
                379,
                False,
                True
            ),

            (
                "Biryani House",
                "Biryani",
                "Special Biryani",
                "Restaurant special biryani with premium toppings.",
                449,
                False,
                True
            ),

            (
                "Biryani House",
                "Biryani",
                "Family Pack Biryani",
                "Large family-sized biryani pack.",
                799,
                False,
                True
            ),

            (
                "Biryani House",
                "Biryani",
                "Andhra Chicken Biryani",
                "Spicy Andhra-style chicken biryani with aromatic rice.",
                319,
                False,
                True
            ),

            (
                "Biryani House",
                "Biryani",
                "Mutton Dum Biryani",
                "Slow-cooked mutton with fragrant basmati rice and spices.",
                429,
                False,
                True
            ),

            (
                "Biryani House",
                "Biryani",
                "Mutton Fry Biryani",
                "Spicy mutton fry pieces served with flavorful biryani rice.",
                449,
                False,
                True
            ),

            (
                "Biryani House",
                "Biryani",
                "Chicken Keema Biryani",
                "Flavorful minced chicken cooked with aromatic biryani rice.",
                349,
                False,
                False
            ),

            (
                "Biryani House",
                "Biryani",
                "Kolkata Chicken Biryani",
                "Kolkata-style chicken biryani with potato and aromatic rice.",
                329,
                False,
                False
            ),

            (
                "Biryani House",
                "Biryani",
                "Hyderabadi Mutton Biryani",
                "Traditional Hyderabadi mutton biryani cooked with rich spices.",
                429,
                False,
                True
            ),

            (
                "Biryani House",
                "Biryani",
                "Chicken Tikka Biryani",
                "Tender chicken tikka pieces combined with fragrant biryani rice.",
                389,
                False,
                True
            ),

            (
                "Biryani House",
                "Biryani",
                "Paneer Dum Biryani",
                "Soft paneer cooked with aromatic basmati rice and spices.",
                299,
                True,
                False
            ),

            (
                "Biryani House",
                "Biryani",
                "Mushroom Biryani",
                "Fresh mushrooms cooked with fragrant basmati rice and spices.",
                269,
                True,
                False
            ),

            (
                "Biryani House",
                "Biryani",
                "Family Chicken Biryani",
                "Large chicken biryani portion suitable for a family meal.",
                899,
                False,
                True
            ),

            # ========================================================
            # SPICE GARDEN
            # ========================================================

            (
                "Spice Garden",
                "Indian",
                "Paneer Butter Masala",
                "Paneer cooked in a rich tomato butter gravy.",
                249,
                True,
                True
            ),

            (
                "Spice Garden",
                "Indian",
                "Chicken Tikka",
                "Char-grilled chicken marinated with Indian spices.",
                299,
                False,
                True
            ),

            (
                "Spice Garden",
                "Indian",
                "Butter Chicken",
                "Creamy tomato-based chicken curry.",
                329,
                False,
                True
            ),

            (
                "Spice Garden",
                "Indian",
                "Dal Tadka",
                "Yellow lentils tempered with Indian spices.",
                179,
                True,
                False
            ),

            (
                "Spice Garden",
                "Indian",
                "Palak Paneer",
                "Paneer cooked in creamy spinach gravy.",
                239,
                True,
                True
            ),

            (
                "Spice Garden",
                "Indian",
                "Chole Masala",
                "Spiced chickpeas cooked in Punjabi style.",
                189,
                True,
                False
            ),

            (
                "Spice Garden",
                "Indian",
                "Kadai Chicken",
                "Chicken cooked with capsicum and aromatic spices.",
                319,
                False,
                True
            ),

            (
                "Spice Garden",
                "Indian",
                "Tandoori Chicken",
                "Chicken roasted in a traditional tandoor.",
                349,
                False,
                True
            ),

            (
                "Spice Garden",
                "Indian",
                "Garlic Naan",
                "Soft naan topped with garlic and butter.",
                79,
                True,
                True
            ),

            (
                "Spice Garden",
                "Indian",
                "Butter Naan",
                "Soft Indian flatbread with butter.",
                69,
                True,
                False
            ),

            (
                "Spice Garden",
                "Indian",
                "Veg Thali",
                "Complete Indian meal with rice, dal, curry and bread.",
                299,
                True,
                True
            ),

            (
                "Spice Garden",
                "Indian",
                "Shahi Paneer",
                "Soft paneer cooked in a creamy royal-style gravy.",
                259,
                True,
                True
            ),

            (
                "Spice Garden",
                "Indian",
                "Paneer Tikka",
                "Marinated paneer grilled with onions and capsicum.",
                279,
                True,
                True
            ),

            (
                "Spice Garden",
                "Indian",
                "Chicken Curry",
                "Traditional Indian chicken curry cooked with aromatic spices.",
                299,
                False,
                True
            ),

            (
                "Spice Garden",
                "Indian",
                "Chicken Korma",
                "Creamy chicken curry prepared with rich Indian spices.",
                329,
                False,
                False
            ),

            (
                "Spice Garden",
                "Indian",
                "Matar Paneer",
                "Paneer and green peas cooked in tomato-based gravy.",
                229,
                True,
                True
            ),

            (
                "Spice Garden",
                "Indian",
                "Rajma Masala",
                "Red kidney beans cooked in a flavorful Indian gravy.",
                189,
                True,
                False
            ),

            (
                "Spice Garden",
                "Indian",
                "Aloo Gobi",
                "Potatoes and cauliflower cooked with Indian spices.",
                179,
                True,
                False
            ),

            (
                "Spice Garden",
                "Indian",
                "Malai Kofta",
                "Soft vegetable and paneer koftas in creamy gravy.",
                269,
                True,
                True
            ),

            (
                "Spice Garden",
                "Indian",
                "Jeera Rice",
                "Fragrant basmati rice cooked with cumin seeds.",
                149,
                True,
                True
            ),

            (
                "Spice Garden",
                "Indian",
                "Tandoori Paneer",
                "Grilled paneer marinated with yogurt and Indian spices.",
                289,
                True,
                True
            ),

            # ========================================================
            # DRAGON WOK
            # ========================================================

            (
                "Dragon Wok",
                "Chinese",
                "Veg Hakka Noodles",
                "Stir-fried noodles with fresh vegetables.",
                199,
                True,
                True
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Chicken Hakka Noodles",
                "Stir-fried noodles with tender chicken.",
                249,
                False,
                True
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Chicken Fried Rice",
                "Classic fried rice with chicken and vegetables.",
                249,
                False,
                True
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Veg Fried Rice",
                "Fried rice loaded with fresh vegetables.",
                199,
                True,
                False
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Veg Manchurian",
                "Crispy vegetable balls in Manchurian sauce.",
                219,
                True,
                True
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Chicken Manchurian",
                "Chicken pieces tossed in spicy Manchurian sauce.",
                269,
                False,
                True
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Paneer Chilli",
                "Paneer tossed with peppers and chilli sauce.",
                239,
                True,
                False
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Chicken Chilli",
                "Chicken cooked with peppers and chilli sauce.",
                279,
                False,
                True
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Schezwan Noodles",
                "Spicy noodles tossed in Schezwan sauce.",
                229,
                True,
                True
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Spring Rolls",
                "Crispy rolls filled with seasoned vegetables.",
                179,
                True,
                False
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Chicken Momos",
                "Steamed dumplings filled with seasoned chicken.",
                219,
                False,
                True
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Schezwan Fried Rice",
                "Spicy fried rice prepared with Schezwan sauce and vegetables.",
                229,
                True,
                True
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Chicken Schezwan Rice",
                "Spicy Schezwan fried rice with tender chicken pieces.",
                279,
                False,
                True
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Veg Chilli",
                "Crispy vegetables tossed with peppers and chilli sauce.",
                209,
                True,
                False
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Honey Chilli Potato",
                "Crispy potatoes tossed in sweet and spicy sauce.",
                219,
                True,
                True
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Chicken Lollipop",
                "Crispy chicken lollipops served with spicy dipping sauce.",
                299,
                False,
                True
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Chicken Dragon Roll",
                "Crispy chicken rolls with vegetables and signature sauce.",
                259,
                False,
                False
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Veg Chow Mein",
                "Stir-fried chow mein noodles with fresh vegetables.",
                199,
                True,
                False
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Chicken Chow Mein",
                "Stir-fried noodles with chicken and fresh vegetables.",
                249,
                False,
                True
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Veg Manchow Soup",
                "Hot and spicy vegetable soup with crispy noodles.",
                159,
                True,
                True
            ),

            (
                "Dragon Wok",
                "Chinese",
                "Chicken Manchow Soup",
                "Spicy chicken soup topped with crispy noodles.",
                189,
                False,
                True
            ),

            # ========================================================
            # SWEET TREATS
            # ========================================================

            (
                "Sweet Treats",
                "Desserts",
                "Chocolate Brownie",
                "Rich and fudgy chocolate brownie.",
                129,
                True,
                True
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Chocolate Cake",
                "Soft chocolate cake with chocolate cream.",
                149,
                True,
                True
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Red Velvet Cake",
                "Classic red velvet cake with cream cheese frosting.",
                179,
                True,
                True
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Gulab Jamun",
                "Soft milk dumplings soaked in sugar syrup.",
                99,
                True,
                True
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Rasmalai",
                "Soft cheese dumplings in sweet saffron milk.",
                139,
                True,
                False
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Chocolate Mousse",
                "Creamy chocolate mousse dessert.",
                159,
                True,
                True
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Vanilla Ice Cream",
                "Classic creamy vanilla ice cream.",
                99,
                True,
                False
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Chocolate Ice Cream",
                "Rich chocolate ice cream.",
                119,
                True,
                True
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Brownie with Ice Cream",
                "Warm brownie served with vanilla ice cream.",
                199,
                True,
                True
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Fruit Custard",
                "Fresh fruits served with creamy custard.",
                129,
                True,
                False
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Cheesecake",
                "Creamy cheesecake with a biscuit base.",
                199,
                True,
                True
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Strawberry Ice Cream",
                "Creamy strawberry ice cream with fresh strawberry flavour.",
                129,
                True,
                True
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Butterscotch Ice Cream",
                "Creamy butterscotch ice cream with crunchy caramel pieces.",
                139,
                True,
                True
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Mango Ice Cream",
                "Rich mango ice cream with fruity mango flavour.",
                129,
                True,
                True
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Pista Ice Cream",
                "Creamy pistachio ice cream with roasted pistachio pieces.",
                149,
                True,
                False
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Black Currant Ice Cream",
                "Smooth black currant ice cream with berry flavour.",
                149,
                True,
                False
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Cookies and Cream",
                "Creamy ice cream with crunchy chocolate cookie pieces.",
                159,
                True,
                True
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Caramel Sundae",
                "Vanilla ice cream topped with rich caramel sauce.",
                179,
                True,
                True
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Chocolate Sundae",
                "Chocolate ice cream with chocolate sauce and toppings.",
                189,
                True,
                True
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Kulfi",
                "Traditional Indian frozen dessert with cardamom and nuts.",
                129,
                True,
                True
            ),

            (
                "Sweet Treats",
                "Desserts",
                "Falooda",
                "Refreshing dessert with ice cream, vermicelli and nuts.",
                199,
                True,
                True
            ),

            # ========================================================
            # FRESH SIP
            # ========================================================

            (
                "Fresh Sip",
                "Beverages",
                "Fresh Lime Soda",
                "Refreshing lime soda served chilled.",
                79,
                True,
                True
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Cold Coffee",
                "Chilled creamy coffee with ice.",
                129,
                True,
                True
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Chocolate Shake",
                "Thick chocolate milkshake.",
                159,
                True,
                True
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Vanilla Shake",
                "Creamy vanilla milkshake.",
                149,
                True,
                False
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Mango Shake",
                "Fresh mango blended into a creamy shake.",
                159,
                True,
                True
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Strawberry Shake",
                "Fresh strawberry milkshake.",
                169,
                True,
                False
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Masala Chai",
                "Indian tea prepared with aromatic spices.",
                59,
                True,
                True
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Filter Coffee",
                "South Indian style filter coffee.",
                69,
                True,
                True
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Iced Tea",
                "Refreshing chilled lemon iced tea.",
                99,
                True,
                False
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Watermelon Cooler",
                "Fresh watermelon drink served chilled.",
                129,
                True,
                True
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Mint Mojito",
                "Refreshing mint and lime cooler.",
                139,
                True,
                True
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Blue Lagoon",
                "Chilled citrus cooler with a refreshing taste.",
                149,
                True,
                True
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Green Apple Cooler",
                "Refreshing green apple flavoured cooler.",
                149,
                True,
                True
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Peach Iced Tea",
                "Cold peach-flavoured iced tea served with ice.",
                119,
                True,
                False
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Lemon Iced Tea",
                "Refreshing lemon tea served chilled.",
                109,
                True,
                True
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Orange Cooler",
                "Fresh orange-based chilled summer cooler.",
                129,
                True,
                True
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Virgin Mojito",
                "Refreshing mint, lime and soda cooler.",
                149,
                True,
                True
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Strawberry Cooler",
                "Sweet strawberry cooler served chilled.",
                139,
                True,
                False
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Mango Fizz",
                "Mango-based fizzy summer drink.",
                149,
                True,
                True
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Cola Chill",
                "Classic chilled cola-style soft drink.",
                79,
                True,
                False
            ),

            (
                "Fresh Sip",
                "Beverages",
                "Lemon Soda",
                "Sparkling lemon soda served with ice.",
                89,
                True,
                True
            ),
        ]

        # ============================================================
        # IMAGE KEYWORDS
        # ============================================================

        image_keywords = {

            "Pizza":
                "pizza",

            "Burgers":
                "burger",

            "Biryani":
                "biryani",

            "Indian":
                "indian-food",

            "Chinese":
                "chinese-food",

            "Desserts":
                "ice-cream",

            "Beverages":
                "cold-drink",
        }

        # ============================================================
        # CREATE FOOD ITEMS
        # ============================================================

        for index, data in enumerate(
            food_data,
            start=1
        ):

            (
                restaurant_name,
                category_name,
                food_name,
                description,
                price,
                vegetarian,
                popular
            ) = data

            restaurant = restaurants[
                restaurant_name
            ]

            category = categories[
                category_name
            ]

            keyword = image_keywords[
                category_name
            ]

            image_url = (
                f"https://loremflickr.com/"
                f"1200/800/"
                f"{keyword}?lock={index}"
            )

            food_item, created = FoodItem.objects.get_or_create(

                restaurant=restaurant,

                name=food_name,

                defaults={

                    "category": category,

                    "description": description,

                    "price": price,

                    "is_vegetarian": vegetarian,

                    "is_available": True,

                    "is_popular": popular,

                    "image_url": image_url,
                }
            )

            if not created:

                food_item.category = category

                food_item.description = description

                food_item.price = price

                food_item.is_vegetarian = vegetarian

                food_item.is_available = True

                food_item.is_popular = popular

                food_item.image_url = image_url

                food_item.save()

        # ============================================================
        # RESTAURANT IMAGES
        # ============================================================

        restaurant_images = {

            "Spice Garden":
                "https://loremflickr.com/1200/800/indian-restaurant?lock=201",

            "Pizza Palace":
                "https://loremflickr.com/1200/800/pizza-restaurant?lock=202",

            "Biryani House":
                "https://loremflickr.com/1200/800/biryani-restaurant?lock=203",

            "Dragon Wok":
                "https://loremflickr.com/1200/800/chinese-restaurant?lock=204",

            "Burger Hub":
                "https://loremflickr.com/1200/800/burger-restaurant?lock=205",

            "Sweet Treats":
                "https://loremflickr.com/1200/800/dessert-restaurant?lock=206",

            "Fresh Sip":
                "https://loremflickr.com/1200/800/drinks-restaurant?lock=207",
        }

        for name, url in restaurant_images.items():

            restaurant = restaurants[name]

            restaurant.image_url = url

            restaurant.save()

        # ============================================================
        # CATEGORY IMAGES
        # ============================================================

        category_images = {

            "Pizza":
                "https://loremflickr.com/1200/800/pizza?lock=301",

            "Burgers":
                "https://loremflickr.com/1200/800/burger?lock=302",

            "Biryani":
                "https://loremflickr.com/1200/800/biryani?lock=303",

            "Indian":
                "https://loremflickr.com/1200/800/indian-food?lock=304",

            "Chinese":
                "https://loremflickr.com/1200/800/chinese-food?lock=305",

            "Desserts":
                "https://loremflickr.com/1200/800/ice-cream?lock=306",

            "Beverages":
                "https://loremflickr.com/1200/800/cold-drink?lock=307",
        }

        for name, url in category_images.items():

            category = categories[name]

            category.image_url = url

            category.save()

        # ============================================================
        # FINAL COUNTS
        # ============================================================

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "Foodly demo data created successfully."
            )
        )

        self.stdout.write("")

        self.stdout.write(
            f"Restaurants: {Restaurant.objects.count()}"
        )

        self.stdout.write(
            f"Categories: {Category.objects.count()}"
        )

        self.stdout.write(
            f"Food items: {FoodItem.objects.count()}"
        )

        self.stdout.write("")

        for category_name in category_names:

            count = FoodItem.objects.filter(
                category__name=category_name
            ).count()

            self.stdout.write(
                f"{category_name}: {count} items"
            )

        self.stdout.write("")

        for restaurant_name in restaurants:

            count = FoodItem.objects.filter(
                restaurant__name=restaurant_name
            ).count()

            self.stdout.write(
                f"{restaurant_name}: {count} items"
            )

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "Foodly seed data completed."
            )
        )