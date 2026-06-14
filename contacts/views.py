# contact/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Contact
from .serializers import ContactCreateSerializer, ContactListSerializer, ContactSerializer
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})



class ContactCreateView(generics.CreateAPIView):
    serializer_class = ContactCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        contact = serializer.save()

        return Response(
            {
                "success": True,
                "message": "Your message has been sent successfully!",
                "id": contact.id,
            },
            status=status.HTTP_201_CREATED,
        )
            
class ContactListView(generics.ListAPIView):
    """لیست پیام‌ها (فقط برای ادمین)"""
    queryset = Contact.objects.all()
    serializer_class = ContactListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # فقط ادمین
    
    def get_queryset(self):
        """فیلتر بر اساس خوانده شده یا نشده"""
        queryset = super().get_queryset()
        is_read = self.request.query_params.get('is_read')
        
        if is_read is not None:
            if is_read.lower() == 'true':
                queryset = queryset.filter(is_read=True)
            elif is_read.lower() == 'false':
                queryset = queryset.filter(is_read=False)
        
        return queryset


class ContactDetailView(generics.RetrieveUpdateAPIView):
    """جزئیات پیام و علامت خوانده شده (فقط برای ادمین)"""
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'id'
    
    def perform_update(self, serializer):
        """هنگام آپدیت، علامت خوانده شده رو True کن"""
        serializer.save(is_read=True)


class ContactDeleteView(generics.DestroyAPIView):
    """حذف پیام (فقط برای ادمین)"""
    queryset = Contact.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'id'


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def mark_as_read(request, pk):
    """علامت زدن پیام به عنوان خوانده شده (API برای ادمین)"""
    try:
        contact = Contact.objects.get(pk=pk)
        contact.is_read = True
        contact.save()
        return Response({
            'success': True, 
            'message': 'Message marked as read'
        })
    except Contact.DoesNotExist:
        return Response({
            'error': 'Message not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def mark_as_unread(request, pk):
    """علامت زدن پیام به عنوان خوانده نشده (API برای ادمین)"""
    try:
        contact = Contact.objects.get(pk=pk)
        contact.is_read = False
        contact.save()
        return Response({
            'success': True, 
            'message': 'Message marked as unread'
        })
    except Contact.DoesNotExist:
        return Response({
            'error': 'Message not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_unread_count(request):
    """تعداد پیام‌های خوانده نشده (برای نمایش نوتیفیکیشن در ادمین)"""
    if request.user.is_authenticated and request.user.is_staff:
        count = Contact.objects.filter(is_read=False).count()
        return Response({'unread_count': count})
    return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)