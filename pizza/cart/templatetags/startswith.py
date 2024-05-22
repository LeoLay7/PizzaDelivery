import django.template

register = django.template.Library()


@register.filter
def startswith(value: str, chars):
    if value.startswith(chars):
        return True
    return False
