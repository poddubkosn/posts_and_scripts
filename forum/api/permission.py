from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class CustomerAccessPermission(permissions.BasePermission):
    message = 'Изменение чужого контента запрещено!.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True


class CustomerAccessPermissionFollow(permissions.BasePermission):
    message = 'Чтение и изменение чужых подписок запрещено!.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
