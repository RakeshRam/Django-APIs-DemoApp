import graphene
from graphene_django import DjangoObjectType, DjangoListField

from .models import Author, Award, Publisher, Book, AwardRecord

class PublisherType(DjangoObjectType):
    class Meta:
        model = Publisher
        fields = ('name', 'award')

class AwardType(DjangoObjectType):
    # Required for PK or ID look-up
    pk = graphene.ID(source='pk')
    class Meta:
        model = Award
        fields = ('pk', 'name', 'country', 'category')

class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ('name', 'award', 'age')

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ('name', 'author', 'award')


# Only for Querying data from DB(Read-Only)!!
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

# !!! CRUD Operations !!!
class AwardMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.ID()
        name = graphene.String(required=False)
        country = graphene.String(required=False)

    award = graphene.Field(AwardType)

    @classmethod
    def mutate(cls, root, info, pk=None, **kwargs):
        """
        Ex Mutation:
        ------------
        CREATE:
            mutation createUpdateDeleteAwardRecord{
                    createUpdateAward(name:"<Name>", country:"<Country>"){
                        award{
                            name
                            country
                        }    
                    }
                }

        UPDATE:
            mutation createUpdateDeleteAwardRecord{
                    createUpdateAward(pk:<primary_key>, name:"<Name>", country:"<Country>"){
                        ....
                }

        DELETE:
            mutation createUpdateDeleteAwardRecord{
                    createUpdateAward(pk:<primary_key>){
                        ....
                }
        """

        # Note: Using PK as an example.
        if pk:
            award = Award.objects.get(pk=pk)
            if kwargs:
                # Update Existing Record.
                for (key, value) in kwargs.items():
                        setattr(award, key, value)
                award.save()
            else:
                # Delete Existing Record.
                award.delete()
        else:
            # Create New Record.
            award = Award.objects.create(**kwargs)

        return AwardMutation(award=award)

# For Modifying Data in DB(Create-Read-Write-Delete)!!
class Mutation(graphene.ObjectType):
    create_update_award = AwardMutation.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)
