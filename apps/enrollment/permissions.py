from rest_framework import permissions


class EnrolledStudentPermission(permissions.BasePermission):
    message = "You have to be a student to enroll in a course."

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            if request.method in permissions.SAFE_METHODS:
                return True

        elif request.user.type == "STUDENT":
            return True
