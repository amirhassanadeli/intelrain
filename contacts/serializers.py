# contact/serializers.py
from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['id', 'is_read', 'created_at', 'updated_at']


class ContactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']  # ← phone اضافه شد
    
    def validate_email(self, value):
        """اعتبارسنجی ایمیل"""
        if '@' not in value:
            raise serializers.ValidationError("Email must contain @")
        return value
    
    def validate_name(self, value):
        """اعتبارسنجی نام"""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters")
        return value
    
    def validate_phone(self, value):
        """اعتبارسنجی شماره تماس (اختیاری)"""
        if value and len(value) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits")
        return value
    
    def validate_message(self, value):
        """اعتبارسنجی پیام"""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters")
        return value


class ContactListSerializer(serializers.ModelSerializer):
    """برای نمایش لیست پیام‌ها در ادمین"""
    message_preview = serializers.SerializerMethodField()
    
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'message_preview', 'is_read', 'created_at']
    
    def get_message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message