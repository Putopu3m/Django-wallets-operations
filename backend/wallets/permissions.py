from rest_framework.permissions import BasePermission


class IsWalletOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.users.all()
