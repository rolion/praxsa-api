from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import CarModelPart
from ..serializers import CarModelPartSerializer
from rest_framework import status
from django.http import Http404
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist, FieldError
from django.db.models import Q
from ..util.numbers import is_number_tryexcept


class CarModelPart_APIView(APIView, PageNumberPagination):

    def get(self, request, format= None, *args, **kwargs):
        try:
            order=request.query_params.get('orderby')
            is_enable = request.query_params.get('is_enable')
            car_model_part = CarModelPart.objects.select_related('car_model', 'car_part').all()
            if order:
                car_model_part = car_model_part.order_by(order)
            if is_enable is not None:
                car_model_part = car_model_part.filter(is_enable = is_enable.lower() in ['true', '1'])
            serializer = CarModelPartSerializer(car_model_part, many=True, context={'request':request})
            return Response(data = serializer.data, status= status.HTTP_200_OK)
        except FieldError as e:
            return Response(data = 'Invalid Field', status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(data = '', status= status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, format=None):
        serializer = CarModelPartSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CarModelPart_Search_Paginated(APIView, PageNumberPagination):
    def get(self, request, format= None, *args, **kwargs):
        try:
            text=request.query_params.get('text')
            order=request.query_params.get('orderby')
            if text:
                if is_number_tryexcept(text):
                    brand = CarModelPart.objects.select_related('car_model', 'car_part').filter(Q(width=text) | Q(length=text) | Q(installation_price = text))
                else:
                    brand = CarModelPart.objects.select_related('car_model', 'car_part').filter(Q(car_model__name__contains=text) | Q(car_part__name__contains=text))

            else:
                brand= CarModelPart.objects.select_related('car_model', 'car_part').all()
            if order:
                brand = brand.order_by(order)
            results = self.paginate_queryset(brand, request, view=self)
            serializer = CarModelPartSerializer(results, many=True, context={'request':request})
            # return Response(data = serializer.data, status= status.HTTP_200_OK)
            return self.get_paginated_response(serializer.data)
        except FieldError as e:
            return Response(data = 'Invalid Field', status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # send error to logger
            print(e)
            return Response(data = '', status= status.HTTP_500_INTERNAL_SERVER_ERROR)


class CarModelPart_detail(APIView):
    def get(self, request, pk,format= None):
        try:
            car_model_part = CarModelPart.objects.select_related('car_model', 'car_part').get(id = pk)
            serializer = CarModelPartSerializer(car_model_part, many=False, context={'request':request})
            return Response(data = serializer.data, status= status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response(data = '', status= status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # send error to logger
            print(e)
            return Response(data = '', status= status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, format= None):
        try:
            car_model_part = CarModelPart.objects.get(id = pk)
            data = request.data
            serializer = CarModelPartSerializer(car_model_part, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response(data = '', status= status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # send error to logger
            print(e)
            return Response(data = '', status= status.HTTP_500_INTERNAL_SERVER_ERROR)