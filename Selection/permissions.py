from rest_framework.permissions import BasePermission
from Selecto.settings import ACCESS_TOKEN



class IsCorrectToken(BasePermission):
    def has_permission(self, request, view):
        return bool(request.headers.get('AccessToken', None) == ACCESS_TOKEN)
