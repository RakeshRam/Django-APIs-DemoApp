from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django_grpc_framework import generics
from .serializers import BookProtoSerializer

from .serializers import AuthorSerializer, PublisherSerializer, AwardSerializer, BookSerializer, AwardRecordSerializer
from .models import Author, Award, Publisher, Book, AwardRecord

def bookHomePage(request):
    context = {
        'books': Book.objects.filter(is_available=True).order_by('id')[:10] 
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

# Example CRUD Operations(GET, POST, PUT, DELETE)
class BookViewSet(viewsets.ModelViewSet):
    """
    Example Create -> POST:
    -----------------------
                {
                    "publisher": <Publisher_ID>,
                    "name": "<BOOK NAME>",
                    "is_available": true
                }

    Example Update -> PUT:
    ----------------------
                {
                    "id": <BOOK_ID>,
                    "publisher": <Publisher_ID>,
                    "name": "<BOOK NEW_NAME>",
                    "is_available": true,
                    
                }

    Example Delete -> DELETE:
    -------------------------
                /core/api/books/<BOOK_ID>/
    """
    queryset = Book.objects.all().order_by('name')
    serializer_class = BookSerializer
    http_method_names = ['get', 'put', 'post', 'delete']

    # CREATE NEW Book VIA API - POST
    def create(self, request, *args, **kwargs):
        book = request.data
        if "publisher" in book:
            book['publisher'] = Publisher.objects.get(pk=book['publisher'])
        new_book = Book.objects.create(**book)
        new_book.save()        

        serializer = BookSerializer(new_book)

        return Response(serializer.data)


# ========================================================================================== #
# gRPC Service
class BookService(generics.ModelService):
    """
    gRPC service to query books.
    """
    queryset = Book.objects.all().order_by('-name')
    serializer_class = BookProtoSerializer

