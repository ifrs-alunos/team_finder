from django import template

register = template.Library()


@register.filter
def add_classes(field, classes):
    return field.as_widget(attrs={'class': classes})


@register.filter
def add_property(field, props):
    pairs = props.split(",")
    attrs = {}
    for pair in pairs:
        attr, val = pair.split()
        attrs[attr] = val
    return field.as_widget(attrs=attrs)
