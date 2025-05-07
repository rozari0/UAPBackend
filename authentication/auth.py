# auth_backend.py
from ninja.security import HttpBearer

from .models import AuthToken


class SimpleTokenAuth(HttpBearer):
    def authenticate(self, request, token: str):
        try:
            auth_token = AuthToken.objects.get(key=token)
            request.user = auth_token.user
            return auth_token.user
        except AuthToken.DoesNotExist:
            return None
