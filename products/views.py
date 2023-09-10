import os
import io
import re
import copy
import json
import datetime
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status #pagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from users.models import User
from Store.settings import MEDIA_ROOT

from .helpers import get_products, update_user_product_info, place_order_helper, record_visit_history_helper

def index(request):
    return render(request, 'index.html')

def serve_app(request, exception):
    return render(request, 'index.html')


@api_view(["GET","POST"])
# #@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def products(request):
    try:
        if request.method == "GET":
            products = get_products(request)
            context = {"data":products, "status_flag":True, "status":status.HTTP_200_OK, "message":None}
            return Response(data=context, status=status.HTTP_200_OK)
        
        elif request.method == "POST":
            product = get_products(request)
            context = {"data":product, "status_flag":True, "status":status.HTTP_200_OK, "message":None}
            return Response(data=context, status=status.HTTP_200_OK)
        
        else:
            context = {"data":None, "status_flag":False, "status":status.HTTP_405_METHOD_NOT_ALLOWED, "message":"Only POST & GET Method available"}
            return Response(data=context, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as excepted_message:
        print(str(excepted_message))
        context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":str(excepted_message)}
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
#@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def record_visit_history(request):
    try:
        if request.method == "GET":
            context = {"data":None, "status_flag":False, "status":status.HTTP_405_METHOD_NOT_ALLOWED, "message":"Only GET Method available"}
            return Response(data=context, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        elif request.method == "POST":
            message = record_visit_history_helper(request)
            context = {"data":None, "status_flag":True, "status":status.HTTP_200_OK, "message":message}
            return Response(data=context, status=status.HTTP_200_OK)
        
        else:
            context = {"data":None, "status_flag":False, "status":status.HTTP_405_METHOD_NOT_ALLOWED, "message":"Only POST Method available"}
            return Response(data=context, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    except Exception as excepted_message:
        print(str(excepted_message))
        context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":str(excepted_message)}
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
# @authentication_classes([TokenAuthenticationSafe])
@permission_classes([IsAuthenticated])
def edit_product(request):
    try:
        if request.method == "GET":
            context = {"data":None, "status_flag":False, "status":status.HTTP_405_METHOD_NOT_ALLOWED, "message":"Only GET Method available"}
            return Response(data=context, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        elif request.method == "POST":
            update_user_product_info(request)
            data = get_products(request)
            context = {"data":data, "status_flag":True, "status":status.HTTP_200_OK, "message":None}
            return Response(data=context, status=status.HTTP_200_OK)
        
        else:
            context = {"data":None, "status_flag":False, "status":status.HTTP_405_METHOD_NOT_ALLOWED, "message":"Only POST Method available"}
            return Response(data=context, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as excepted_message:
        print(str(excepted_message))
        context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":str(excepted_message)}
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(["POST"])
#@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def place_order(request):
    try:
        if request.method == "GET":
            context = {"data":None, "status_flag":False, "status":status.HTTP_405_METHOD_NOT_ALLOWED, "message":"Only GET Method available"}
            return Response(data=context, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        elif request.method == "POST":
            place_order_helper(request)
            data = get_products(request)
            context = {"data":data, "status_flag":True, "status":status.HTTP_200_OK, "message":"Order Placed Successfully"}
            return Response(data=context, status=status.HTTP_200_OK)
        
        else:
            context = {"data":None, "status_flag":False, "status":status.HTTP_405_METHOD_NOT_ALLOWED, "message":"Only POST Method available"}
            return Response(data=context, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as excepted_message:
        print(str(excepted_message))
        context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":str(excepted_message)}
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)