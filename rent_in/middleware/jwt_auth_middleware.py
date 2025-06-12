from utils.jwt_auth import get_user_from_jwt
from django.contrib.auth.models import AnonymousUser

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only override if session-based user is not authenticated
        if not getattr(request, "user", None) or request.user.is_anonymous:
            request.user = get_user_from_jwt(request) or AnonymousUser()
        return self.get_response(request)

