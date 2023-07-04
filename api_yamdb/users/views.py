from django.core.mail import send_mail
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import filters, viewsets, status
from rest_framework_simplejwt.tokens import RefreshToken

import uuid

from .permissions import IsAdminOrAction, IsUser
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)
    permission_classes = [IsAdminOrAction,]

    @action(detail=False, methods=['GET','PATCH'])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data,
                            status=status.HTTP_200_OK
            )
        user = request.user
        serializer = UserSerializer(user,
                                    data=request.data,
                                    partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        confirmation_code = str(uuid.uuid4())
        email_subject = 'Your confirmation code'
        message = f'Ваш код: {confirmation_code}'
        to_email = request.data['email']
        try:
            send_mail(
                subject=email_subject,
                message=message,
                from_email='from@example.com',
                recipient_list=(to_email,),
            )
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.save(confirmation_code=confirmation_code)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def send_token(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    try:
        user = User.objects.get(username=username)
    except Exception:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if user.confirmation_code == confirmation_code:
        refresh = RefreshToken.for_user(user)
        token = {
        'token': str(refresh.access_token)
        }
        return Response(token)
    return Response(status=status.HTTP_400_BAD_REQUEST)
    
