from rest_framework import permissions


class IsAdminOrAction(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'me':
            return True
        return (request.user.is_authenticated and
                request.user.role == 'admin'
        )
    

class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.role in ('admin'
                                      'moderator',
                )
        )


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.role in ('admin',
                                      'moderator',
                                      'user',
                )
        )
