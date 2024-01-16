from .models import Cart
from menu.models import FoodItem
from marketplace.models import Tax

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

def get_cart_amount(request):
    subtotal=0
    tax=0
    grand_total=0
    tax_dict={}
    if request.user.is_authenticated:
        
        cart_item = Cart.objects.filter(user=request.user)
        #looping cart items to get food items
        for item in cart_item:
            foodItem = FoodItem.objects.get(pk=item.fooditem.id)
            print('foodItem',foodItem)
            subtotal+=(foodItem.price * item.quantity)

        #Getting dynamic tax from db
        
        get_tax=Tax.objects.filter(is_active=True)
        
        for i in get_tax:
            tax_type=i.tax_type
            print('tex_type',tax_type)
            tax_percentage=i.tax_percentage
            tax_amount=round((tax_percentage * subtotal)/100,2)
            print('List',tax_type,tax_percentage,tax_amount)
            tax_dict.update({tax_type: {str(tax_percentage):tax_amount}})
            print('Dict',tax_dict)

        tax=0
        for key in tax_dict.values():
            for x in key.values():
                tax = tax + x
        print(tax)

        

        grand_total = subtotal + tax
        #print(subtotal)
        #print(grand_total)
    print('Outside',tax_dict)
    return dict(subtotal=subtotal , tax=tax,grand_total=grand_total,tax_dict=tax_dict)
