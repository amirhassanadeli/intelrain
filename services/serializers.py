# services/serializers.py
from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    hash = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Service
        fields = ['id', 'hash', 'slug', 'title', 'icon', 'category', 'description', 'features', 'is_active']
    
    def get_hash(self, obj):
        return obj.hash


class ServiceCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.id
        representation['hash'] = instance.hash
        representation['slug'] = instance.slug
        return representation


class ServiceListSerializer(serializers.ModelSerializer):
    hash = serializers.SerializerMethodField(read_only=True)
    category_display = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Service
        fields = ['hash', 'slug', 'title', 'icon', 'category_display', 'description', 'features', 'is_active']
    
    def get_hash(self, obj):
        return obj.hash
    
    def get_category_display(self, obj):
        return obj.get_category_display()


class ServiceDetailSerializer(serializers.ModelSerializer):
    hash = serializers.SerializerMethodField(read_only=True)
    category_display = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Service
        fields = '__all__'
    
    def get_hash(self, obj):
        return obj.hash
    
    def get_category_display(self, obj):
        return obj.get_category_display()


class ServiceByCategorySerializer(serializers.Serializer):
    category = serializers.CharField()
    category_display = serializers.CharField()
    services = ServiceListSerializer(many=True)