from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET' and request.user.is_authenticated and request.user.is_superuser == True:
            return True

        if request.method == 'POST':
            return True
