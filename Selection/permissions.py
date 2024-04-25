from rest_framework.permissions import BasePermission

class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True