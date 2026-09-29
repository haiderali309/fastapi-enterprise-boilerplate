from .roles import Role
from .permissions import Permission

# -----------------------------------------------------------------------------
# Role Policy Mapping
# -----------------------------------------------------------------------------
# Maps each Role to its corresponding set of allowed Permissions.
# To grant a permission to a role, simply include it in the set below.
ROLE_POLICY = {
    Role.SUPER_ADMIN: {
        Permission.CREATE_USER,
        Permission.UPDATE_USER,
        Permission.DELETE_USER,
        Permission.VIEW_USER,
        Permission.UPDATE_PROFILE,
    },
    Role.ADMIN: {
        Permission.CREATE_USER,
        Permission.UPDATE_USER,
        Permission.VIEW_USER,
        Permission.DELETE_USER,
    },
    Role.USER: {
        Permission.UPDATE_PROFILE,
    },
}