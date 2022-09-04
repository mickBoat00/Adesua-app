from rest_framework import permissions

from apps.enrollment.models import CourseEnrollment


class CourseRatingPerm(permissions.BasePermission):

    message = "Only course students will be allowed to perform this action."

    def has_permission(self, request, view):

        if request.user.is_anonymous:
            if request.method in permissions.SAFE_METHODS:
                return True

        if request.method in permissions.SAFE_METHODS:
            return True

        else:

            return CourseEnrollment.objects.filter(
                course__slug=view.kwargs.get("courseslug"), student=request.user
            ).exists()

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return CourseEnrollment.objects.filter(
            course__slug=view.kwargs.get("courseslug"), student=request.user
        ).exists()
