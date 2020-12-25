from django.urls import path, include

from rest_framework import routers


from . import views

router = routers.DefaultRouter()
router.register(r'authors', views.AuthorViewSet)
router.register(r'publishers', views.PublisherViewSet)
router.register(r'awards', views.AwardViewSet)
router.register(r'books', views.BookViewSet)

# Wire up API's using automatic URL routing
# Include login urls for browsable API
urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]