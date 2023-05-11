import itertools
import re

from operator import add

from django import template
from django.utils.functional import SimpleLazyObject
from django.utils.safestring import mark_safe, SafeString


register = template.Library()
re_newlines = SimpleLazyObject(lambda *_: re.compile(r"\r\n|\r", 0))


def _paras_to_lines(paras: list[str]) -> list[str]:
    """Merge words and decrement slash_n"""
    lines, line = [], ''
    for item in paras:
        if slashes_len := sum(char == '\n' for char in item):
            lines.append(line)
            if slashes_len >= 2:
                lines += ['\n'] * (len(item) - 1)
            line = ''
        else:
            line += item
    if line:
        lines.append(line)
    return lines


def _divide_lines(lines: list[str], max_line_len: int) -> list[str]:
    """
    1. Get accumulated words len.
    2. Get indexes by accumulated words len.
    3. Get words sentences from dividing by indexes.
    """
    correct_lines = []
    for line in lines:
        if len(line) > max_line_len:
            words = re.split(r'(\s+)', line)
            white_space = 1
            words_len = itertools.accumulate((len(word) + white_space
                                              for word in words), add)
            # get indexes
            _max_line_len = max_line_len
            indexes = [0]
            for idx, word_len in enumerate(words_len):
                if word_len > _max_line_len:
                    _max_line_len += max_line_len
                    indexes.append(idx)
            indexes.append(len(words))

            # get words by indexes
            correct_lines += (''.join(words[last_idx:idx]) for last_idx, idx in
                              zip(indexes[:len(words) - 1], indexes[1:]))
        else:
            correct_lines.append(line)
    return correct_lines


def _get_correct_lines(paras: list[str], max_line_len: int,
                       max_line_count: int) -> tuple[str, int]:
    lines = _paras_to_lines(paras)
    correct_lines = _divide_lines(lines, max_line_len)

    continue_symbol = ' ...'
    lines_html = ''.join(
        f"<p>{line[:-len(continue_symbol)]}{continue_symbol}</p>"
        if index == max_line_count-1 and len(correct_lines) > max_line_count
        else f'<p>{line}</p>'
        for index, line in enumerate(correct_lines[:max_line_count])
    )

    return lines_html, len(correct_lines) > max_line_count  # need Read more ?


@register.filter(name="truncate_line")
def truncate_line(
    _html: str,
    args: str = '"4","63","Read more","comment_message"'
) -> SafeString:
    """
    {{ subject | truncate_line:'"4","63","Read more","comment_message"' }}
    Works only with all arguments.
    """
    if args == '"4","63","Read more","comment_message"':
        args = 4, 63, "Read more", "comment_message"  # default
        max_line_count, max_line_len, message, _class = args
    else:
        # serialize input
        args = (arg.strip('"').rstrip(' ') for arg in args.split(','))
        max_line_count, max_line_len, message, _class = args
        max_line_len, max_line_count = int(max_line_len), int(max_line_count)

    # parse html to divided lines and restrict by max_line_len, max_line_count
    normalize_html = re_newlines.sub("\n", str(_html))
    paras = re.split(r'(\s+)', str(normalize_html))
    lines_html, _read_more = _get_correct_lines(
        paras, max_line_len, max_line_count
    )

    if _read_more:
        message_html = f"<span class='{_class}'>{message}</span"
        return mark_safe(f"<p>{lines_html}{message_html}</p>")
    return mark_safe(f"<p>{lines_html}</p>")
