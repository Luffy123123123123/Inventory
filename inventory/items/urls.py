from django.urls import path
from .views import *

urlpatterns = [
    path('add', AddItemApiView.as_view()),
    path('get/<int:id>', GetItemsAPIView.as_view()),
    path('edit/<int:id>', UpdateItemsAPIView.as_view()),
    path('delete/<int:id>', DeleteItemsAPIView.as_view()),
]
