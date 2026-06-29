from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from contact.models import Contact
from .permissions import IsOwner
from .serializers import ContactSerializer, RegisterSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username
    })


@api_view(['POST'])
def logout_view(request):
    request.user.auth_token.delete()
    return Response(
        {'message': 'Logged out successfully'},
        status=status.HTTP_200_OK
    )


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        return Contact.objects.filter(
            user=self.request.user
        ).order_by('name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_favourite(self, request, pk=None):
        contact = self.get_object()
        contact.is_favourite = not contact.is_favourite
        contact.save()
        return Response({
            'id': contact.id,
            'is_favourite': contact.is_favourite
        })

    @action(detail=False, methods=['get'])
    def stats(self, request):
        qs = self.get_queryset()
        return Response({
            'total_contacts': qs.count(),
            'total_favourites': qs.filter(is_favourite=True).count(),
            'added_this_month': qs.filter(
                created_at__month=timezone.now().month,
                created_at__year=timezone.now().year
            ).count()
        })
