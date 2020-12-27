from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from rest_framework import routers
from graphene_django.views import GraphQLView


from . import views
from .schema import schema

router = routers.DefaultRouter()
router.register(r'authors', views.AuthorViewSet)
router.register(r'publishers', views.PublisherViewSet)
router.register(r'awards', views.AwardViewSet)
router.register(r'books', views.BookViewSet)

# Wire up API's using automatic URL routing
# Include login urls for browsable API
urlpatterns = [
    # REST
    path('api/', include(router.urls)), # Base End point -> http://127.0.0.1:8000/core/api
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # GraphQL
    # Single END point -> http://127.0.0.1:8000/core/graphql
    path(r"graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]