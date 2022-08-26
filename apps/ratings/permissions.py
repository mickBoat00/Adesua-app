from rest_framework import permissions

from apps.students.models import CourseEnrollment


class CourseRatingPerm(permissions.BasePermission):

    message = "Only course students will be allowed to perform this action."

    def has_permission(self, request, view):

        if request.user.is_anonymous:
            if request.method in permissions.SAFE_METHODS:
                return True

        elif request.method in permissions.SAFE_METHODS:

            return True
        else:
            return CourseEnrollment.objects.filter(student=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.rater == request.user
