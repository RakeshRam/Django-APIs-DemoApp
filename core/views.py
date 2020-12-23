from django.shortcuts import render

from rest_framework import viewsets

from .serializers import AuthorSerializer, PublisherSerializer, AwardSerializer, BookSerializer
from .models import Author, Award, Publisher, Book

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer
    http_method_names = ['get']

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all().order_by('name')
    serializer_class = PublisherSerializer
    http_method_names = ['get']

class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.all().order_by('name')
    serializer_class = AwardSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('name')
    serializer_class = BookSerializer
    http_method_names = ['get']

