# portfolio/models.py
from django.db import models
from django.utils.text import slugify
from hashids import Hashids
from django.conf import settings

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('ai', 'AI Automation'),
        ('data', 'Data Intelligence'),
        ('vision', 'Computer Vision'),
    ]
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True, blank=True, max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)
    icon = models.CharField(max_length=10, help_text="Emoji for the project")
    description = models.TextField()
    results = models.TextField(help_text="Results achieved with this project")
    tech = models.JSONField(default=list, help_text="List of technologies used")
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    client_name = models.CharField(max_length=200, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            counter = 1
            while Project.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
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
    
    class Meta:
        db_table = 'portfolio_projects'
        ordering = ['-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'