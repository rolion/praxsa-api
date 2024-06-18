from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CarBrand, CarModel, CarPart, CarModelPart
from .serializers import CarBrandSerializer, CarModelSerializer, CarPartSerializer, CarModelPartSerializer
from rest_framework import status
from django.http import Http404
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist, FieldError


class CarBrand_APIView(APIView, PageNumberPagination):

    def get(self, request, format= None, *args, **kwargs):
        try:
            order=request.query_params.get('orderby')
            brand = CarBrand.objects.all()
            if order:
                brand = brand.order_by(order)
            results = self.paginate_queryset(brand, request, view=self)
            serializer = CarBrandSerializer(results, many=True, context={'request':request})
            return self.get_paginated_response(serializer.data)
        except FieldError as e:
            return Response(data = 'Invalid Field', status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data = '', status= status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, format=None):
        serializer = CarBrandSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CarBrand_Search_Paginated(APIView, PageNumberPagination):
    def get(self, request, format= None, *args, **kwargs):
        try:
            text=request.query_params.get('text')
            order=request.query_params.get('orderby')
            if text:
                brand = CarBrand.objects.filter(name__contains=text)
            else:
                brand= CarBrand.objects.all()
            if order:
                brand = brand.order_by(order)
            results = self.paginate_queryset(brand, request, view=self)
            serializer = CarBrandSerializer(results, many=True, context={'request':request})
            # return Response(data = serializer.data, status= status.HTTP_200_OK)
            return self.get_paginated_response(serializer.data)
        except FieldError as e:
            return Response(data = 'Invalid Field', status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # send error to logger
            print(e)
            return Response(data = '', status= status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class CarBrand_detail(APIView):
    def get(self, request, pk,format= None):
        try:
            brand = CarBrand.objects.get(id = pk)
            serializer = CarBrandSerializer(brand, many=False, context={'request':request})
            return Response(data = serializer.data, status= status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response(data = '', status= status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # send error to logger
            print(e)
            return Response(data = '', status= status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, format= None):
        try:
            brand = CarBrand.objects.get(id = pk)
            serializer = CarBrandSerializer(brand, data={"name":request.query_params.get('name')})
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
    
    def delete(self, request, pk, format= None):
        try:
            brand = CarBrand.objects.get(id = pk)
            brand_model = CarModel.objects.filter(car_brand = brand)
            if len(brand_model) > 0:
                return Response(data= f'no se puede eliminar la marca {brand.name}, ya que existen modelos relacionados con la marca', status=status.HTTP_400_BAD_REQUEST)
            else:
                brand.delete()
                return Response(data = '', status=status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist as e:
            return Response(data = '', status= status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # send error to logger
            print(e)
            return Response(data = '', status= status.HTTP_500_INTERNAL_SERVER_ERROR)

# class CarBrandListCreate(generics.ListCreateAPIView):
#     queryset = CarBrand.objects.all()
#     serializer_class = CarBrandSerializer

# class CarBrandDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = CarBrand.objects.all()
#     serializer_class = CarBrandSerializer

# class CarModelListCreate(generics.ListCreateAPIView):
#     queryset = CarModel.objects.all()
#     serializer_class = CarModelSerializer

# class CarModelDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = CarModel.objects.all()
#     serializer_class = CarModelSerializer

# class CarPartListCreate(generics.ListCreateAPIView):
#     queryset = CarPart.objects.all()
#     serializer_class = CarPartSerializer

# class CarPartDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = CarPart.objects.all()
#     serializer_class = CarPartSerializer

# class CarModelPartListCreate(generics.ListCreateAPIView):
#     queryset = CarModelPart.objects.all()
#     serializer_class = CarModelPartSerializer

# class CarModelPartDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = CarModelPart.objects.all()
#     serializer_class = CarModelPartSerializer