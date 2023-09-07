# import os
# import io
# import re
# import copy
# import datetime

# from django.shortcuts import render
# import pandas as pd
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from .serializers import *
# from django.core.mail import EmailMessage
# from rest_framework.authtoken.models import Token

# # reset password imports
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

# # Create your views here.
# def index(request):
#     return render(request, 'index.html')

# @api_view(['POST'])
# def signup(request):
#     try:
#         if request.method == "POST":
#             data = request.data.copy()
#             signup_serializer = SignupSerializer(
#                 data=data, context={'request': request})
#             signup_serializer.is_valid(raise_exception=True)

#             if data["passwordConfirmation"] != data["password"]:
#                 context = None
#                 status_flag = False
#                 message = "Password mismatch"
#                 status_code = status.HTTP_406_NOT_ACCEPTABLE
#                 context = {"data":context, "status_flag":status_flag, "status":status_code, "message":message}
#                 return Response(status=status_code, data= context)

#             # print(data)
#             signup_serializer = SignupSerializer(
#                 data=data, context={'request': request})
#             signup_serializer.is_valid(raise_exception=True)
#             print(signup_serializer.data)
#             signup_serializer.save()
#             user_data = signup_serializer.data

#             context = None
#             status_flag = True
#             message = "Success"
#             status_code = status.HTTP_200_OK
#             context = {"data":context, "status_flag":status_flag, "status":status_code, "message":message}
#             return Response(status=status_code, data= context)

#         else:
#             context = None
#             status_flag = False
#             message = "Only Post Method available"
#             status_code = status.HTTP_405_METHOD_NOT_ALLOWED
#             context = {"data":context, "status_flag":status_flag, "status":status_code, "message":message}
#             return Response(status=status_code, data= context)

#     except Exception as excepted_message:
#         print(excepted_message)
#         context = None
#         status_flag = False
#         message = str(excepted_message)
#         status_code = status.HTTP_400_BAD_REQUEST
#         context = {"data":context, "status_flag":status_flag, "status":status_code, "message":message}
#         return Response(status=status_code, data= context)

# @api_view(['POST'])
# def login(request):
#     data = request.data.copy()
#     login_serializer = AuthenticationSerializer(
#         data=data, context={'request': request})
#     login_serializer.is_valid(raise_exception=True)
#     user = login_serializer.validated_data['user']
#     token, created = Token.objects.get_or_create(user=user)
#     data = {
#         'token': token.key
#     }
#     context = data
#     status_flag = True
#     message = None
#     status_code = status.HTTP_200_OK
#     context = {"data":context, "status_flag":status_flag, "status":status_code, "message":message}
#     return Response(status=status_code, data= context)

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def logout(request):
#     print(request.user)
#     try:
#         token = Token.objects.get(user=request.user)
#     except Token.DoesNotExist:
#         token = None

#     if token:
#         token.delete()
    
#     context = None
#     status_flag = False
#     message = None
#     status_code = status.HTTP_204_NO_CONTENT
#     context = {"data":context, "status_flag":status_flag, "status":status_code, "message":message}
#     return Response(status=status_code, data= context)

# @api_view(['GET', ])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def profile(request):
#     try:
#         user = request.user
#         if request.method == 'GET':
#             profile_data = UserProfileSerializer(instance=user).data

#             context = profile_data
#             status_flag = True
#             message = None
#             status_code = status.HTTP_200_OK
#             context = {"data":context, "status_flag":status_flag, "status":status_code, "message":message}
#             return Response(status=status_code, data= context)

#         else:
#             context = None
#             status_flag = False
#             message = "Only Get Method available"
#             status_code = status.HTTP_405_METHOD_NOT_ALLOWED
#             context = {"data":context, "status_flag":status_flag, "status":status_code, "message":message}
#             return Response(status=status_code, data= context)

#     except Exception as excepted_message:
#         print(excepted_message)
#         context = None
#         status_flag = False
#         message = str(excepted_message)
#         status_code = status.HTTP_400_BAD_REQUEST
#         context = {"data":context, "status_flag":status_flag, "status":status_code, "message":message}
#         return Response(status=status_code, data= context)

# @api_view(['POST'])
# def forgot_password(request):
#     data = request.data.copy()
#     try:
#         if User.objects.filter(email=data['email']).exists():
#             user = User.objects.get(email=data['email'])
#             if not user.is_active:
#                 context = None
#                 status_flag = False
#                 message = 'User is set Not Active'
#                 status_code = status.HTTP_400_BAD_REQUEST
#                 context = {"data":context, "status_flag":status_flag, "status":status_code, "message":message}
#                 return Response(status=status_code, data= context)
                                                
#             uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
#             token = PasswordResetTokenGenerator().make_token(user)               
#             # reset_password_url = f'{get_current_site(request=request).domain}/reset-password/{uidb64}/{token}'        
#             reset_password_url = request.build_absolute_uri(f'/reset-password/{uidb64}/{token}')  

#             email_body = 'Hello, \n Use link below to reset your password  \n' + \
#                     reset_password_url

#             subject = "Reset your passsword"            
#             from_email = DEFAULT_FROM_EMAIL
#             to = [data["email"], ]
#             email = EmailMessage(subject, email_body, from_email, to)
#             email.send()

#             context = None
#             status_flag = True
#             message = 'We have sent reset code. Please check your email'
#             status_code = status.HTTP_200_OK
#             context = {"data":context, "status_flag":status_flag, "status":status_code, "message":message}
#             return Response(status=status_code, data= context)
        
#         else:
#             context =  None
#             status_flag = False
#             message = "User not found. Not a valid email"
#             status_code = status.HTTP_404_NOT_FOUND
#             context = {"data":context, "status_flag":status_flag, "status":status_code, "message":message}
#             return Response(status=status_code, data= context)

#     except Exception as excepted_message:
#         print(excepted_message)
#         context = None
#         status_flag = False
#         message = "Password Reset Failed"
#         status_code = status.HTTP_400_BAD_REQUEST
#         context = {"data":context, "status_flag":status_flag, "status":status_code, "message":message}
#         return Response(status=status_code, data= context)



# @api_view(['POST'])
# def reset_password(request):
#     data = request.data.copy()
#     try:
#         id = smart_str(urlsafe_base64_decode(data["uidb64"]))
#         user = User.objects.get(id=id)

#         if not PasswordResetTokenGenerator().check_token(user, data["token"]):
#             context = None
#             status_flag = False
#             message = "Reset token expired, please request a new one"
#             status_code = status.HTTP_400_BAD_REQUEST
#             context = {"data":context, "status_flag":status_flag, "status":status_code, "message":message}
#             return Response(status=status_code, data= context)

#         user.set_password(data["password"])
#         user.save()

#         context = None
#         status_flag = True
#         message = 'Password reset success'
#         status_code = status.HTTP_200_OK
#         context = {"data":context, "status_flag":status_flag, "status":status_code, "message":message}
#         return Response(status=status_code, data= context)

#     except Exception as excepted_message:
#         print(excepted_message)
#         context =  None
#         status_flag = False
#         message = "Password Reset Failed"
#         status_code = status.HTTP_400_BAD_REQUEST
#         context = {"data":context, "status_flag":status_flag, "status":status_code, "message":message}
#         return Response(status=status_code, data= context)