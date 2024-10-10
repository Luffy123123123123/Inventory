from datetime import datetime 
import json
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.db.models import Q
import logging
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import Itemserializers
from .models import Items

inventory_log= logging.getLogger('default')


# Create your views here.
class AddItemApiView(APIView):
    """
        Register API endpoint
    """

    serializer_class = Itemserializers
    permission_classes = (permissions.IsAuthenticated,)
    @swagger_auto_schema(request_body=Itemserializers)
    def post(self, request):
        try:
            if request.body:
                decoded_data = request.body.decode('utf-8')
                json_data = json.loads(decoded_data)
                if not Items.objects.filter(name = json_data['name']).first():
                    serializer = Itemserializers(data=json_data)
                    if serializer.is_valid():
                        serializer.save()  # Save the new post instance
                        inventory_log.info("item created")
                        return Response({'success': True,'status': 200, 'item': serializer.data}, status=200)
                    inventory_log.debug(str(serializer.errors))
                    return JsonResponse({'success': False,'status': 400, 'error':serializer.errors}, status=400)
                inventory_log.debug('item already exists')
                return JsonResponse({'success': False,'status': 400, 'error':'item already exist.'}, status=400)
            inventory_log.error('POST request body is empty.')  
            return JsonResponse({'success': False,'status': 400, 'error':'POST request body is empty.'}, status=400)
        except Exception as e:
            inventory_log.error(str(e), exc_info=True)
            return JsonResponse({'success': False,'status': 400, 'error':str(e)}, status=400)
        
    
        
class GetItemsAPIView(APIView):
    serializer_class = Itemserializers
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id):
        try:
            item = Items.objects.get(id=id)
            serializer = Itemserializers(item)
            return Response({'success': True,'status': 200, 'item': serializer.data}, status=200)
        except Items.DoesNotExist:
            inventory_log.debug(f'Item with id {id} does not exist.')
            return JsonResponse({'success': False,'status': 404, 'error':'Item not found.'}, status=404)
        except Exception as e:
            inventory_log.error(str(e), exc_info=True)
            return JsonResponse({'success': False,'status': 400, 'error':str(e)}, status=400)
        

class UpdateItemsAPIView(APIView):
    serializer_class = Itemserializers
    permission_classes = (permissions.IsAuthenticated,)
    @swagger_auto_schema(request_body=Itemserializers)

    def put(self, request, id):
        try:
            item = Items.objects.get(id=id)
            serializer = Itemserializers(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                inventory_log.info(f'item with id {id} updated')
                return Response({'success': True,'status': 200, 'item': serializer.data}, status=200)
            return Response({'success': False,'status': 400, 'item': serializer.error}, status=400)
        except Items.DoesNotExist:
            inventory_log.debug(f'Item with id {id} does not exist.')
            return JsonResponse({'success': False,'status': 404, 'error':'Item not found.'}, status=404)
        except Exception as e:
            inventory_log.error(str(e), exc_info=True)
            return JsonResponse({'success': False,'status': 400, 'error':str(e)}, status=500)
        

class DeleteItemsAPIView(APIView):
    serializer_class = Itemserializers
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, id):
        try:
            item = Items.objects.get(id=id)
            item.delete()
            inventory_log.info(f'item with id {id} deleted')
            return Response({'success': True,'status': 200, 'item':'item deleted'}, status=200)
        except Items.DoesNotExist:
            inventory_log.debug(f'Item with id {id} does not exist.')
            return JsonResponse({'success': False,'status': 404, 'error':'Item not found.'}, status=404)
        except Exception as e:
            inventory_log.error(str(e), exc_info=True)
            return JsonResponse({'success': False,'status': 400, 'error':str(e)}, status=400)