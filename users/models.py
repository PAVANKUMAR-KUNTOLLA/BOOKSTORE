from django.db import models
from crum import get_current_user
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from rest_framework.authtoken.models import Token

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email for user must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    updated_at = models.DateTimeField(auto_now=True, editable=False)
    account_terminated = models.BooleanField(default=False, editable=False)

    objects = UserManager()
    
    def __str__(self):
        return self.email

    def users_return(self):
        return User.objects.filter(account_terminated=False)

    def save(self, *args, **kwargs):
       
        if not self.is_active:
            token_ins = Token.objects.filter(user_id=self.id)
            if token_ins:
                token_ins.delete()

        super(User, self).save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     self.account_terminated = True
    #     self.is_active = False
    #     super(User, self).save(*args, **kwargs)
    
class UserProducts(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, editable=False, blank=True, null=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, editable=False)
    is_favourite = models.BooleanField(default=False)
    is_item_in_cart = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)
    view_count =  models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    def __str__(self):
        return str(self.product.title)

    def save(self, *args, **kwargs):
        super(UserProducts, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "User Products"
        unique_together = ['user', 'product']

class UserOrderHistory(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, editable=False)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, editable=False)
    quantity = models.IntegerField(default=1, editable=False)
    price = models.FloatField(default=0, editable=False)
    order_date = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __str__(self):
        return str(self.product.title)

    def save(self, *args, **kwargs):
        super(UserOrderHistory, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "User Order History"
