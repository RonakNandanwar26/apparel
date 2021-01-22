from django.shortcuts import render,get_object_or_404,reverse
from django.contrib.auth.decorators import login_required
from .models import Cart,Order
from django.contrib import messages 
from django.contrib.auth.models import User
from products.models import Product
from django.http import JsonResponse,HttpResponse
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
import random
from django.views.decorators.csrf import csrf_exempt
# Create your views here.



@login_required
def add_to_cart(request):
    items = Cart.objects.filter(user__id=request.user.id,status=False)
    context = {}
    context['items'] = items
    if request.user.is_authenticated:    
        if request.method == 'POST':
            pid = request.POST["pid"]
            qty = request.POST["qty"]
            is_exist = Cart.objects.filter(products__id=pid,user__id=request.user.id,status=False)
            if len(is_exist)>0:
                messages.error(request,'Item already exist in Cart')
            else:
                product = get_object_or_404(Product,id=pid)
                user = get_object_or_404(User,id=request.user.id)
                c = Cart(user=user,products=product,quantity=qty)
                c.save()
                messages.success(request,'{} Added in your Cart'.format(product.name))
    else:
        context['status'] = 'Please login to view your cart'
    return render(request, 'cart_temp/cart.html',context)




def get_cart_data(request):
    items = Cart.objects.filter(user__id=request.user.id,status=False)
    total,quantity = 0,0
    for i in items:
        total += i.products.price * i.quantity
        quantity += i.quantity
    
    res = {'total':total,'quan':quantity}
    return JsonResponse(res) 
 


def change_quan(request):
    if "quantity" in request.GET:
        cid = request.GET["cid"]   # cid is cart id
        qty = request.GET["quantity"]
        cart_obj = get_object_or_404(Cart,id=cid)
        cart_obj.quantity = qty
        cart_obj.save()
        return JsonResponse(cart_obj.quantity)
    
    if "delete_cart" in request.GET:
        id = request.GET["delete_cart"]
        cart_obj = get_object_or_404(Cart,id=id)
        cart_obj.delete()
        return HttpResponse(1)



def process_payment(request):
    items = Cart.objects.filter(user_id__id=request.user.id,status=False)
    product = ""
    amt = 0
    inv = "INV-"+str(random.randint(1,1000000))
    cart_ids = ""
    p_ids = ""
    for i in items:
        product += str(i.products.name)+"\n"
        p_ids += str(i.products.id)+","
        amt += float(i.products.price)
        inv += str(i.id)
        cart_ids += str(i.id)+","
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(amt),
        'item_name': product,
        'invoice': "Inv- "+inv,
        'notify_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('Home:Products:Cart:payment_done')),
        'cancel_return': 'http://{}{}'.format("127.0.0.1:8000",
                                              reverse('Home:Products:Cart:payment_canceled')),     
    }

    usr = User.objects.get(username=request.user.username)
    ord = Order(cust_id=usr,cart_ids=cart_ids,product_ids=p_ids)
    ord.save()
    ord.invoice_id = str(ord.id)+inv
    ord.save()
    request.session['order_id'] = ord.id


    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'cart_temp/process_payment.html', {'form': form})



@csrf_exempt
def payment_done(request):
    if 'order_id' in request.session:
        order_id = request.session["order_id"]
        order_obj = get_object_or_404(Order,id=order_id)
        order_obj.status = True
        order_obj.save()

        for i in order_obj.cart_ids.split(",")[:-1]:
            cart_object = Cart.objects.get(id=i)
            cart_object.status=True
            cart_object.save()
    template = 'cart_temp/payment_success.html'
    return render(request,template)



@csrf_exempt
def payment_canceled(request):
    template = 'cart_temp/payment_failed.html'
    return render(request,template)
