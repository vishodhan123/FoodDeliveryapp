from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow access to authenticated users
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        # Check object-level permission here
        if request.user.is_authenticated:
            if request.user.user_type == 'restaurant_owner':
                # Check if the user is the owner of the restaurant
                return obj.user == request.user
        return False