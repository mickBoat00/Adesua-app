from rest_framework import permissions

from .models import Course


class IsOwner(permissions.BasePermission):

    message = "You are not allowed to perform this action."

    def has_permission(self, request, view):

        print("obj")

        return False

    def has_object_permission(self, request, view, obj):

        print("obj", obj)

        if request.method in permissions.SAFE_METHODS:
            if obj.course.instructor == request.user.profile:
                return True
            else:
                return request.user.profile in obj.course.students.all()

        return obj.course.instructor == request.user.profile


class EnrolledStudent(permissions.BasePermission):
    message = "You are not allowed to perform this action."

    def has_object_permission(self, request, view, obj):
        print("qqqqq")

        if obj.students.filter(user=self.request.user).exists():
            print("obj", obj)
            return True


# --------------------------------------------------------------------------------------------------
class CreateLessonPerm(permissions.BasePermission):
    message = "You are not a course instructor."

    """
        Check particular course
    """

    def has_permission(self, request, view):

        if Course.objects.filter(instructor=request.user.profile).exists():
            return True


class CourseInstrutorPerm(permissions.BasePermission):

    message = "Only Course instructor is allowed to perform this action."

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.instructor == request.user.profile


class LessonsDetailPerm(permissions.BasePermission):

    message = "You are not allowed to perform this action."

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            course = Course.objects.get(slug=view.kwargs.get("slug"))

            if course.instructor == request.user.profile:
                return True

            elif course.students.filter(profile=request.user.profile).exists():
                return True

            return False


class SingleLessonPerm(permissions.BasePermission):
    message = "You are not allowed to view this lesson."

    def has_object_permission(self, request, view, obj):

        print("djddjddjd")

        if request.method in permissions.SAFE_METHODS:
            if obj.course.students.filter(profile=request.user.profile).exists():
                return True
            elif obj.course.instructor == request.user.profile:
                return True

            return False

        return obj.course.instructor == request.user.profile
