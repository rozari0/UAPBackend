from typing import List
from django.shortcuts import get_object_or_404
from ninja_extra import http_post, api_controller, http_get
from ninja import Schema, ModelSchema

from authentication.auth import SimpleTokenAuth
from .models import Course, Skill, Lesson


class SkillSchema(ModelSchema):
    class Meta:
        model = Skill
        fields = "__all__"


class CourseSchema(ModelSchema):
    skills: list[SkillSchema] = []

    class Meta:
        model = Course
        fields = "__all__"


class LessonSchema(ModelSchema):
    class Meta:
        model = Lesson
        fields = "__all__"


class SingleCourseSchema(ModelSchema):
    skills: list[SkillSchema] = []
    lessons: list[LessonSchema] = []

    class Meta:
        model = Course
        fields = "__all__"


@api_controller("/course", tags=["Course"])
class CourseController:
    @http_get("/list", response=List[CourseSchema])
    def list_courses(self, request):
        courses = Course.objects.all()
        print(courses)
        return courses

    @http_get("/{course_id}", response=SingleCourseSchema)
    def get_course(self, request, course_id: int):
        try:
            course = Course.objects.get(id=course_id)
            return course
        except Course.DoesNotExist:
            return None

    @http_post("/mark_completed", response=CourseSchema, auth=SimpleTokenAuth())
    def mark_completed(self, request, course_id: int):
        try:
            user = request.user
            course = get_object_or_404(Course, id=course_id)
            user.profile.completed_course.add(Course)
            for skill in course.skills.all():
                user.profile.verified_skills.add(skill)
            user.profile.save()
        except Course.DoesNotExist:
            return None
