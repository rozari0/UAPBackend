from django.contrib import admin

from .models import Course, Lesson, Skill


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1
    fields = ("title", "content", "video_url")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "get_skills")
    search_fields = ("title",)
    inlines = [LessonInline]

    def get_skills(self, obj):
        return ", ".join([skill.name for skill in obj.skills.all()])

    get_skills.short_description = "Skills"


admin.site.register(Skill)
