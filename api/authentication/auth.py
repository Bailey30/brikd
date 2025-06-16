from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom authentication class that allows JWT authentication via HTTP-only cookies.

    Why this exists:
    ----------------
    By default, SimpleJWT expects JWTs to be sent in the Authorization header as:
        Authorization: Bearer <token>

    In this project, we store JWT tokens in secure HTTP-only cookies to:
    - Improve XSS protection (cookies can be HttpOnly, so JavaScript can't access them)
    - Let the browser handle token sending automatically (no manual header setup in frontend)

    This class extends SimpleJWT's JWTAuthentication to:
    - First try to authenticate from the Authorization header (default)
    - If that fails, fallback to reading the access token from the cookie defined in settings.SIMPLE_JWT["AUTH_COOKIE"]

    When to use:
    ------------
    Use this class when:
    - Your frontend stores tokens in cookies (e.g., for automatic auth in SPAs)
    - You want to avoid using localStorage or manually attaching headers in JS

    Make sure:
    ----------
    - You set the access token as an HttpOnly cookie (usually in the login view)
    - Your settings.py defines SIMPLE_JWT["AUTH_COOKIE"] = "access_token" (or whatever name you're using)
    - This class is registered in REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']
    """

    def authenticate(self, request):
        # Try reading token from the Authorization header first
        header_auth = super().authenticate(request)
        if header_auth:
            return header_auth

        # Fallback: try reading from cookie
        raw_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])

        print("AUTHENTICATING")
        print("request:", request)
        print("cookies:", request.COOKIES)
        if raw_token:
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token
