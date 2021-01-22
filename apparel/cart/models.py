from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.core.validators import MinValueValidator
# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=0)
    status = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + '-' + self.products.name



class Order(models.Model):
	cust_id = models.ForeignKey(User,on_delete=models.CASCADE)
	cart_ids=models.CharField(max_length=250)
	product_ids=models.CharField(max_length=250)
	invoice_id=models.CharField(max_length=250)
	status=models.BooleanField(default=False)
	processed_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.cust_id.username