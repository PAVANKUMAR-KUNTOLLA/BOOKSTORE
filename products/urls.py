from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('api/v1/products/', products),
    path('api/v1/edit_product/',edit_product),
    path('api/v1/record_visit_history/', record_visit_history),
    path('api/v1/place_order/', place_order),
]