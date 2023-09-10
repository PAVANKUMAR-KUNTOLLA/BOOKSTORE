from django.db import models
from crum import get_current_user
from users.models import User
import datetime

# Create your models here.
def get_image_path(instance, filename):
    return f'user_data/{instance.id}_{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}_{filename}'

class Product(models.Model):
    title = models.CharField(unique=True, max_length=255)
    category = models.ForeignKey('products.Category', on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField()
    price = models.FloatField()
    author = models.CharField(blank=True,max_length=255)
    author_description = models.TextField(blank=True)
    image = models.ImageField(blank=True, null=True, upload_to=get_image_path)
    rating = models.FloatField(null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by_user = models.ForeignKey('users.User', on_delete=models.RESTRICT, editable=False)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not user:
            user=User.objects.get(id=1)
        self.created_by_user = user
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Products"

class Category(models.Model):
    name = models.CharField(unique=True, max_length=255)
    date_time = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey('users.User', on_delete=models.RESTRICT, editable=False)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not user:
            user=User.objects.get(id=1)
        self.created_by_user = user
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"