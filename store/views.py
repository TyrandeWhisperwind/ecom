from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart,cartData,guestOrder

# if producted deleted then check cart cuz it throws price error
def store(request,cat):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	products = Product.objects.filter(category=cat)
	#if category doesnt exits then show all categories
	cat = Category.objects.filter(id=cat).count()
	if cat == 0:
		products=Product.objects.all()

	categories=Category.objects.all()
	context = {'products':products, 'cartItems':cartItems,'categories':categories}
	return render(request, 'store/store.html', context)

def store2(request,cat,subcat):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	products = Product.objects.filter(category=cat,sub_category=subcat)
	#if category doesnt exits then show all categories
	cat = Category.objects.filter(id=cat).count()
	subcat =SubCategory.objects.filter(id=subcat).count()
	if cat == 0 or subcat == 0:
		products=Product.objects.all()
	categories=Category.objects.all()
	context = {'products':products, 'cartItems':cartItems,'categories':categories}
	return render(request, 'store/store.html', context)



def cart(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	categories=Category.objects.all()


	context = {'items':items, 'order':order, 'cartItems':cartItems,'categories':categories}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	categories=Category.objects.all()


	context = {'items':items, 'order':order, 'cartItems':cartItems,'categories':categories}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	"""
	You specified order_item.quantity += 1, This is okay until 2 people click "Add to cart" at the same time or a user clicks very fast that the first request isn't finished, This is a race condition and should be avoided. Like this

	from django.db.models import F

	order_item.quantity = F('quantity') + 1
	"""

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.now().timestamp()
	data = json.loads(request.body)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id
	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(customer=customer,order=order,address=data['shipping']['address'],city=data['shipping']['city'],state=data['shipping']['state'],zipcode=data['shipping']['zipcode'],)

	return JsonResponse('Payment submitted..', safe=False)
