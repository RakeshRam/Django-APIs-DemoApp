from rest_framework import serializers

from .models import Author, Award, Publisher, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'award')
        depth = 1

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('name', 'award')
        depth = 1

class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ('name', 'country', 'category')

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'author', 'award', )
        # fields = '__all__'
        depth = 1