from click import clear as click_clear


class Text:
    END = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'

    @classmethod
    def black(cls, string):
        return f"{cls.BLACK}{string}{cls.END}"

    @classmethod
    def yellow(cls, string):
        return f"{cls.YELLOW}{string}{cls.END}"

    @classmethod
    def blue(cls, string):
        return f"{cls.BLUE}{string}{cls.END}"

    @classmethod
    def magenta(cls, string):
        return f"{cls.MAGENTA}{string}{cls.END}"

    @classmethod
    def cyan(cls, string):
        return f"{cls.CYAN}{string}{cls.END}"

    @classmethod
    def white(cls, string):
        return f"{cls.WHITE}{string}{cls.END}"

    @classmethod
    def success(cls, string):
        return f"{cls.SUCCESS}{string}{cls.END}"

    @classmethod
    def warning(cls, string):
        return f"{cls.WARNING}{string}{cls.END}"

    @classmethod
    def fail(cls, string):
        return f"{cls.FAIL}{string}{cls.END}"

    @classmethod
    def bold(cls, string):
        return f"{cls.BOLD}{string}{cls.END}"

    @classmethod
    def dim(cls, string):
        return f"{cls.DIM}{string}{cls.END}"

    @classmethod
    def underline(cls, string):
        return f"{cls.UNDERLINE}{string}{cls.END}"

    @classmethod
    def green(cls, string):
        return f"{cls.GREEN}{string}{cls.END}"

    @classmethod
    def red(cls, string):
        return f"{cls.RED}{string}{cls.END}"

    @staticmethod
    def getpass(*args, char="*", end="", sep=" ", input_zone=False):
        msg = sep.join([str(arg) for arg in args])
        o_char = char
        valids = "q w e r t y u i o p a s d f g h j k l z x c v b n m Q W E R T Y U I O P A S D F G H J K L Z X C V B N M 1 2 3 4 5 6 7 8 9 0 - = [] ; ' # \\ , . / ! \" £ $ % ^ & * ( ) _ + { } : @ ~ < > ? | ` ¬".split(
            " ")
        passw = []
        chars = []
        print(msg, "\n\nInput:\t" if input_zone else "", end=end, flush=True)
        while True:
            ch = getkey()
            if o_char is None:
                char = ch
            if ch == keys.ENTER:
                break
            elif ch == keys.BACKSPACE:
                try:
                    del passw[-1]
                    del chars[-1]
                except IndexError:
                    continue
            elif ch == keys.SPACE:
                ch = " "
                chars.append(char)
                passw.append(ch)
            elif ch not in valids:
                continue
            else:
                chars.append(char)
                passw.append(ch)
            Cursor.clear_line()
            print("\r", end="")
            print("Input:\t" if input_zone else msg, "".join(chars), end="", flush=True)
        print()
        return "".join(passw)

    @staticmethod
    def heading(msg):
        exceptions = ["the", "a", "an"]
        msg = msg.split(" ")
        for idx, word in enumerate(msg):
            if word.lower() in exceptions and idx != 0 and idx != len(msg) - 1:
                msg[idx] = word.lower()
                continue
            msg[idx] = word[0].upper() + word[1:].lower()
        return " ".join(msg)

    @staticmethod
    def help():
        example = '''from KLib.formatting import Text

print(f"This text is default, {Text.red('but this text is red.')}")'''

        methods = '''Styles [ <style>(<text>) ]:

Black
Yellow
Blue
Magenta
Cyan
White
Red
Green
Success Text
Warning Text
Failure Text
Bold
Dim
Underline
Heading


Other Methods:

Text.getpass(<message (*args)>, char=<cover_string>, end=<end_string>, sep=<arg separation string>, input_zone=bool)'''

        return f"Using styles:\n\nTo change a text style to a red colour, follow the below syntax:\n\n{example}\n\nMethods:\n\n{methods}\n\n\nEnjoy :)"


class Cursor:

    @staticmethod
    def up(n=1):
        print(f"\033[{n}A", end="", flush=True)

    @staticmethod
    def down(n=1):
        print(f"\033[{n}B", end="", flush=True)

    @staticmethod
    def forward(n=1):
        print(f"\033[{n}C", end="", flush=True)

    @staticmethod
    def back(n=1):
        print(f"\033[{n}D", end="", flush=True)

    @staticmethod
    def clear_terminal():
        print("\033[1J", end="", flush=True)

    @staticmethod
    def clear_line():
        print("\033[1K", end="", flush=True)

    @staticmethod
    def help():
        example = '''from KLib.formatting import Cursor

Cursor.forward(5)'''

        methods = '''Movement [ <direction>(<magnitude>) ]:

Up
Down
Forward
Back


Other Methods:

Cursor.clear_terminal()
Cursor.clear_line()'''

        return f"Using cursor movement:\n\nTo to move the cursor position up by 5 spaces, follow the below syntax:\n\n{example}\n\nMethods:\n\n{methods}\n\n\nEnjoy :)"


class Terminal:

    def click_clear(method):
        def __impl(*args, **kwargs):
            click_clear()
            method(*args, **kwargs)

        return __impl
