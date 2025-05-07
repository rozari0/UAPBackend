from typing import List
from ninja_extra import api_controller, http_get, http_post
from ..models import Skill
from .user import SkillSchema
from authentication.views import ProfileResponse
from authentication.models import UserProfile
from django.db.models import Count, Q


@api_controller("/skills", tags=["Skills"])
class SkillsController:
    @http_get("/", response=List[SkillSchema])
    def get_skills(self, request):
        """
        Get all skills
        """
        return Skill.objects.all()

    @http_post("/filtered_user", response=List[ProfileResponse])
    def filtered_user(self, request, skills: List[int] = None):
        """
        Get all users with filter
        """
        profiles = UserProfile.objects.prefetch_related("user").all()
        if skills:
            # Annotate profiles with a count of how many verified skills match
            profiles = profiles.annotate(
                verified_skill_match_count=Count(
                    "verified_skills", filter=Q(verified_skills__id__in=skills)
                )
            )

            # Order profiles by the number of matching verified skills, in descending order
            profiles = profiles.filter(verified_skill_match_count__gt=0).order_by(
                "-verified_skill_match_count"
            )
        for profile in profiles:
            profile.verified_skill_match_count = profile.verified_skills.count()
            profile.first_name = profile.user.first_name
            profile.last_name = profile.user.last_name
            profile.email = profile.user.email
        return profiles
