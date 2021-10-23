import re
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


@register.filter
def only_text(word):
    word = word.split('\n')
    word = ' '.join(word)
    match_img = re.match(r'(.*)(<img.*src=.*</p>)', word,)
    match_iframe = re.match(r'(.*)<p><iframe.*(src=.*)'
                            'width=".*"></iframe></p>(.*)', word,)
    if match_iframe:
        return (f'{match_iframe.group(1)[:100]}<div class="ratio ratio-16x9">'
                '<iframe class="embed-responsive-item" allow="accelerometer;'
                ' autoplay; clipboard-write; encrypted-media; gyroscope;'
                ' picture-in-picture" allowfullscreen="" frameborder="0"'
                f' {match_iframe[2]} title="YouTube video player">'
                f'</iframe></div>{match_iframe.group(3)[:100]}')
    else:
        if match_img:
            return (f'{match_img.group(1)[:100]} {match_img.group(2)}')
        return word[:200]


@register.filter
def only_text_detail(word):
    word = word.split('\n')
    word = ' '.join(word)
    match_img = re.match(r'(.*)(<img.*src=.*</p>)', word,)
    match_iframe = re.match(r'(.*)<p><iframe.*(src=.*)'
                            'width=".*"></iframe></p>(.*)', word,)
    if match_iframe:
        return (f'{match_iframe.group(1)}<div class="ratio ratio-16x9"><iframe'
                ' class="embed-responsive-item" allow="accelerometer;'
                ' autoplay; clipboard-write; encrypted-media; gyroscope;'
                ' picture-in-picture" allowfullscreen="" frameborder="0"'
                f' {match_iframe[2]} title="YouTube video player">'
                f'</iframe></div>{match_iframe.group(3)}')
    else:
        if match_img:
            return (f'{match_img.group(1)} {match_img.group(2)}')
        return word
