"""
URL configuration for praxsa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("product/", include("proforma.urls")),
    # path('carbrands/<int:pk>/', CarBrandDetail.as_view(), name='carbrand-detail'),
    # path('carmodels/', CarModelListCreate.as_view(), name='carmodel-list'),
    # path('carmodels/<int:pk>/', CarModelDetail.as_view(), name='carmodel-detail'),
    # path('carparts/', CarPartListCreate.as_view(), name='carpart-list'),
    # path('carparts/<int:pk>/', CarPartDetail.as_view(), name='carpart-detail'),
    # path('carmodelparts/', CarModelPartListCreate.as_view(), name='carmodelpart-list'),
    # path('carmodelparts/<int:pk>/', CarModelPartDetail.as_view(), name='carmodelpart-detail'),
]