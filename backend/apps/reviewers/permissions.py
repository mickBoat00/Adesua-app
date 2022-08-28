from rest_framework import permissions


class ReviewerPerm(permissions.BasePermission):
    message = "You are not allowed because you're not a reviewer."

    def has_permission(self, request, view):
        if request.user.type == "REVIEWER":
            return True

    def has_object_permission(self, request, view, obj):

        if request.user.type == "REVIEWER":
            return True
