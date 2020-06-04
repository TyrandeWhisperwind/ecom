import json
from .models import *

def cookieCart(request):

	#Create empty cart for now for non-logged in user
    #the try catch is for in case the first page that gets loads in is the cart template so we create a dummy cart in case it happens
    try:
        #since the cookie is a string we must parse to to a jason type
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('CART:', cart)
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:
        #We use try block to prevent items in cart that may have been removed from causing error
        try:
                print(cart[i])
                for j in cart[i]:
                    print(j)
                    cartItems += cart[i][j]#quqntity
                    product = Product.objects.get(id=i)
                    tcolorsize = TakenColorSize.objects.get(id=j)
                    total = (product.price * cart[i][j])
                    order['get_cart_total'] += total
                    order['get_cart_items'] += cart[i][j]
                    item = {
                        'id':product.id,
                        'product':{'id':product.id,'name':product.name, 'price':product.price,
                        'imageURL':product.imageURL,'color':tcolorsize.color,'size':tcolorsize.size},
                        'quantity':cart[i][j],
                        'digital':product.digital,'get_total':total,
                        'color_size':tcolorsize.id
                        }
                    items.append(item)
                    if product.digital == False:
                        order['shipping'] = True
        except:
                pass

    return {'cartItems':cartItems ,'order':order, 'items':items}



def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems':cartItems ,'order':order, 'items':items}


def guestOrder(request, data):
    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    cookieData = cookieCart(request)
    items = cookieData['items']#use email to trace the user if he ever wants to creat an account then we find and identify him by his email
    customer, created = Customer.objects.get_or_create(email=email,)
    customer.name = name
    customer.save()
    order = Order.objects.create(customer=customer,complete=False,)
    for item in items:
        product = Product.objects.get(id=item['id'])
        tcolorsize = TakenColorSize.objects.get(id=item['color_size'])
        orderItem = OrderItem.objects.create(product=product,order=order,quantity=item['quantity'],color_size=tcolorsize,)
    return customer, order
