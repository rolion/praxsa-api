from rest_framework import serializers
from .models import CarBrand, CarModel, CarPart, CarModelPart, WindowFilm, WindowFilmReel, BranchOffice, Profile, Company

class CarBrandSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.is_enable = validated_data.get('is_enable', instance.is_enable)
        instance.save()
        return instance
    class Meta:
        model = CarBrand
        fields = '__all__'

class CarModelSerializer(serializers.ModelSerializer):
    car_brand_name = serializers.CharField(source="car_brand.name", read_only=True)
    class Meta:
        model = CarModel
        fields = '__all__'

class CarPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarPart
        fields = '__all__'

class CarModelPartSerializer(serializers.ModelSerializer):
    car_model_name = serializers.CharField(source="car_model.name", read_only=True)
    car_part_name = serializers.CharField(source="car_part.name", read_only=True)
    class Meta:
        model = CarModelPart
        fields = '__all__'

class WindowFilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindowFilm
        fields = '__all__'


class WindowFilmReelSerializer(serializers.ModelSerializer):
    windowfilm_name = serializers.CharField(source="windowfilm.name", read_only=True)
    class Meta:
        model = WindowFilmReel
        fields = '__all__'

class BranchOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchOffice
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'