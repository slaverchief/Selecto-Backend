from rest_framework.permissions import BasePermission
from Selecto.settings import ACCESS_TOKEN
class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsCorrectToken(BasePermission):
    def has_permission(self, request, view):
        return bool(request.headers.get('AccessToken', None) == ACCESS_TOKEN)
