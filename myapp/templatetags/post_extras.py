from django import template

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

register = template.Library()


@register.filter
def model_type(value):
    return type(value).__name__


@register.filter
def get_posted_at_display(posted_at):
    return f'{posted_at.strftime("%Hh%M, %d %b %y")}'


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user == context["user"]:
        return "vous avez"
    else:
        return f'{user.username} a'
