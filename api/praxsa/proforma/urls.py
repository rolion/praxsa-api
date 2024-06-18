
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from proforma.custom_views.brand import CarBrand_APIView, CarBrand_Search_Paginated, CarBrand_detail

from proforma.custom_views.car_model import CarModel_APIView, CarModel_Search_Paginated, CarModel_detail
from proforma.custom_views.car_part import CarPart_APIView, CarPart_Search_Paginated, CarPart_detail
from proforma.custom_views.car_model_part import CarModelPart_APIView, CarModelPart_detail, CarModelPart_Search_Paginated
# CarBrandDetail, CarBrandListCreate, CarModelDetail, CarModelListCreate, CarModelPartDetail, CarModelPartListCreate, CarPartDetail, CarPartListCreate
app_name = 'proforma'
urlpatterns = [
    path('carbrands/', CarBrand_APIView.as_view(), name='carbrand-get-post'),
    path('carbrands/search/', CarBrand_Search_Paginated.as_view(), name='carbrand-search'),
    path('carbrands/<int:pk>/', CarBrand_detail.as_view(), name='carbrand-detail'),

    path('carmodel/', CarModel_APIView.as_view(), name='carmodel-get-post'),
    path('carmodel/search/', CarModel_Search_Paginated.as_view(), name='carmodel-search'),
    path('carmodel/<int:pk>/', CarModel_detail.as_view(), name='carmodel-by-id'),
    
    path('carpart/', CarPart_APIView.as_view(), name='carpart-get-post'),
    path('carpart/search/', CarPart_Search_Paginated.as_view(), name='carpart-search'),
    path('carpart/<int:pk>/', CarPart_detail.as_view(), name='carpart-detail'),


    path('carmodelpart/', CarModelPart_APIView.as_view(), name='carpart-get-post'),
    path('carmodelpart/search/', CarModelPart_Search_Paginated.as_view(), name='carpart-search'),
    path('carmodelpart/<int:pk>/', CarModelPart_detail.as_view(), name='carpart-detail'),
]
urlpatterns = format_suffix_patterns(urlpatterns)