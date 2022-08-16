from rest_framework import permissions

from .models import Course


class CourseInstructorPerm(permissions.BasePermission):
    message = "You are not a course instructor."

    """
        Check if the request.user's type is INSTRUCTOR
        If not they cannot create course and lessons for that particular course.
    """

    def has_permission(self, request, view):

        if request.user.type == "INSTRUCTOR":
            return True


class CreateLessonPerm(permissions.BasePermission):
    message = "You are not a course instructor."

    """
        Check particular course
    """

    def has_permission(self, request, view):

        if Course.objects.filter(instructor=request.user).exists():
            return True


# class CourseInstrutorPerm(permissions.BasePermission):

#     message = "Only Course instructor is allowed to perform this action."

#     def has_object_permission(self, request, view, obj):

#         if not request.user.is_authenticated:
#             if request.method in permissions.SAFE_METHODS:
#                 return True
#             return False

#         if request.method in permissions.SAFE_METHODS:
#             return True

#         return obj.instructor == request.user


class CourseInstrutorPerm(permissions.BasePermission):

    message = "Only Course instructor is allowed to perform this action."

    def has_object_permission(self, request, view, obj):

        if obj.status == "Pending" and request.user != obj.instructor:
            return False

        if not request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.instructor == request.user


class LessonsDetailPerm(permissions.BasePermission):

    message = "You are not enrolled in this course, hence can't view lessons."

    def has_permission(self, request, view):

        course = Course.objects.get(slug=view.kwargs.get("slug"))

        if request.method in permissions.SAFE_METHODS:

            if course.instructor == request.user:
                return True

            elif course.enrollments.filter(student=request.user).exists():
                return True

            return False

        return course.instructor == request.user


class SingleLessonPerm(permissions.BasePermission):
    message = "You are not allowed to view this lesson."

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            if obj.course.enrollments.filter(student=request.user).exists():
                return True
            elif obj.course.instructor == request.user:
                return True

            return False

        return obj.course.instructor == request.user
