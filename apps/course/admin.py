from django.contrib import admin

from .models import Category, Course, Lesson, Student

admin.site.register(Category)


class LessonInLine(admin.StackedInline):
    model = Lesson
    fields = ["title", "slug", "description", "video"]
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInLine]
    list_display = ["title", "slug", "pay", "price"]
    list_filter = ["price", "pay"]
    readonly_fields = ["instructor", "slug", "created_on", "updated_on"]


admin.site.register(Course, CourseAdmin)


# admin.site.register(Lesson)
admin.site.register(Student)
