from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Только авторизованный продавец и владелец товара может его изменять или удалять
        """
        if request.method in SAFE_METHODS:
            return True
        # try:
            return request.user.is_authenticated and request.user.role == 'Worker'
        # except AttributeError:
        #     return False