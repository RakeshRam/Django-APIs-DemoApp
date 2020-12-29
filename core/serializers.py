from rest_framework import serializers

from django_grpc_framework import proto_serializers
from .proto_files import books_pb2

from .models import Author, Award, Publisher, Book, AwardRecord

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('name', 'award')
        depth = 1

class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ('name', 'country', 'category')

class AwardRecordSerializer(serializers.ModelSerializer):
    name = AwardSerializer(read_only=True, many=False)
    class Meta:
        model = AwardRecord
        fields = ('name', 'awarded_on', 'is_active')

class AuthorSerializer(serializers.ModelSerializer):
    # SHOW AwardRecord SELECTION BOX
    award = serializers.PrimaryKeyRelatedField(queryset=AwardRecord.objects.filter(is_active=True), many=True)
    class Meta:
        model = Author
        fields = ('name', 'award', 'age')
        depth = 2

class BookSerializer(serializers.ModelSerializer):
    # Required to Add ID field
    id = serializers.IntegerField()
    # Hyper Link to Related ForeignKey(Ex: Author)
    author = serializers.HyperlinkedRelatedField(
                                                    many=True,
                                                    read_only=True,
                                                    view_name='author-detail'
                                                )
    publisher = serializers.PrimaryKeyRelatedField(queryset=Publisher.objects.filter(is_active=True), many=False)
    class Meta:
        model = Book
        #fields = ('id', 'name', 'author')
        fields = '__all__'
        depth = 2


# gRPC Serializer
class BookProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Book
        proto_class = books_pb2.Book
        fields = ('id', 'name', 'publisher', 'is_available')