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
    match_img = re.findall(r'<img.*src=.*</p>', word, re.X)
    #match_iframe = re.match(r'(.*iframe).*(height=".*")(src=.*)(width=".*")(.*)', word)
    match_iframe = re.match(r'(.*iframe).*(src=.*)(width=".*")(.*)', word)
    if match_iframe:
        # return word
        # return (f'{match_iframe[1]} allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="" frameborder="0" height="315"{match_iframe[3]}'
        #         f'title="YouTube video player" width="560" {match_iframe[5]}')
        return (f'{match_iframe[1]} class="embed-responsive-item" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="" frameborder="0" {match_iframe[2]}'
                f' title="YouTube video player"></p></iframe>')
    # if match_text_only:
    #     return match_text_only
    else:
        if match_img:
            return word[:100] + str(match_img)
        return word[:200]
