from .models import Cart
from menu.models import FoodItem

def get_cart_counter(request):
    cart_count=0
    if request.user.is_authenticated:
        try:
            cart_item = Cart.objects.filter(user=request.user)
            if cart_item:
                for cart_items in cart_item:
                    cart_count+=cart_items.quantity
            else:
                cart_count=0
        except:
            cart_count=0
    return dict(cart_count =cart_count)