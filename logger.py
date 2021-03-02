import sys, os, time
from datetime import datetime

class Logger():
    """
    Utility class to log informations to the user
    """
    @staticmethod
    def message(input):
        # Outputs an information
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        msg = "%s [INFO] : " % current_time + input
        sys.stdout.write(msg)

        return msg

    @staticmethod
    def warning(input):
        # Outputs a warning
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        msg = "%s [WARNING] : " % current_time + input
        sys.stdout.write(msg)

        return msg

    @staticmethod
    def error(input):
        # Outputs an error
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        msg = "%s [ERROR] : " % current_time + input
        sys.stdout.write(msg)

        return msg

    @staticmethod
    def console_progress_bar(prefix, suffix, progress, length):
        # Prints a progress bar to the console
        iter = progress * length / 100
        bar = "\r{0}[{1}]{2}".format(prefix, (("#" * iter) + (" " * (length - iter))), suffix)
        sys.stdout.write(bar)

    @staticmethod
    def waiting_wheel():
        # Prints a waiting wheel to the console \-/

        def spinning_cursor():
            while True:
                for cursor in "\\|/-":
                    yield cursor

        spinner = spinning_cursor()

        for i in range(0, 4):
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            time.sleep(0.3)
            sys.stdout.write("\b")

    @staticmethod
    def waiting_message(input):
        # Prints message with a spinning wheel
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        def spinning_cursor():
            while True:
                for cursor in "\\|/-":
                    yield cursor

        spinner = spinning_cursor()

        for i in range(0, 4):
            sys.stdout.write("%s [INFO] : " % current_time + input + " " + next(spinner))
            sys.stdout.flush()
            time.sleep(0.3)
            sys.stdout.write("\r")
