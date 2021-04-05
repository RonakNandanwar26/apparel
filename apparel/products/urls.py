from django.urls import path, include
from .views import productcreate,products_list,singleproduct,update_product,delete_product,my_products,search,winter,ratings

app_name = 'Products'

urlpatterns = [
	path('shop/',products_list,name='shop'),
	path('productcreate/',productcreate,name='productcreate'),
	path('singleproduct/<int:pk>/<str:slug>/',singleproduct,name='singleproduct'),
	path('update_product/<int:pk>/', update_product, name='update_product'),
	path('delete_product/<int:pk>/', delete_product, name='delete_product'),
	path('my_products/',my_products,name='my_products'),
	path('search/',search,name='search'),
	path('cart/',include('cart.urls')),
	path('winter/',winter,name='winter'),
	path('ratings/<int:pk>/',ratings,name='ratings'),
]