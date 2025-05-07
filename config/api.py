from authentication.views import AuthController, DashboardController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()

api.register_controllers(
    AuthController,
    DashboardController,
)
