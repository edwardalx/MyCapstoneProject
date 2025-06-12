from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.backends import TokenBackend
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

def get_user_from_jwt(request):
    auth = request.headers.get('Authorization', None)
    if not auth or not auth.startswith('Bearer '):
        return None

    token = auth.split(' ')[1]
    try:
        # Validate and decode token
        validated_token = UntypedToken(token)
        token_backend = TokenBackend(algorithm='HS256', signing_key=settings.SECRET_KEY)
        decoded_data = token_backend.decode(token, verify=True)

        user_id = decoded_data.get('user_id')
        return User.objects.get(id=user_id)
    except (TokenError, InvalidToken, User.DoesNotExist):
        return None