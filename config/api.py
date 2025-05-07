from ninja_extra import NinjaExtraAPI

from authentication.views import AuthController, DashboardController, ProfileController
from course.api.user import CourseController
from course.api.skills import SkillsController

api = NinjaExtraAPI()

api.register_controllers(
    AuthController,
    DashboardController,
    ProfileController,
)
api.register_controllers(
    CourseController,
    SkillsController,
)
