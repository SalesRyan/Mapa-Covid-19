from django import template
register = template.Library()
@register.filter
def float_filter_tag(numero):
    try:
        return str(round(numero,2)).replace('.',',')
    except:
        return None