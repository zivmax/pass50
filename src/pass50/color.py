from colorama import Back, Fore, Style, init
init(autoreset=True)


class Colored(object):
    @classmethod
    def red(cls, s):
        return Style.BRIGHT + Fore.RED + s + Fore.RESET

    @classmethod
    def green(cls, s):
        return Style.BRIGHT + Fore.GREEN + s + Fore.RESET

    @classmethod
    def yellow(cls, s):
        return Style.BRIGHT + Fore.YELLOW + s + Fore.RESET

    @classmethod
    def blue(cls, s):
        return Style.BRIGHT + Fore.BLUE + s + Fore.RESET

    @classmethod
    def magenta(cls, s):
        return Style.BRIGHT + Fore.MAGENTA + s + Fore.RESET

    @classmethod
    def cyan(cls, s):
        return Style.BRIGHT + Fore.CYAN + s + Fore.RESET

    @classmethod
    def white(cls, s):
        return Style.BRIGHT + Fore.WHITE + s + Fore.RESET

    @classmethod
    def black(cls, s):
        return Style.BRIGHT + Fore.BLACK + s + Fore.RESET

    @classmethod
    def white_green(cls, s):
        return Style.BRIGHT + Fore.WHITE + Back.GREEN + s + Fore.RESET + Back.RESET

