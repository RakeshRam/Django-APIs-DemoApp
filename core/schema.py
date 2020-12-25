import graphene
from graphene_django import DjangoObjectType, DjangoListField

from .models import Author, Award, Publisher, Book, AwardRecord

class PublisherType(DjangoObjectType):
    class Meta:
        model = Publisher
        fields = ('name', 'award')

class AwardType(DjangoObjectType):
    class Meta:
        model = Award
        fields = ('name', 'country', 'category')

class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ('name', 'award', 'age')

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ('name', 'author', 'award')


class Query(graphene.ObjectType):
    # Example Field
    # qz = graphene.String()
    # def resolve_qz(root, info):
    #     """Param: query{
    #                 qz
    #                 }"""
    #     return "My String"

    # Multi-Query Example
    """
        query{
            authors{
                name
                age
                author{
                    name
                    }
            }
            books{
                name
            }
        }
    """

    books = graphene.List(BookType, id=graphene.Int())
    def resolve_books(root, info, id=None):
        """
        Param: {
                books{
                        name
                    }
                }

        OR With Parameter
                query{
                    books(id:2){
                            name
                        }
                    }

        OR Named Function
                query getBooks($id: Int=1){
                    books(id:$id){
                        name
                    }
                }
        """
        if id:
            return Book.objects.filter(pk=id)

        return Book.objects.all().order_by('name')

    authors = DjangoListField(AuthorType)
    def resolve_authors(root, info):
        """
        Param: query{
                authors{
                    name
                    age
                }
                }
        """
        return Author.objects.all().order_by('name')

    

schema = graphene.Schema(query=Query)
