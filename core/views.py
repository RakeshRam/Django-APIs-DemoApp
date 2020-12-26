from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import AuthorSerializer, PublisherSerializer, AwardSerializer, BookSerializer, AwardRecordSerializer
from .models import Author, Award, Publisher, Book, AwardRecord

def bookHomePage(request):
    context = {
        'books': Book.objects.all()
    }
    return render(request, 'books.html', context)

class AwardRecordViewSet(viewsets.ModelViewSet):
    queryset = AwardRecord.objects.all().order_by('name')
    serializer_class = AwardRecordSerializer
    http_method_names = ['get']

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer
    http_method_names = ['get', 'post']

    # CREATE NEW AUTHOR VIA API - POST
    def create(self, request, *args, **kwargs):
        author = request.data
        new_author = Author.objects.create(name=author["name"], 
                                            age=author["age"])
        new_author.save()
        # TO FIX - Multiple elements not saved.
        new_author.award.add(*AwardRecord.objects.filter(id__in=author['award']))
        
        serializer = AuthorSerializer(new_author)

        return Response(serializer.data)

class PublisherViewSet(viewsets.ModelViewSet):
    # Authentication
    permission_classes = (IsAuthenticated,) 
    
    content = {'message': 'Hello, World!'}
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

