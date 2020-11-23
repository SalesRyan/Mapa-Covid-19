from django import template
register = template.Library()
@register.filter
def float_filter_tag(numero):
    try:
        return str(round(numero,2)).replace('.',',')
    except:
        return None

@register.filter
def add_one_tag(numero):
    try:
        return int(numero)+1
    except:
        return None

@register.filter
def list_tag(lista,index):
    try:
        return lista[int(index)]
    except:
        return None