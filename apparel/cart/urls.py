from django.urls import path
from .views import add_to_cart,get_cart_data,change_quan,process_payment,payment_done,payment_canceled

app_name = 'Cart'


urlpatterns = [
	path('',add_to_cart,name='add_to_cart'),
	path('get_cart_data/',get_cart_data,name='get_cart_data'),
	path('change_quan/',change_quan,name='change_quan'),
	path('process_payment/',process_payment,name='process_payment'),
	path('payment_done/',payment_done,name='payment_done'),
	path('payment_canceled/',payment_canceled,name='payment_canceled'),
]