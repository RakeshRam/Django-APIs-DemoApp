from django.core.management.base import BaseCommand

import grpc
from core.proto_files import books_pb2, books_pb2_grpc

# python manage.py setup_dummydata
class Command(BaseCommand):
    help = 'Test gRPC Client'

    def handle(self, *args, **kwargs):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = books_pb2_grpc.BookControllerStub(channel)
            for book in stub.List(books_pb2.BookListRequest()):
                print(book, end='')
                print("------")