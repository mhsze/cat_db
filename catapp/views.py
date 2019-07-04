from django.shortcuts import render
from rest_framework import viewsets
from .serializers import HomeSerializer, HumanSerializer, BreedSerializer, CatSerializer
from .models import Home, Human, Breed, Cat
from rest_framework.decorators import api_view, action
# Create your views here.

class HomeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = HomeSerializer
    queryset = Home.objects.all()

class HumanViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = HumanSerializer
    queryset = Human.objects.all()

class BreedViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = BreedSerializer
    queryset = Breed.objects.all()

class CatViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = CatSerializer
    queryset = Cat.objects.all()

