from ninja_extra import NinjaExtraAPI

from authentication.views import (
    AuthController,
    DashboardController,
    ProfileController,
    EmployerController,
)
from course.api.user import CourseController
from course.api.skills import SkillsController

api = NinjaExtraAPI()

api.register_controllers(
    AuthController,
    DashboardController,
    ProfileController,
    EmployerController,
)
api.register_controllers(
    CourseController,
    SkillsController,
)
