from ninja_extra import NinjaExtraAPI

from authentication.views import AuthController, DashboardController, ProfileController

api = NinjaExtraAPI()

api.register_controllers(
    AuthController,
    DashboardController,
    ProfileController,
)
