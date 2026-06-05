# portfolio/serializers.py
from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    hash = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'
    
    def get_hash(self, obj):
        return obj.hash


class ProjectListSerializer(serializers.ModelSerializer):
    hash = serializers.SerializerMethodField(read_only=True)
    category_display = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'hash',
            'slug',
            'title',
            'category',
            'category_display',
            'icon',
            'description',
            'results',
            'tech',
            'is_active',
            'created_at'
        ]
    
    def get_hash(self, obj):
        return obj.hash
    
    def get_category_display(self, obj):
        return obj.get_category_display()


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'title',
            'category',
            'icon',
            'description',
            'results',
            'tech',
            'client_name',
            'completion_date',
            'is_active'
        ]
    
    def validate_tech(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Tech must be a list")
        return value
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.id
        representation['hash'] = instance.hash
        representation['slug'] = instance.slug
        return representation


class ProjectDetailSerializer(serializers.ModelSerializer):
    hash = serializers.SerializerMethodField(read_only=True)
    category_display = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'
    
    def get_hash(self, obj):
        return obj.hash
    
    def get_category_display(self, obj):
        return obj.get_category_display()