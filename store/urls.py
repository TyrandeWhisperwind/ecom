from django.urls import path
from . import views


urlpatterns=[

path('<int:cat>',views.store,name='store'),
path('<int:cat>/<int:subcat>/',views.store2,name='store2'),
path('<int:pk>/description/',views.slider,name='slider'),
path('cart/',views.cart,name='cart'),
path('checkout/',views.checkout,name='checkout'),
path('update_item/',views.updateItem,name='update_item'),
path('process_order/',views.processOrder,name='process_order'),



]
