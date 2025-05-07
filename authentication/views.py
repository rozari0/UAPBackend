# api/auth.py
from ninja_extra import api_controller, http_get, http_post
from ninja import Schema, ModelSchema
from django.contrib.auth import authenticate

from authentication.auth import SimpleTokenAuth
from .models import AuthToken, User


class LoginSchema(Schema):
    username: str
    password: str


class TokenResponse(Schema):
    token: str


class SignupSchema(Schema):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str


class SelfUserResponse(ModelSchema):
    class Meta:
        model = User
        exclude = "password", "is_superuser", "is_staff", "groups", "user_permissions"


class ErrorResponse(Schema):
    detail: str


@api_controller("/auth", tags=["Authentication"])
class AuthController:
    @http_post("/login", response={200: TokenResponse, 401: ErrorResponse})
    def login(self, request, data: LoginSchema):
        user = authenticate(username=data.username, password=data.password)
        if not user:
            print("test")
            return 401, ErrorResponse(detail="Wrong creds.")

        token, _ = AuthToken.objects.get_or_create(user=user)
        token.key = AuthToken.generate_token()
        token.save()

        return 200, {"token": token.key}

    @http_post("/signup", response={201: TokenResponse, 400: ErrorResponse})
    def signup(self, request, data: SignupSchema):
        if User.objects.filter(username=data.username).exists():
            return 400, {"detail": "Username already exists"}
        if User.objects.filter(email=data.email).exists():
            return 400, {"detail": "Email already exists"}

        user = User.objects.create_user(
            username=data.username,
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
        )
        user.set_password(data.password)
        user.save()
        token, _ = AuthToken.objects.get_or_create(user=user)
        token.key = AuthToken.generate_token()
        token.save()

        return 201, {"token": token.key}


@api_controller("/dashboard", auth=SimpleTokenAuth())
class DashboardController:
    @http_get("/me", response=SelfUserResponse)
    def welcome(self, request):
        # print(request.user.id)
        return request.user
