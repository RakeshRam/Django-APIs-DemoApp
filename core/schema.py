import graphene
from graphene_django import DjangoObjectType, DjangoListField
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery

from .models import Author, Award, Publisher, Book, AwardRecord

# Registration
class AuthMutation(graphene.ObjectType):
    """
    Used to register, update and verify user and auth token
    Example Register: 
    -----------------
            mutation {
                register(
                    email: "r@r.com", 
                    username: "newUser", 
                    password1: "aqwsdf2123", 
                    password2: "aqwsdf2123"
                    ) {
                        success
                        errors
                        token
                        refreshToken
                    }
            }

    Example Verification:
    ---------------------
            mutation {
                verifyAccount(token: "eyJ1c2Vybm....."){
                    success
                    errors
                }
            }

    Example Get JWT(For Registered User):
    -------------------------------------
            mutation {
                tokenAuth(username: "<USER_NAME>", password: "<PWD>"){
                    success
                    errors
                    token
                    refreshToken
                    user{
                        username
                    }
                }
            } 

    Example Update:
    ---------------
            mutation {
                updateAccount(firstName: "Hello"){
                    success
                    errors
                }
            }

    """
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()

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
    pk = graphene.ID(source='pk')
    class Meta:
        model = Book
        fields = ('name', 'author', 'is_available', 'publisher')


# Only for Querying data from DB(Read-Only)!!
class Query(UserQuery, MeQuery, graphene.ObjectType):
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
    # UserQuery Example
    """
    query {
        users{
            edges{
                node{
                    username
                    email
                }
            }
        }
    }
    """
    # MeQuery Example: Returns Logged in User
    """
    query {
        me{
            username
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

# ========================================================================================================= #

# !!! CRUD Operations Example !!!
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
        -------
            mutation createUpdateDeleteAwardRecord{
                    createUpdateAward(name:"<Name>", country:"<Country>"){
                        award{
                            name
                            country
                        }    
                    }
                }

        UPDATE:
        -------
            mutation createUpdateDeleteAwardRecord{
                    createUpdateAward(pk:<primary_key>, name:"<Name>", country:"<Country>"){
                        ....
                }

        DELETE:
        -------
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

# Book Table Basic CRUD operations
class BookMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.ID()
        name = graphene.String(required=False)
        is_available = graphene.Boolean()
        publisher = graphene.Int()

    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, root, info, pk=None, **kwargs):
        """
        Example Usage:
            mutation {
                createUpdateBook(pk:1, publisher:21){
                    book{
                        name
                        isAvailable
                        publisher{
                                name
                            }
                    }
                }
            }
        """
        if pk:
            book = Book.objects.get(pk=pk)
            if kwargs:
                # Update Existing Record.
                for (key, value) in kwargs.items():
                    if key == 'publisher':
                        value = Publisher.objects.get(pk=value)
                    setattr(book, key, value)
                book.save()
            else:
                # Delete Existing Record.
                book.delete()
        else:
            # Create New Record.
            book = Book.objects.create(**kwargs)

        return BookMutation(book=book)

# For Modifying Data in DB(Create-Read-Write-Delete)!!
class Mutation(AuthMutation, graphene.ObjectType):
    create_update_award = AwardMutation.Field()
    create_update_book = BookMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
