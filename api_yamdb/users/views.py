from django.core.mail import send_mail
from django.core.mail import EmailMessage
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import filters, viewsets, status

import uuid

import api_yamdb.settings as settings
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)

    @action(detail=False, methods=['GET','PATHC'])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data,
                            status=status.HTTP_200_OK
            )


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