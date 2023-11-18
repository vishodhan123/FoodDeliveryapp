from django.urls import path

from .permissions.authentication import LoginAPIView
from .views import UserAPIView, UpdateUserAPIView, CreateRestaurantAndMenuItems

urlpatterns = [
    path('api/create_user/', UserAPIView.as_view()),
    path('api/update_user/', UpdateUserAPIView.as_view()),
    path('api/login/', LoginAPIView.as_view()),
    path('api/add_restaurant/', CreateRestaurantAndMenuItems.as_view()),
]
