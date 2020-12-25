from django.urls import path, include

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
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # GraphQL
    # Single END point
    path(r"graphql", GraphQLView.as_view(graphiql=True, schema=schema)),
]