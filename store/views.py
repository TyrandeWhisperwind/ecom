from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart,cartData,guestOrder
from django.shortcuts import render,redirect
from . import forms
from django.contrib.auth import login,logout
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm



"""
You specified order_item.quantity += 1, This is okay until 2 people click "Add to cart"
at the same time or a user clicks very fast that the first request isn't finished,
This is a race condition and should be avoided. Like this
from django.db.models import F
order_item.quantity = F('quantity') + 1

email field
"""


def logout_view(request):
    if request.method=='POST':
        logout(request)
        return redirect(reverse('store', kwargs={"cat":0}))


def signup_view(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories=Category.objects.all()
    product = Product.objects.all()
    if request.method=='POST':
        #getting the passed values in the request and putting them in a new form
        #to check if it is valid or nop
        form=forms.CostumerForm(request.POST)
        if form.is_valid():
            #save user in database plus
            #log user in after signinup....
            user=form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,user)
            #app name plus the name of the url in the view
            return redirect(reverse('store', kwargs={"cat":0}))
        else:
            form=forms.CostumerForm()
            return render(request, 'store/signup.html', { 'form': form,'context':context})
    #if method is get then send the forms
    #if the form is not valid it ll resend the form also
    else:
        #instanciate a form
        form=forms.CostumerForm()
    #send the form the the html template
    context = {'form': form,'product':product, 'cartItems':cartItems,'categories':categories}
    return  render(request, 'store/signup.html', context)

def login_view(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories=Category.objects.all()
    product = Product.objects.all()
    print(cartItems)
    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            #redirect user to login
            user = form.get_user()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,user)
            #check where the user was trying to go with the next value in the url
            if 'next' in request.POST:
                #'next' is the name of the input in the html
                return redirect(request.POST.get('next'))
            else:
                return redirect(reverse('store', kwargs={"cat":0}))
    else:
        form=AuthenticationForm()
    context = {'form':form,'product':product, 'cartItems':cartItems,'categories':categories}
    return render(request,'store/login.html',context)

def slider(request,pk):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	product = Product.objects.get(id=pk)
	categories=Category.objects.all()
	context = {'product':product, 'cartItems':cartItems,'categories':categories}
	return render(request, 'store/slider.html', context)

def store(request,cat):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.filter(category=cat)
    #if category doesnt exits then show all products
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
	#if category doesnt exits then show all products
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
	val=data['val']
	colorsize=data['colorsize']
	print('Action:', action)
	print('Product:', productId)
	customer = request.user.customer
	product = Product.objects.get(id=productId)
	tcolorsize = TakenColorSize.objects.get(id=colorsize)

	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	#here add color size
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product,color_size=tcolorsize)
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + int(val))
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

	if float(total) == float(order.get_cart_total):
		order.complete = True
		order.save()
		if order.shipping == True:
			ShippingAddress.objects.create(customer=customer,order=order,address=data['shipping']['address'],city=data['shipping']['city'],state=data['shipping']['state'],zipcode=data['shipping']['zipcode'],)
	return JsonResponse('Payment submitted..', safe=False)
