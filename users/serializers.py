from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import validate_email
from rest_framework import serializers
from users.models import User,UserProducts,UserOrderHistory,UserManager


from djoser import serializers as DjsoerSerializer


class SignupSerializer(DjsoerSerializer.UserCreateSerializer):
    class Meta(DjsoerSerializer.UserCreateSerializer.Meta):
        model = User
    
    

# class SignupSerializer(serializers.Serializer):
#     email = serializers.CharField(required=True)
#     password = serializers.CharField(required=True)
#     name = serializers.CharField(required=True)

#     def validate_email(self, email):
#         is_valid_email = False
#         try:
#             validate_email(email)
#         except Exception as excepted_message:
#             raise Exception('Please use valid email for registration.')
            
#         if User.objects.filter(email__iexact=email).exists():
#             raise Exception('This user already exists. Please sign in.')
#         return str(email).strip().lower()

#     def save(self):
#         name = self.validated_data['name']
#         email = self.validated_data['email']
#         password = self.validated_data['password']

#         user = User.objects.create(name=name, email=email)
#         user.is_active = True
#         user.set_password(password)

#         user.save()
#         return user

class AuthenticationSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']
        if email and password:
            user = authenticate(request=self.context['request'], email=str(email).strip().lower(), password=password)
            print(user)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')

            if not user.is_active:
                msg = _('User is set Not Active')
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')
        
class UserProductsSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    visited_at = serializers.SerializerMethodField()
    class Meta:
        model = UserProducts
        fields = ['id', 'title', 'is_favourite', 'is_item_in_cart', 'view_count', 'is_brought', 'visited_at'] 
        

    def get_title(self, instance):
        return instance.product.title

    def get_visited_at(self, instance):
        return instance.updated_at.strftime("%d %b %Y")


class UserOrderHistorySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    order_date = serializers.SerializerMethodField()
    class Meta:
        model = UserOrderHistory
        fields = ['id', 'title', 'price', 'quantity', 'order_date']

    def get_title(self, instance):
        return instance.product.title
    
    def get_order_date(self, instance):
        return instance.order_date.strftime("%d %b %Y")

class UserProfileSerializer(serializers.ModelSerializer):
    history = serializers.SerializerMethodField()
    order_history = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'name', 'email', "history", "order_history"]
        
    def get_history(self, instance):
        return_dict = []
        products = instance.products.all().order_by("-updated_at")
        for each_product in products:
            each_dict = {"id":each_product.id, "title":each_product.product.title, "view_count":each_product.view_count}
            each_dict["visited_at"] = each_product.updated_at.strftime("%d %b %Y")
            return_dict.append(each_dict)
            
        return return_dict
            
    def get_order_history(self, instance):
        return_dict = []
        products = instance.orders.all().order_by("-order_date")
        for each_product in products:
            each_dict = {"id":each_product.id, "title":each_product.product.title, "price":each_product.product.price, "quantity":each_product.quantity}
            each_dict["order_date"] = each_product.order_date.strftime("%d %b %Y")
            return_dict.append(each_dict)
            
        return return_dict