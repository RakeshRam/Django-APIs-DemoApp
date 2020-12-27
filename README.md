# Django API Demo APP
Example Django App with REST, GraphQL and gRPC

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirments.txt.

```bash
pip install -r requirements.txt
```

## Usage
Set-up dummy data.

```
python manage.py setup_dummydata
```

Run server in local environment.

```bash
python manage.py runserver
```

## Features
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



## License
[MIT](https://choosealicense.com/licenses/mit/)