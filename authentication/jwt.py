from rest_framework.authentication import  get_authorization_header, BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
import jwt
from authentication.models import  User


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request): 
        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode('utf-8')
        auth_token = auth_data.split(" ")
        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed("Invalid TOken")
        token  = auth_token[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            username = payload['username']
            user = User.objects.get(username=username)
            return (user, token)

        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed(ex, " Token expired. Login Again")
        except  jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed(ex, "TOken is Invalid")
        except User.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed(no_user, "User does not Exist.")

        return super().authenticate(request)


