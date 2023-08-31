class ColorPrint:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

    @staticmethod
    def red(*args):
        print(ColorPrint.RED + ' '.join(map(str, args)) + ColorPrint.RESET)

    @staticmethod
    def green(*args):
        print(ColorPrint.GREEN + ' '.join(map(str, args)) + ColorPrint.RESET)

    @staticmethod
    def yellow(*args):
        print(ColorPrint.YELLOW + ' '.join(map(str, args)) + ColorPrint.RESET)

    @staticmethod
    def blue(*args):
        print(ColorPrint.BLUE + ' '.join(map(str, args)) + ColorPrint.RESET)

    @staticmethod
    def magenta(*args):
        print(ColorPrint.MAGENTA + ' '.join(map(str, args)) + ColorPrint.RESET)

    @staticmethod
    def cyan(*args):
        print(ColorPrint.CYAN + ' '.join(map(str, args)) + ColorPrint.RESET)
