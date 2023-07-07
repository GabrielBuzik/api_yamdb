from rest_framework import permissions


class IsAdminOrAction(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'me':
            return True
        return (
            request.user.is_authenticated
            and (
                request.user.role == 'admin'
                or request.user.is_superuser
            )
        )


class IsGetOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in (
                'admin'
                'moderator',
            )
        )


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in (
                'admin',
                'moderator',
                'user',
            )
        )


class AuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role in (
                'admin',
                'moderator',
            )
        )
