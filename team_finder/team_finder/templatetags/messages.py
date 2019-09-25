from django import template

register = template.Library()

@register.inclusion_tag('core/toast_messages.html', takes_context=True)
def toast_messages(context):
    return {
        'messages': context['messages']
    }