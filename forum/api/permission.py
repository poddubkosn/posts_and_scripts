from rest_framework import permissions


class CustomerAccessPermission(permissions.BasePermission):
    message = 'Изменение чужого контента запрещено!.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
