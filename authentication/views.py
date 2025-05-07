# api/auth.py
from typing import Optional

from django.contrib.auth import authenticate
from ninja import File, ModelSchema, Schema, UploadedFile
from ninja_extra import api_controller, http_get, http_post

from authentication.auth import SimpleTokenAuth

from .models import AuthToken, Resume, User, UserProfile


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
    cv: Optional[str] = None

    class Meta:
        model = User
        exclude = "password", "is_superuser", "is_staff", "groups", "user_permissions"


class ProfileResponse(ModelSchema):
    first_name: str
    last_name: str
    email: str

    class Meta:
        model = UserProfile
        fields = "__all__"


class ErrorResponse(Schema):
    detail: str


@api_controller("/auth", tags=["Authentication"])
class AuthController:
    @http_post("/login", response={200: TokenResponse, 401: ErrorResponse})
    def login(self, request, data: LoginSchema):
        user = authenticate(username=data.username.lower(), password=data.password)
        if not user:
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


@api_controller("/dashboard", auth=SimpleTokenAuth(), tags=["Dashboard"])
class DashboardController:
    @http_get("/me", response=SelfUserResponse)
    def welcome(self, request):
        request.user.cv = request.user.resume.resume_file
        return request.user

    @http_get("self_profile/", response=ProfileResponse)
    def get_user(self, request):
        UserProfile.objects.get_or_create(user=request.user)
        request.user.profile.first_name = request.user.first_name
        request.user.profile.last_name = request.user.last_name
        request.user.profile.email = request.user.email
        return request.user.profile

    @http_get(
        "profile/{username}",
        response={200: ProfileResponse, 404: ErrorResponse},
        auth=None,
    )
    def get_user_by_username(self, request, username: str):
        """
        Get user profile by username.
        """
        try:
            user = User.objects.get(username=username)
            if user.user_type != "seeker":
                return 404, {"detail": "User not found"}
            UserProfile.objects.get_or_create(user=user)
            user.profile.first_name = user.first_name
            user.profile.last_name = user.last_name
            user.profile.email = user.email
            return user.profile
        except User.DoesNotExist:
            return 404, {"detail": "User not found"}


@api_controller("/profile", auth=SimpleTokenAuth(), tags=["Profile"])
class ProfileController:
    @http_get("/me", response=SelfUserResponse)
    def me(self, request):
        return request.user

    @http_post("/settype", response={200: SelfUserResponse, 400: ErrorResponse})
    def set_user_type(self, request, user_type: str):
        """
        Set the user type for the authenticated user.
        Choices are 'seeker' and 'employer'."
        """
        if user_type not in ["seeker", "employer"]:
            return 400, {"detail": "Invalid user type"}

        user = request.user
        user.user_type = user_type
        user.save()
        return 200, user

    @http_post("/cv")
    def upload_cv(self, request, file: UploadedFile = File(...)):
        user = request.user
        cv_model, _ = Resume.objects.get_or_create(user=user)
        cv_model.resume_file = file
        cv_model.save()

        return 200, {
            "detail": "CV uploaded successfully",
            "cv": cv_model.resume_file.url,
        }
