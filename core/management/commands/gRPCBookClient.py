from django.core.management.base import BaseCommand

import grpc
from core.proto_files import books_pb2, books_pb2_grpc

# python manage.py setup_dummydata
class Command(BaseCommand):
    help = 'Test gRPC Client CRUD Operations'

    def handle(self, *args, **kwargs):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = books_pb2_grpc.BookControllerStub(channel)
            print('----- Create -----')
            response = stub.Create(books_pb2.Book(name='TestgRPC', is_available=True, publisher=21))
            print(response, end='')
            
            print('----- List -----')
            for book in stub.List(books_pb2.BookListRequest()):
                print(book, end='')
                print("-------------")

            print('----- Retrieve -----')
            response = stub.Retrieve(books_pb2.BookRetrieveRequest(id=response.id))
            print(response, end='')

            print('----- Update -----')
            response = stub.Update(books_pb2.Book(id=response.id, name='TestgRPC_EDIT', is_available=False, publisher=21))
            print(response, end='')

            print('----- Delete -----')
            stub.Destroy(books_pb2.Book(id=response.id))