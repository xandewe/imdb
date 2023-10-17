from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        return bool(request.user.is_superuser and request.user.is_authenticated)


class ReviewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        if request.method == 'POST' and request.user.is_authenticated:
            return True

        if request.user.is_authenticated or request.user.is_superuser:
            return True
