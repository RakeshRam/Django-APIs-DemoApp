# Django Demo API APP

Example Django App with REST, GraphQL and gRPC.

## <u>Installation</u>

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirments.txt.

```bash
pip install -r requirements.txt
```

## <u>Usage</u>

Set-up dummy data.

```bash
python manage.py setup_dummydata
```

Run server in local environment.

```bash
python manage.py runserver
```

## <u>Features</u>

* Demo Books Gallery
* Basic DRF implementation(CRUD)
  * [Django REST framework](https://www.django-rest-framework.org/)
    * Authentication
      * Token Authentication
      * [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
* Basic Graphql Implementation(CRUD)
  * [Graphene-Django](https://docs.graphene-python.org/projects/django/en/latest/)
    * Authentication
      * [JWT Authentication](https://django-graphql-jwt.domake.io/en/latest/)
      * [Django-Graphql-Auth](https://django-graphql-auth.readthedocs.io/en/latest/)

## <u>API Usage Demo</u>

### **DjangoRestFramework**

* Get JWT

  ```bash
  /api-jwt/token/
  {
      "username": "<USER_NAME>",
      "password": "<PWD>"
  }
  ```

* Create New Book -> POST

  ```json
  /core/api/books/
  {
      "publisher": <Publisher_ID>,
      "name": "<BOOK_NAME>",
      "is_available": true
  }
    ```

* Update Book -> PUT

  ```json
  /core/api/books/<BOOK_ID>/
  {
      "id": <BOOK_ID>,
      "publisher": <Publisher_ID>,
      "name": "<BOOK NEW_NAME>",
      "is_available": true,
      
  }
  ```

* Delete Book -> DELETE

  ```bash
  /core/api/books/<BOOK_ID>/
  ```

### **GraphQL**

* Get JSON Web Token for Verified User

  ```json
  mutation {
        tokenAuth(username: "<USER_NAME>", password: "<PWD>") {
          success
          errors
          token
          refreshToken
          user {
            username
          }
        }
    }
  ```

* Query

  ```json
  {
    books {
      name
    }
  }
  ```

  With Argument(Book ID).

  ```json
  query{
      books(id:<BOOK_ID>){
          name
      }
  }
  ```

* Mutation

  Create

  ```python
  mutation {
    createUpdateBook(name:"<BOOK_NAME>", publisher: <Publisher_ID>, isAvailable:true, ....) {
      book {
        name
        isAvailable
        publisher {
          name
        }
      }
    }
  }
  ```

  Update

  ```json
  mutation {
            createUpdateBook(pk:<BOOK_ID>, publisher:<Publisher_ID>, ....){
                ....
            }
        }
  ```

  Delete

  ```json
  mutation {
            createUpdateBook(pk:<BOOK_ID>){
                ....
            }
        }
  ```

## License

[MIT](https://choosealicense.com/licenses/mit/)