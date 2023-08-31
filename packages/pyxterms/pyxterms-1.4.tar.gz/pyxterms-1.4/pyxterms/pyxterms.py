"""
made by akame/@dhvd

https://github.com/lutherantz

Version 1.0
"""

import os
import sys
import time
import ctypes
import msvcrt
from datetime import datetime
from os import system as _system # thanks pystyle

if os.name == 'nt':
    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]
        
class Term:
    """
    Vars:
        Windows : if os is on Windows
    Funcs:
        clear: clear terminal
        title: set terminal title
        cmd: do a command
        _terminal_size: get terminal size more complex
    """
    Windows = os.name == 'nt' # thanks pystyle

    def clear():
        return _system("cls" if Term.Windows else "clear")
    
    def title(name: int or str):
        _system(f"title {name}")

    def cmd(comd):
        _system(comd)
    
    def _terminal_size():
        try:
            import shutil
            size = shutil.get_terminal_size()
            return size
        except (ImportError, AttributeError):
            try:
                columns = int(os.environ.get('COLUMNS', 80))
                lines = int(os.environ.get('LINES', 24))
                return os.terminal_size((columns, lines))
            except (ValueError, TypeError):
                return os.terminal_size()

class Cursor:
    # https://stackoverflow.com/questions/5174810/how-to-turn-off-blinking-cursor-in-command-window
    """
    Funcs:
        hide_cursor: hide cursor in the terminal
        show_cursor: show cursor in the terminal
    """
    def hide_cursor():
        if Term.Windows:
            ci = _CursorInfo()
            handle = ctypes.windll.kernel32.GetStdHandle(-11)
            ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
            ci.visible = False
            ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
        elif os.name == 'posix':
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()

    def show_cursor():
        if Term.Windows:
            ci = _CursorInfo()
            handle = ctypes.windll.kernel32.GetStdHandle(-11)
            ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
            ci.visible = True
            ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
        elif os.name == 'posix':
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()

class Color:
    """
    Funcs:
        begin: do color
        reset: reset color
        fade: do a linear gradient
    """
    def begin(color: str):
        return f"\033[38;2;{color}m"
    
    def reset():
        return "\033[38;2;255;255;255m"

    def fade(content: str, start: str or int = "", color = str, date: bool = False) -> str:
        col = f"\033[38;2;{color}m"
        if start == "":
            if date:
                first_part = f"[{datetime.now().strftime('%H:%M:%S')}] {content}"
            else:
                first_part = f"{content}"
        else:
            if date:
                first_part = f"[{start}] | [{datetime.now().strftime('%H:%M:%S')}] {content}"
            else:
                first_part = f"[{start}] | {content}"

        new_part = ""
            
        counter = 0
        for caracter in first_part:
            new_part += col.replace('-', str(225 - counter * int(255/len(first_part)))) + caracter
            counter += 1 

        return f"{new_part}"
    
    # Thanks pystyle for color ur da best XD

    red = begin('255;0;0')
    green = begin('0;255;0')
    blue = begin('0;0;255')

    white = begin('255;255;255')
    black = begin('0;0;0')
    gray = begin('150;150;150')

    yellow = begin('255;255;0')
    purple = begin('255;0;255')
    cyan = begin('0;255;255')

    orange = begin('255;150;0')
    pink = begin('255;0;150')
    turquoise = begin('0;150;255')

    light_gray = begin('200;200;200')
    dark_gray = begin('100;100;100')

    light_red = begin('255;100;100')
    light_green = begin('100;255;100')
    light_blue = begin('100;100;255')

    dark_red = begin('100;0;0')
    dark_green = begin('0;100;0')
    dark_blue = begin('0;0;100')
    reset = white

    black_to_white = "-;-;-"
    black_to_red = "-;0;0"
    black_to_green = "0;-;0"
    black_to_blue = "0;0;-"

    white_to_black = "-;-;-"
    white_to_red = "255;-;-"
    white_to_green = "-;255;-"
    white_to_blue = "-;-;255"

    red_to_black = "-;0;0"
    red_to_white = "255;-;-"
    red_to_yellow = "255;-;0"
    red_to_purple = "255;0;-"

    green_to_black = "0;n;0"
    green_to_white = "-;255;-"
    green_to_yellow = "-;255;0"
    green_to_cyan = "0;255;-"

    blue_to_black = "0;0;-"
    blue_to_white = "-;-;255"
    blue_to_cyan = "0;-;255"
    blue_to_purple = "-;0;255"

    yellow_to_red = "255;-;0"
    yellow_to_green = "-;255;0"

    purple_to_red = "255;0;-"
    purple_to_blue = "-;0;255"

    cyan_to_green = "0;255;-"
    cyan_to_blue = "0;-;255"

class Anim:
    """
    Funcs:
        typing: do a typewriter effect
    """
    def typing(text: str, slp: int):
        for x in text:
            time.sleep(slp)
            sys.stdout.write(x)
            sys.stdout.flush()
        print("")

class Center: 
    """
    Funcs:
        center: center x and y
        center_x: center in x
        center_y: center in y
    """  
    def center(text):
        col = Term._terminal_size().columns
        lin = Term._terminal_size().lines
        
        text_lines = text.splitlines()
        max_line_length = max(len(line) for line in text_lines)
        horizontal_padding = (col - max_line_length) // 2
        vertical_padding = (lin - len(text_lines)) // 2

        centered_text_lines = [
            " " * horizontal_padding + line.center(max_line_length) + " " * horizontal_padding
            for line in text_lines
        ]

        top_padding = "\n" * vertical_padding
        centered_text = top_padding + "\n".join(centered_text_lines)

        return centered_text

    def center_x(text: str):
        col = Term._terminal_size().columns
        
        text_lines = text.splitlines()
        max_line_length = max(len(line) for line in text_lines)
        horizontal_padding = (col - max_line_length) // 2

        centered_text_lines = [
            " " * horizontal_padding + line
            for line in text_lines
        ]

        centered_text = "\n".join(centered_text_lines)

        return centered_text

    def center_y(text: str):
        lin = Term._terminal_size().lines
        
        text_lines = text.splitlines()
        vertical_padding = (lin - len(text_lines)) // 2

        top_padding = "\n" * vertical_padding
        bottom_padding = "\n" * (lin - len(text_lines) - vertical_padding)

        centered_text = top_padding + text + bottom_padding

        return centered_text