from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

# REST
from rest_framework.authtoken.views import obtain_auth_token
# JWT
from rest_framework_simplejwt import views as jwt_views
# gRPC
from core.proto_files import books_pb2_grpc

from core.views import bookHomePage, BookService

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('books/', bookHomePage, name='books_homepage'),
    path('admin/', admin.site.urls),
    
    
    # CORE
    path('core/', include('core.urls')),

    # $$$$$$$$$$$$$$$ AUTHENTICATION $$$$$$$$$$$$$$$
    # ************* Token Auth END Point (REST) *************
    # Ex: http://127.0.0.1:8000/api-token-auth/
    # Ex Data: {
    #            "username": "admin",
    #            "password": "admin"
    #        }
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # ************* JWT Auth END Point (REST) *************
    # EX: http://127.0.0.1:8000/api-jwt/token/
    # Ex Data: {
    #            "username": "admin",
    #            "password": "admin"
    #        }
    # Ex RESPONSE: {
    #            "refresh": "eyJ0eXAiOiJKV1Q.....",
    #            "access": "eyJ0eXAiOiJKV1Qi....."
    #          }
    path('api-jwt/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Ex: http://127.0.0.1:8000/api-jwt/token/refresh/
    # Ex Data: {
    #           "Authorization": "Bearer <RECEIVED REFRESH TOKEN FROM ABOVE ENDPOINT>"
    # } 
    # Ex RESPONSE: {
    #            "access": "kyasdasf034dfsdfs....."
    #          }
    path('api-jwt/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

# gRPC Routing
def grpc_handlers(server):
    books_pb2_grpc.add_BookControllerServicer_to_server(BookService.as_servicer(), server)
