from django.contrib.auth.models import Permission
from graphql_jwt.decorators import user_passes_test


def permission_required(perm):

    def check_perms(user):
        if isinstance(perm, str):
            perms = (perm,)
        else:
            perms = perm
        perm_tuple = user.user_permissions.all() | Permission.objects.filter(group__user=user)
        perm_tuple = [x.codename for x in perm_tuple]
        if set(perms).issubset(set(perm_tuple)):
            return True
        return False
    return user_passes_test(check_perms)

# example for use with decorator
# permission_required(['add_immunoserology']) without app_label