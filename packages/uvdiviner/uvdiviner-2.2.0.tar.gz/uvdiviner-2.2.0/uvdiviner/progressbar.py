#!/usr/bin/env python3
import time
import sys
import traceback
import warnings

import colorama
from colorama import Fore, Style

colorama.init()

def warning_show(message, category, filename, lineno, file=None, line=None):
    tb = traceback.extract_stack()[:-1]
    tb_message = ''.join(traceback.format_list(tb))
    warning_message = "Traceback (most recent call last):\n"
    warning_message += tb_message
    warning_message += f"{category.__name__}: {message}\n\n"
    if file is not None:
        file.write(warning_message)
    else:
        sys.stderr.write(warning_message)

def ProgressBar(progress, name="", fill="━", fill_color=Fore.RED, complete_color=Fore.YELLOW, empty_char="━"):
    if progress > 1 or progress < 0:
        warnings.warn("进度条不建议将其的值设置在0→1之外, 这可能会使得进度条的显示出现异常.", Warning)
    if progress >= 1:
        fill_color = complete_color
    if len(empty_char) > 1 or len(empty_char) == 0:
        warnings.warn("空占位符不建议将其长度设为大于一个字符的值, 这可能会使得进度条的显示出现异常.", Warning)

    bar_width = 50
    fill_char = fill_color + fill + Style.RESET_ALL
    empty_char = empty_char

    filled_length = int(progress * bar_width)
    bar = fill_char * filled_length + empty_char * (bar_width - filled_length)
    percentage = Fore.GREEN + str(round(float(progress) * 100, 1)) + "%" + Style.RESET_ALL
    print(f'{name} {bar} {percentage}\r', end='', flush=True)

warnings.showwarning = warning_show

if __name__ == "__main__":
    progress_value = 0.86
    for i in range(0, 1001, 10):
        ProgressBar(i / 1000)
        time.sleep(0.02)
    print("\n")
    ProgressBar(progress_value)
    
