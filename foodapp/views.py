from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Restaurant, MenuItem
from django.db import transaction

from .models import CustomUser
from .permissions.permission import CustomPermission


# Create your views here.
class UserAPIView(APIView):

    def post(self, request, format=None):
        try:
            user_data = {
                'username': request.data.get('username'),
                'email': request.data.get('email'),
                'password': request.data.get('password'),
                'first_name': request.data.get('first_name'),
                'last_name': request.data.get('last_name'),
                'address': request.data.get('address'),
                'city': request.data.get('city'),
                'user_type': request.data.get('user_type'),
            }

            # Basic validation checks
            if not user_data['username'] or not user_data['email'] or not user_data['password']:
                return Response({'error': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)

            # Create new user
            user = CustomUser.objects.create_user(**user_data)

            return Response(
                {'message': f"User {user.username} created successfully", 'id': user.id, 'username': user.username,
                 'email': user.email},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserAPIView(APIView):
    def put(self, request, format=None):
        try:
            username = request.data.get('username')
            user = CustomUser.objects.get(username=username)

            # Update user fields
            user.email = request.data.get('email', user.email)
            user.first_name = request.data.get('first_name', user.first_name)
            user.last_name = request.data.get('last_name', user.last_name)
            user.address = request.data.get('address', user.address)
            user.city = request.data.get('city', user.city)

            # Save the updated user
            user.save()

            return Response(
                {'message': f"User {user.username} updated successfully", 'id': user.id, 'username': user.username,
                 'email': user.email},
                status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateRestaurantAndMenuItems(APIView):
    import pdb; pdb.set_trace()
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomPermission]

    def post(self, request, *args, **kwargs):
        try:
            import pdb;
            pdb.set_trace()
            data = request.data
            username = data.get('username')
            restaurant_data = data.get('restaurant', {})
            menu_item_data = data.get('menu_items', [])

            # Find the owner (user) by username
            user = CustomUser.objects.get(username=username)
            if user.user_type != "restaurant_owner":
                return Response({"msg": "user must be restaurant_owner"}, status=status.HTTP_400_BAD_REQUEST)

            # Create restaurant and associate it with the owner
            restaurant = Restaurant(
                user=user,
                name=restaurant_data.get('name', ''),
                address=restaurant_data.get('address', ''),
                city=restaurant_data.get('city', ''),
                phone_number=restaurant_data.get('phone_number', ''),
                email=restaurant_data.get('email', ''),
                rating=restaurant_data.get('rating', 0.0),
                cuisine_type=restaurant_data.get('cuisine_type', ''),
                opening_time=restaurant_data.get('opening_time', ''),
                closing_time=restaurant_data.get('closing_time', ''),
                is_active=restaurant_data.get('is_active', True)
            )
            restaurant.save()

            # Create menu items for the restaurant
            menu_item_ids = []
            for menu_item_info in menu_item_data:
                menu_item = MenuItem(
                    restaurant=restaurant,
                    name=menu_item_info.get('name', ''),
                    description=menu_item_info.get('description', ''),
                    price=menu_item_info.get('price', 0.0),
                    category=menu_item_info.get('category', ''),
                    dietary_restrictions=menu_item_info.get('dietary_restrictions', ''),
                    is_vegan=menu_item_info.get('is_vegan', False),
                    is_available=menu_item_info.get('is_available', True)
                )
                menu_item.save()
                menu_item_ids.append(menu_item.id)

            return Response(
                {
                    'message': f'Restaurant "{restaurant.name}" and Menu items created with IDs: {menu_item_ids}',
                    'restaurant_id': restaurant.id,
                    'menu_item_ids': menu_item_ids,
                },
                status=status.HTTP_201_CREATED,
            )

        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
