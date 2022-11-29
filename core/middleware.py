from django.contrib.auth.middleware import AuthenticationMiddleware
from django.utils.functional import SimpleLazyObject

from user.services import AuthenticationService


class JWTAuthenticationMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: AuthenticationService.get_jwt_user(request))
