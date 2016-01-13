from subprocess import call, check_output

__author__ = 'fmca'


class Adb:
    @staticmethod
    def write(text):
        call(["adb", "shell", "input", "text", "'" + text.replace(' ', '%s') + "'"])

    @staticmethod
    def start(activity):
        call(["adb", "shell", "am", "start", activity])

    @staticmethod
    def shell(*args):
        command = ["adb", "shell"]
        command.extend(args)
        return check_output(command).decode("utf-8")


class StrUtils:
    @staticmethod
    def split(string, separator, span):
        words = string.split(separator)
        return [separator.join(words[i:i + span]) for i in range(0, len(words), span)]
