from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import validate_email
from rest_framework import serializers
from users.models import User ,UserProducts,UserOrderHistory

class SignupSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    college = serializers.CharField(required=True)
    phone_no = serializers.CharField(required=True)

    def validate_email(self, email):
        is_valid_email = False
        try:
            validate_email(email)
        except Exception as excepted_message:
            raise Exception('Please use valid email for registration.')
            
        if User.objects.filter(email__iexact=email).exists():
            raise Exception('This user already exists. Please sign in.')
        return str(email).strip().lower()

    def save(self):
        name = self.validated_data['name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        phone_no = self.validated_data['phone_no']
        address = self.validated_data['address']
        college = self.validated_data['college']
        
        user = User.objects.create(name=name, email=email,phone_no=phone_no,address=address,college=college)
        user.is_active = True
        user.set_password(password)

        user.save()
        return user

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
    orderHistory = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'name', 'email','address','phone_no','college', 'orderHistory')
        
    def get_orderHistory(self, instance):
        orders = UserOrderHistory.objects.filter(user__id=instance.id).order_by("-order_date").values("id", "product__id", "product__title", "quantity", "order_date")
        for index, each in enumerate(orders):
            orders[index]["order_date"] = each["order_date"].strftime("%d %b %Y")
            orders[index]["title"] = each["product__title"]
            del orders[index]["product__title"]
            orders[index]["product_id"] = each["product__id"]
            del orders[index]["product__id"]
        return orders