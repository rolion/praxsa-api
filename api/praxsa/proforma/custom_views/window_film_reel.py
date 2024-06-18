from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import  WindowFilmReel
from ..serializers import WindowFilmReelSerializer
from rest_framework import status
from django.http import Http404
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist, FieldError


class WindowFilmReel_APIView(APIView, PageNumberPagination):

    def get(self, request, format= None, *args, **kwargs):
        try:
            order=request.query_params.get('orderby')
            is_enable = request.query_params.get('is_enable')
            windos_film_reel = WindowFilmReel.objects.all()
            if order:
                windos_film_reel = windos_film_reel.order_by(order)
            if is_enable is not None:
                windos_film_reel = windos_film_reel.filter(is_enable = is_enable.lower() in ['true', '1'])
            serializer = WindowFilmReelSerializer(windos_film_reel, many=True, context={'request':request})
            return Response(data = serializer.data, status= status.HTTP_200_OK)
        except FieldError as e:
            print(e)
            return Response(data = 'Invalid Field', status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(data = '', status= status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, format=None):
        serializer = WindowFilmReelSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Window_Film_Reel_Search_Paginated(APIView, PageNumberPagination):
    def get(self, request, format= None, *args, **kwargs):
        try:
            text=request.query_params.get('text')
            order=request.query_params.get('orderby')
            if text:
                window_film_reel = WindowFilmReel.objects.filter(name__contains=text)
            else:
                window_film_reel= WindowFilmReel.objects.all()
            if order:
                window_film_reel = window_film_reel.order_by(order)
            results = self.paginate_queryset(window_film_reel, request, view=self)
            serializer = WindowFilmReelSerializer(results, many=True, context={'request':request})
            # return Response(data = serializer.data, status= status.HTTP_200_OK)
            return self.get_paginated_response(serializer.data)
        except FieldError as e:
            return Response(data = 'Invalid Field', status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # send error to logger
            print(e)
            return Response(data = '', status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class Window_Film_detail(APIView):
    def get(self, request, pk,format= None):
        try:
            window_film_reel = WindowFilmReel.objects.get(id = pk)
            serializer = WindowFilmReelSerializer(window_film_reel, many=False, context={'request':request})
            return Response(data = serializer.data, status= status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response(data = '', status= status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # send error to logger
            print(e)
            return Response(data = '', status= status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, format= None):
        try:
            window_film_reel = WindowFilmReel.objects.get(id = pk)
            data = request.data
            serializer = WindowFilmReelSerializer(window_film_reel, data=data)
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