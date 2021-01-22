from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import os
import random
from django.db.models.signals import pre_save
from apparel.utils import unique_slug_generator
from PIL import Image
from imagekit import processors
# import cv2
# from sorl.thumbnail import ImageField, get_thumbnail
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=50)

    def __str__(self):
        return self.name


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return ext


def upload_product_image_path(instance, filename):
    new_filename = instance.name
    ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "Products/{final_filename}".format(final_filename=final_filename)



class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    slug = models.SlugField(blank=True, unique=True)
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=50)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=0)
    availability = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    image1 = models.ImageField(default='default.jpg', upload_to=upload_product_image_path)
    image2 = models.ImageField(default='default.jpg',upload_to=upload_product_image_path, null=True, blank=True)
    image3 = models.ImageField(default='default.jpg',upload_to=upload_product_image_path, null=True, blank=True)
    image4 = models.ImageField(default='default.jpg',upload_to=upload_product_image_path, null=True, blank=True)
    features = models.TextField(default='')
    smart1 = ImageSpecField(source='image1', processors=[ResizeToFill(250, 350)], format='JPEG', options={'quality': 99})
    smart2 = ImageSpecField(source='image2', processors=[ResizeToFill(250, 350)], format='JPEG', options={'quality': 99})
    smart3 = ImageSpecField(source='image3', processors=[ResizeToFill(250, 350)], format='JPEG', options={'quality': 99})
    smart4 = ImageSpecField(source='image4', processors=[ResizeToFill(250, 350)], format='JPEG', options={'quality': 99})


    def __str__(self):
        return self.name

   



def product_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_reciever, sender=Product)
