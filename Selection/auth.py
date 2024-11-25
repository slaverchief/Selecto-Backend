
from rest_framework import exceptions
from rest_framework import authentication
from .models import User



class SelectoAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Get the username and password
        auth = request.headers.get('Authorization')

        if not auth:
            raise exceptions.AuthenticationFailed('No credentials provided.')

        try:
            user = User.objects.get(auth_id=auth)
            return user, None
        except:
            raise exceptions.AuthenticationFailed('Invalid authtorization data.')

