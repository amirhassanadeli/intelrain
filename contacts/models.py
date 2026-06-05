# contact/models.py
from django.db import models

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name="Full Name")
    email = models.EmailField(unique=True ,max_length=200, verbose_name="Email Address")
    phone = models.CharField(unique=True ,max_length=20, blank=True, null=True, verbose_name="Phone Number")
    message = models.TextField(verbose_name="Your Message")
    is_read = models.BooleanField(default=False, help_text="Admin has read this message")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'contact_messages'
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.name} - {self.email} - {self.created_at.strftime('%Y-%m-%d')}"