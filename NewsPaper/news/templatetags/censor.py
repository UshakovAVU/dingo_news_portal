from django import template
import re

register = template.Library()

FORBIDDEN_WORDS = 'редиска', 'плохая', 'нехороший'


@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        raise TypeError("Фильтр censor может применяться только к строкам")

    pattern = r'\b(' + '|'.join(re.escape(word) for word in FORBIDDEN_WORDS) + r')\b'

    def replace_match(match):
        word = match.group(0)
        if word[0].isupper():
            return word[0] + '*' * (len(word) - 1)
        return '*' * len(word)

    return re.sub(pattern, replace_match, value, flags=re.IGNORECASE)
