"""

References
----------
- https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters
"""

from typing import Optional
import re

from repodynamics.actions import _db


class SGR:
    temp = "\033[{}m"
    reset = temp.format(0)
    text_style = {
        'normal': '0',
        'bold': '1',
        'faint': '2',
        'italic': '3',
        'underline': '4',
        'blink': '5',
        'blink_fast': '6',
        'reverse': '7',
        'conceal': '8',
        'strike': '9',
    }
    color = {
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'white': 37,
        'b_black': 90,
        'b_red': 91,
        'b_green': 92,
        'b_yellow': 93,
        'b_blue': 94,
        'b_magenta': 95,
        'b_cyan': 96,
        'b_white': 97,
    }

    @staticmethod
    def style(
        text_styles: int | str | list[int | str] = None,
        text_color: int | str | tuple = None,
        background_color: int | str | tuple = None
    ):

        def add_color(color: int | str | tuple, bg: bool = False):
            int_range = (
                list(range(40, 48)) + list(range(100, 108)) if bg else
                list(range(30, 38)) + list(range(90, 98))
            )
            int_offset = 10 if bg else 0
            rgb_code = 48 if bg else 38
            if isinstance(color, int):
                if color not in int_range:
                    raise ValueError(f"Invalid color code: {color}")
                return f"{color};"
            if isinstance(color, str):
                if color not in SGR.color:
                    raise ValueError(f"Invalid color name: {color}")
                return f"{SGR.color[color] + int_offset};"
            if isinstance(color, tuple):
                if len(color) != 3:
                    raise ValueError(f"Invalid color tuple: {color}")
                if not all(isinstance(c, int) for c in color):
                    raise ValueError(f"Invalid color tuple: {color}")
                if not all(c in range(256) for c in color):
                    raise ValueError(f"Invalid color tuple: {color}")
                return f"{rgb_code};2;{';'.join([str(c) for c in color])};"
            raise TypeError(f"Invalid color type: {type(color)}")

        style_str = ""
        if text_styles:
            if isinstance(text_styles, (str, int)):
                text_styles = [text_styles]
            if not isinstance(text_styles, list):
                raise TypeError("styles must be a string, an integer, or a list of strings or integers")
            for text_style in text_styles:
                if isinstance(text_style, int):
                    if text_style not in range(10):
                        raise ValueError(f"Invalid style code: {text_style}")
                    text_style_code = str(text_style)
                elif isinstance(text_style, str):
                    if text_style not in SGR.text_style:
                        raise ValueError(f"Invalid style name: {text_style}")
                    text_style_code = SGR.text_style[text_style]
                else:
                    raise TypeError(f"Invalid style type: {type(text_style)}")
                style_str += f"{text_style_code};"
        if text_color:
            style_str += add_color(text_color, bg=False)
        if background_color:
            style_str += add_color(background_color, bg=True)
        if not style_str:
            return SGR.reset
        return SGR.temp.format(style_str.removesuffix(";"))

    @staticmethod
    def format(text, style: str, action_name: Optional[str] = None):
        match style:
            case "error":
                s1 = SGR.style(text_styles="bold", text_color=(250, 250, 250), background_color=(255, 0, 0))
                s2 = SGR.style(text_styles="faint", text_color=(250, 250, 250), background_color=(120, 0, 0))
                return f"{s1}ERROR!{SGR.reset}{s2} {text} {SGR.reset}"
            case "warning":
                s1 = SGR.style(text_styles="bold", text_color=(250, 250, 250), background_color=(200, 140, 0))
                s2 = SGR.style(text_styles="faint", text_color=(250, 250, 250), background_color=(150, 70, 0))
                return f"{s1}WARNING! {SGR.reset}{s2}{text} {SGR.reset}"
            case "attention":
                style = SGR.style(text_styles="bold", text_color=(250, 250, 250), background_color=(0, 162, 255))
            case "info":
                style = SGR.style(text_color="b_blue")
            case "success":
                style = SGR.style(text_color="green")
            case "debug":
                style = SGR.style(text_color=(255, 255, 255))
            case "heading":
                style = SGR.style(text_styles="bold", text_color="black", background_color=_db.action_color[action_name])
                return f"{style} {text}  {SGR.reset}"
        return f"{style}{text}{SGR.reset}"


def remove_formatting(text: str):
    """
    Remove ANSI escape sequences from a string.

    Parameters
    ----------
    text

    Notes
    -----
    ANSI escape codes start with the \033 (\x1b) escape character,
    followed by '[', then zero or more numbers separated by ';', and ending with a letter.

    Regex Details:
    - [0-?]*: This part matches zero or more characters in the range between 0 and ?.
    This covers all the numbers and semicolons that might be present in the escape sequence.
    For example, in the code \x1b[31;42m, 31 and 42 are matched by this part.
    - [ -/]*: This is a sequence of characters that might appear in some of the ANSI sequences.
    It's more of a catch-all for certain sequences and may not be strictly necessary for many common sequences.
    But it ensures we catch even those rare ANSI codes.
    - [@-~]: Finally, ANSI escape sequences end with a character from @ to ~:
    @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
    [ \ ] ^ _ ` a b c d e f g h i j k l m n o p q r s t u v w x y z {.
    This part matches that ending character. This character typically indicates what action
    should be taken (e.g., change color, move cursor, clear screen, etc.).
    """
    return re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]').sub('', text)
