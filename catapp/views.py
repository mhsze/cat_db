from django.shortcuts import render
from rest_framework import viewsets
from .serializers import HomeSerializer, HumanSerializer, BreedSerializer, CatSerializer
from .models import Home, Human, Breed, Cat
from rest_framework.decorators import api_view, action
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .authentications import ExpiringTokenAuthentication
from catproject.settings import TOKEN_EXPIRY_TIME
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
# Create your views here.

class HomeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    authentication_classes = (ExpiringTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = HomeSerializer
    queryset = Home.objects.all()

class HumanViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    authentication_classes = (ExpiringTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = HumanSerializer
    queryset = Human.objects.all()

class BreedViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    authentication_classes = (ExpiringTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = BreedSerializer
    queryset = Breed.objects.all()

class CatViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    authentication_classes = (ExpiringTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CatSerializer
    queryset = Cat.objects.all()

class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created =  Token.objects.get_or_create(user=serializer.validated_data['user'])
            time_elapsed = timezone.now() - token.created
            if not created and time_elapsed > timedelta(seconds = settings.TOKEN_EXPIRY_TIME):
                # update the created time of the expired token to keep it valid
                # token.created = timezone.now()
                # token.save()

                # delete existing token and create a new one
                token.delete()
                token = Token.objects.create(user = token.user)
                time_elapsed = timezone.now() - token.created
                expires_in_seconds = timedelta(seconds = settings.TOKEN_EXPIRY_TIME) - time_elapsed
                return Response({'token': token.key, 'expires_in': int(expires_in_seconds.total_seconds())})
            expires_in_seconds = timedelta(seconds = settings.TOKEN_EXPIRY_TIME) - time_elapsed
            return Response({'token': token.key, 'expires_in': int(expires_in_seconds.total_seconds())})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()
