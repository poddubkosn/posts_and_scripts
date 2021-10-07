from django import template
register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})

@register.filter
def len_15(word):
    word_new = word[:15]
    return word_new

@register.filter
def len_30(word):
    word_new = word[:30]
    return word_new