# services/models.py
from django.db import models
from django.utils.text import slugify
from hashids import Hashids
from django.conf import settings

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('ai', 'Artificial Intelligence'),
        ('automation', 'Automation'),
        ('vision', 'Computer Vision'),
        ('data', 'Data Intelligence'),
        ('chatbot', 'Chatbot'),
        ('other', 'Other'),
    ]
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=10)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField()
    features = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    @property
    def hash(self):
        """ساخت هش از روی ID"""
        hashids = Hashids(salt=settings.SECRET_KEY, min_length=8)
        return hashids.encode(self.id)
    
    @classmethod
    def get_by_hash(cls, hash_str):
        """پیدا کردن با هش"""
        hashids = Hashids(salt=settings.SECRET_KEY, min_length=8)
        ids = hashids.decode(hash_str)
        if ids:
            return cls.objects.filter(id=ids[0], is_active=True).first()
        return None
    
    def __str__(self):
        return self.title