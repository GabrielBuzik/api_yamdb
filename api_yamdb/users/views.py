import uuid

from django.core.mail import send_mail
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import filters, viewsets, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdminOrAction
from .models import User
from .serializers import UserSerializer
from api_yamdb.settings import EMAIL_HOST_USER


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)
    permission_classes = [IsAdminOrAction, ]
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']

    @action(detail=False,
            methods=['GET', 'PATCH'],
            permission_classes=(IsAuthenticated,)
            )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        user = request.user
        role = user.role
        serializer = UserSerializer(user,
                                    data=request.data,
                                    partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=role)
        return Response(serializer.data)


@api_view(['POST'])
def signup(request):
    confirmation_code = str(uuid.uuid4())
    try:
        user = User.objects.get(
            username=request.data['username'],
            email=request.data['email']
        )
        user.confirmation_code = confirmation_code
    except Exception:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(confirmation_code=confirmation_code)

    email_subject = 'Your confirmation code'
    message = f'Ваш код: {confirmation_code}'
    to_email = request.data['email']
    try:
        send_mail(
            subject=email_subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=(to_email,),
        )
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response({
        'username': request.data['username'],
        'email': request.data['email']
    })


@api_view(['POST'])
def send_token(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    if (confirmation_code is None or username is None):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(User,
                             username=username)

    if user.confirmation_code == confirmation_code:
        refresh = RefreshToken.for_user(user)
        token = {'token': str(refresh.access_token)}
        return Response(token)
    return Response(status=status.HTTP_400_BAD_REQUEST)
