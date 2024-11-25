from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission
from .models import User

# class IsAllowedUser(BasePermission):
#     def has_permission(self, request, view):
#         auth = request.headers.get('Authorization')
#         try:
#             User.objects.get(auth_id = auth)
#         except ObjectDoesNotExist:
#             return False
#         return True