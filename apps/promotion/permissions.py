from rest_framework import generics, permissions, response, viewsets

class InstructorAdminOnly(permissions.BasePermission):
    message = "You are not a course Instructor or an ADMIN."

    """
        Check if the request.user's type is INSTRUCTOR or and ADMIN
    """

    def has_permission(self, request, view):

        if request.user.type == "INSTRUCTOR" or request.user.type == "ADMIN":
            return True