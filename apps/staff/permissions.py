from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow ADMIN or MANAGER roles to edit/delete objects.
    All authenticated users can perform read-only (GET, HEAD, OPTIONS) requests.
    """
    def has_permission(self, request, view):
        # Allow safe read-only methods for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True

        # Restrict write operations (POST, PUT, PATCH, DELETE) to ADMIN or MANAGER
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Checks role attribute if present, or falls back to superuser status
        user_role = getattr(user, 'role', None)
        return user_role in ['ADMIN', 'MANAGER'] or user.is_superuser