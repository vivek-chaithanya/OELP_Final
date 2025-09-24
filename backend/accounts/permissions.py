from rest_framework import permissions


class RoleNames:
    SUPERADMIN = "SuperAdmin"
    ADMIN = "Admin"
    AGRONOMIST = "Agronomist"
    SUPPORT = "Support"
    ANALYST = "Analyst"
    BUSINESS = "Business"
    DEVELOPMENT = "Development"
    USER = "User"


def user_has_role(user, role_name: str) -> bool:
    return bool(getattr(user, "role", None) and user.role and user.role.name == role_name)


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return user_has_role(request.user, RoleNames.SUPERADMIN)


class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return user_has_role(request.user, RoleNames.SUPERADMIN) or user_has_role(request.user, RoleNames.ADMIN)


class RegionScopedPermission(permissions.BasePermission):
    """Allow SuperAdmin to access all, Admin limited to their region, users to their own resources."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user_has_role(user, RoleNames.SUPERADMIN):
            return True
        if user_has_role(user, RoleNames.ADMIN):
            user_region = getattr(user, "region", None)
            # Object may have region directly or via farm/field
            obj_region = getattr(obj, "region", None)
            if not obj_region and hasattr(obj, "farm"):
                obj_region = getattr(obj.farm, "region", None)
            if not obj_region and hasattr(obj, "field"):
                farm = getattr(obj.field, "farm", None)
                obj_region = getattr(farm, "region", None) if farm else None
            return user_region and obj_region and user_region_id(obj_region) == user_region.id
        # Fallback to owner checks on models that have owner relationship
        if hasattr(obj, 'owner'):
            return obj.owner_id == user.id
        return False


def user_region_id(region_obj):
    return getattr(region_obj, "id", None)

