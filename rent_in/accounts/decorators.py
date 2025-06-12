# accounts/decorators.py

from django.http import JsonResponse
from functools import wraps
from middleware.jwt_auth_middleware import get_user_from_jwt  # adjust import if needed
from django.contrib.auth.models import AnonymousUser
def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = get_user_from_jwt(request)
        if not user or not user.is_authenticated:
            return JsonResponse({'detail': 'Authentication required'}, status=401)
        request._cached_user = get_user_from_jwt(request) or AnonymousUser()
        return view_func(request, *args, **kwargs)
    return _wrapped_view
