from django import template

register = template.Library()

@register.filter(name="has_permission")
def has_permission(user, action_name):
    if user.is_superuser:
        return True
    return user.profile.positions.filter(action__name=action_name).exists()

