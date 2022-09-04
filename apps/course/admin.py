from django.contrib import admin

from .models import Course, Curriculum, Lesson, Year

admin.site.register(Curriculum)
admin.site.register(Year)


class LessonInLine(admin.StackedInline):
    model = Lesson
    fields = ["title", "slug", "description", "video"]
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInLine]
    list_display = ["curriculum", "year", "title", "slug", "enrollment_type", "price"]
    list_filter = ["curriculum", "year", "price", "enrollment_type"]
    readonly_fields = ["slug", "created_on", "updated_on"]


admin.site.register(Course, CourseAdmin)


admin.site.register(Lesson)
