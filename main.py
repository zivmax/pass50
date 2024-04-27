#!/usr/bin/python

import argparse
import os
import re
import sys
import threading
import time
from subprocess import PIPE, Popen, TimeoutExpired
from time import sleep
import datetime

try:
    from colorama import Back, Fore, Style, init
except ImportError:
    exit("\nThe env hasn't be prepared, run with `-I` argument to init the env.\n")

init(autoreset=True)


def main():

    validate_path_and_chdir(args.path)

    if args.course == "":
        course = input("Course? [x/p]: ")
        print('\n')
    else:
        course = args.course

    date = datetime.date.today()
    year = ""
    match course:
        case "x":
            year = str(date.year)
        case "p":
            year = "2022"

    language = ""

    if args.identifier == "f":
        language = input("Language? [c/py]: ")

    if args.check:
        auto_check_only(course, year, language, args.path)

    elif args.submit:
        auto_submit_only(course, year, language, args.path)

    else:
        check_submit_all(course, year, language, args.path)


def validate_path_and_chdir(path):
    if re.fullmatch(r"(?:\.{1,2}|[A-Za-z0-9_\-]+)?(?:/([A-Za-z0-9_\-]+))*/?", path):
        try:
            os.chdir(path)
        except FileNotFoundError:
            sys.exit(Colored.yellow("\nThe directory does not exist.\n"))
    else:
        sys.exit(Colored.yellow("\nInvalid path\n"))


def auto_check_only(course: str, year: str, language=None, path: str | None = None):
    match args.identifier:
        case "d":
            n_getter = nameGetter("dir", language=language, path=path)
        case "f":
            n_getter = nameGetter("file", language=language, path=path)

    names = n_getter.results

    print("\n")
    sleep(0.7)

    checker = runner50("check50", course, year)
    checker.run(names)
    Passed_files = checker.dones

    print("\n")
    sleep(0.7)

    if len(Passed_files) == len(names):
        cowsay.cow(
            "Congratulations!" + "\nAll works are checkable and passed," + "\nSEE YOU!"
        )
        print()

    else:
        cowsay.cow(
            (
                "Sorry,"
                + "\nsome works are uncheckable or unpassed."
                + "\nCheck the log for details."
            )
        )
        print()

    print(Colored.green("PASSED Works:"))
    for idx, file in enumerate(Passed_files):
        print(f"{idx + 1}. {file}")
        sleep(0.1)

    print()

    if args.unpassedLogs:
        print_unpassed_logs(checker.unpassedlogs)

    print()
    sleep(2)
    sys.exit()


def auto_submit_only(course: str, year: str, language=None, path: str | None = None):
    match args.identifier:
        case "d":
            n_getter = nameGetter("dir", language=language, path=path)
        case "f":
            n_getter = nameGetter("file", language=language, path=path)

    names = n_getter.results

    print("\n")
    sleep(0.7)

    submitter = runner50("submit50", course, year)
    submitter.run(names)
    Submitted_files = submitter.dones

    print("\n")
    sleep(0.7)

    if len(Submitted_files) == len(names):
        cowsay.cow(
            ("Congratulations!")
            + "\nAll the works are submitable and"
            + "\nhave been submitted."
            + "\nSEE YOU!"
        )
        print()

    else:
        cowsay.cow(
            (
                "Sorry,"
                + "\nsome works failed to be submitted or"
                + "\nare unsubmitable."
                + "\nCheck the log for details."
            )
        )
        print()

    print(Colored.green("SUBMITTED Works:"))
    for idx, file in enumerate(Submitted_files):
        print(f"{idx + 1}. {file}")
        sleep(0.1)

    print()
    sleep(2)
    sys.exit()


def check_submit_all(course: str, year: str, language=None, path: str | None = None):
    match args.identifier:
        case "d":
            n_getter = nameGetter("dir", language=language, path=path)
        case "f":
            n_getter = nameGetter("file", language=language, path=path)

    names = n_getter.results

    print("\n")
    sleep(0.7)

    checker = runner50("check50", course, year)
    checker.run(names)
    Passed_files = checker.dones

    unPassed_or_unChecked_files = [
        name
        for name in names
        if name not in Passed_files and (name + " (lab)") not in Passed_files
    ]

    print(Colored.blue("Checking complete!"))
    print()
    sleep(0.7)

    if len(Passed_files) == 0:
        cowsay.cow(
            (
                "Sorry,"
                + "\nnone of the works passed the check"
                + "\nor is checkable. "
                + "\nSEE YOU!"
            )
        )

        print()

        if args.unpassedLogs:
            print_unpassed_logs(checker.unpassedlogs)

        print()
        sleep(2)
        sys.exit()

    elif len(unPassed_or_unChecked_files) == 0:
        print(Colored.green("NO unpassed or uncheckable works."))

    else:
        print(Colored.yellow("UNPASSED | UNCHECKABLE Works:"))
        for idx, file in enumerate(unPassed_or_unChecked_files):
            print(f"{idx + 1}. {file}")
            sleep(0.1)

    print()

    print("\n")
    sleep(0.7)

    submitter = runner50("submit50", course, year)
    submitter.run(Passed_files)
    Submitted_files = submitter.dones

    print("\n")
    sleep(0.7)

    if len(Submitted_files) == len(Passed_files):
        cowsay.cow(
            "Congratulations!"
            + "\nAll the passed works have been submitted."
            + "\nSEE YOU!"
        )
        print()

    else:
        cowsay.cow(
            (
                "Sorry,"
                + "\nsome passed works failed to be submitted."
                + "\nCheck the log for details."
            )
        )
        print()

    print(Colored.green("SUBMITTED Works:"))
    for idx, file in enumerate(Submitted_files):
        print(f"{idx + 1}. {file}")
        sleep(0.1)

    print()

    if args.unpassedLogs:
        print_unpassed_logs(checker.unpassedlogs)

    print()
    sleep(2)
    sys.exit()


def print_unpassed_logs(unpassedlogs: list):
    if len(unpassedlogs) == 0:
        print(Colored.green("No unpassed works.\n"))

    else:
        print(Colored.yellow("Logs of unpassed works:\n"))
        for idx, file in enumerate(unpassedlogs):
            print(f"{idx + 1}. {file['name']}:")
            print(Colored.magenta("\nSTDOUT:\n") + file["stdout"])


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


parser = argparse.ArgumentParser(
    prog="pass50",
    description=("A convinent tool to check and submit " +
                 'your codes to "CS50".'),
    epilog="This is pass50." + Colored.green(" :)"),
)
parser.add_argument(
    "-c", "--check", default=False, action="store_true", help="Only auto check50."
)
parser.add_argument(
    "-s", "--submit", default=False, action="store_true", help="Only auto submit50."
)
parser.add_argument(
    "-p",
    "--path",
    default="./",
    help="the path(Rel or Abs) of the dir " + "you want to work with.",
)
parser.add_argument(
    "-i",
    "--identifier",
    choices=["d", "f"],
    default="d",
    help="choose the identifier(dir's name or files' name) " +
    "to generate slug.",
)
parser.add_argument(
    "-C",
    "--course",
    choices=["x", "p"],
    default="",
    help="choose the course from cs50 you're taking.",
)
parser.add_argument(
    "-l",
    "--logs",
    default=False,
    action="store_true",
    help="print the logs of check50 & submit50.",
)
parser.add_argument(
    "-upl",
    "--unpassedLogs",
    default=False,
    action="store_true",
    help="print the all logs of unpassed works at the bottom.",
)
parser.add_argument(
    "-d",
    "--dev",
    default=False,
    action="store_true",
    help="run in developping mode, printing all logs.",
)
parser.add_argument(
    "-I",
    "--init",
    default=False,
    action="store_true",
    help="Init the env for the app.",
)


args = parser.parse_args()


class ProgressBar:
    DISABLED = False
    TICKS_PER_SECOND = 2

    def __init__(self, message, sytle):
        self._message = message
        self._progressing = False
        self._thread: threading.Thread | None = None
        self._progressStlye = sytle

    def stop(self):
        if self._progressing:
            self._progressing = False
            if self._thread:
                self._thread.join()

    def __enter__(self):
        def progress_runner():
            print(f"{self._message}", end="", flush=True)
            while True:
                sleep(
                    (1 / ProgressBar.TICKS_PER_SECOND)
                    if ProgressBar.TICKS_PER_SECOND
                    else 0.5
                )
                print(f"{self._progressStlye}", end="", flush=True)
                if not self._progressing:
                    break
            print()

        if not ProgressBar.DISABLED:
            self._progressing = True
            self._thread = threading.Thread(target=progress_runner)
            self._thread.start()
        else:
            print(f"{self._message}...")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


class Preparer:
    def Pre_starting(self, usr: list[str] | None = None, sudo: list[str] | None = None):
        self._installed_modules = []

        with ProgressBar(Colored.blue("Initializing"), Colored.blue(".")) as Pbar:
            if args.dev:
                Pbar.stop()

            if usr:
                for self._module_name in usr:
                    threading.Thread(target=self.prepare()).start()

            if sudo:
                Pbar.stop()
                for self._module_name in sudo:
                    threading.Thread(target=self.prepare(bool(sudo))).start()

        if len(self._installed_modules) == 0:
            print(Colored.yellow("All preRequests were already installed."))
        else:
            print(
                Colored.yellow(
                    f"Installed by pass50: {self._installed_modules}"
                )
            )

        sleep(0.5)
        print(Colored.green("Successfully initialized! :)"))
        print("\n")
        sleep(0.5)

    def prepare(self, sudo: bool = False):
        if args.dev:
            print(Colored.green(f"Prepareing {self._module_name}..."))

        if sudo:
            PreRequests = Popen(
                f"sudo pip install {self._module_name}",
                shell=True,
                stdout=PIPE,
                stdin=PIPE,
                stderr=PIPE,
            )
            try:
                stdout, stderr = PreRequests.communicate(timeout=100)

            except TimeoutExpired:
                exit(Colored.red("TIME OUT!"))
        else:
            PreRequests = Popen(
                f"pip install {self._module_name}",
                shell=True,
                stdout=PIPE,
                stdin=PIPE,
                stderr=PIPE,
            )
            try:
                stdout, stderr = PreRequests.communicate(timeout=100)
            except TimeoutExpired:
                exit(Colored.red("TIME OUT!"))

        stdout, stderr = stdout.decode("utf-8"), stderr.decode("utf-8")

        if args.dev:
            print(
                stdout + stderr +
                Colored.blue(f"ExitCode: {PreRequests.returncode}\n")
            )

        if PreRequests.returncode != 0:
            # Print the error message from pip.
            print(Colored.red("\nPip complains:"))
            print(stderr)

            sys.exit("\n" + Colored.red("Initialization failed! :("))

        pre_installed = True

        if re.search(rf"Successfully installed .* ?{self._module_name} ?.*", stdout):
            pre_installed = False
            ...
        if not pre_installed:
            self._installed_modules.append(self._module_name)
            sleep(2)
            print()


class nameGetter:
    def __init__(
        self, identifier: str = "file", language: str | None = None, path: str | None = "./"
    ) -> None:
        self._identifier = identifier
        self._path = path

        if identifier == "file":
            if language is None:
                exit(Colored.yellow("please specify the file's suffix."))
            else:
                self._suffix = '.' + language.lower()

        match self._identifier:
            case "dir":
                self._results = self._get_the_dir_name()

            case "file":
                self._results = self._get_all_file_names()

    @property
    def results(self):
        return self._results

    def _get_the_dir_name(self) -> list[str]:
        try:
            cwd = os.getcwd()
        except:
            print(Colored.yellow("Can not get the directory's name.\n"))
            sys.exit()
        else:
            if match := re.fullmatch(
                r"(?:\.{1,2}|[A-Za-z0-9_\-]+)?(?:/([A-Za-z0-9_\-]+))*/?", cwd
            ):
                path_name = [match.group(1)]
                cowsay.cow(("The directory's name have been got!"))
                print(Colored.green(f"The directory's name: "), end="")
                print(Colored.blue(path_name[0]))
                return path_name
            else:
                print(Colored.yellow("Can not get the directory's name.\n"))
                sys.exit()

    def _get_all_file_names(self) -> list[str]:
        all_names = os.listdir(os.getcwd())

        if "pass50.py" in all_names:
            all_names.remove("pass50.py")

        names = list(
            filter(lambda name: name.endswith(self._suffix), all_names))

        for idx, name in enumerate(names):
            names[idx] = name.removesuffix(self._suffix)

        names = sorted(names)

        if len(names) == 0:
            print(
                Colored.yellow(
                    "No '" + self._suffix + "' files exist in the directory."
                )
            )
            sys.exit("")
        else:
            cowsay.cow(("All files'name have been got!"))
            print()
            print(Colored.green("All the '" + self._suffix + "' files:"))
            for idx, name in enumerate(names):
                print(f"{idx + 1}. {name + self._suffix}")
                sleep(0.1)
            return names


class cmd50:
    _DONE = "\033[1;32m" + "Done" + "\033[0m"
    _INVALID_SLUG = "\033[1;33m" + "Invalid slug" + "\033[0m"
    _UNPASSED = "\033[1;33m" + "Unpassed" + "\033[0m"
    _TIME_OUT = "\033[1;31m" + "Timeout" + "\033[0m"
    _ERROR = "\033[1;31m" + "NetError" + "\033[0m"
    _MISSING = "\033[1;31m" + "Missing" + "\033[0m"
    _UNAUTHEN = "\033[1;33m" + "UnAuthen" + "\033[0m"

    def __init__(
        self, commandtype: str, name: str, course: str, year: str, language: str | None = None
    ):
        self._lab = False
        self._command_type = commandtype
        self._name = name
        self._course = course
        self._year = year
        self._language = language
        self._unpassed_logs: list[dict] = []
        self._status = None
        self._stdout = None
        self._stderr = None
        self._exitcode = int()
        self.generate_slug()

    def run(self):
        if self._command_type == "style50":
            self.styling()

        if args.dev:
            print(Colored.magenta("\nCommand:"),
                  self._command_type, self._slug)

        program = Popen(
            [self._command_type, self._slug],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            shell=False,
        )
        try:
            match self._command_type:
                case "submit50":
                    stdout, stderr = program.communicate(
                        b"yes", timeout=100
                    )
                case "check50":
                    stdout, stderr = program.communicate(
                        timeout=100)

        except TimeoutExpired:
            status = self._TIME_OUT
            self._status = status

        else:
            self._exitcode = program.returncode
            self._stdout = stdout.decode("utf-8")
            self._stderr = stderr.decode("utf-8")

        match self._command_type:
            case "submit50":
                self.handle_submit_out()
            case "check50":
                self.handle_check_out()

    def handle_check_out(self):
        if self._stdout == None:
            status = self._ERROR
        elif self._exitcode == 0 and ":( " not in str(self._stdout):
            status = self._DONE
        elif "Invalid slug" in str(self._stderr):
            status = self._INVALID_SLUG
        elif "You seem to be missing these required files" in str(self._stderr):
            status = self._MISSING
        elif ":( " in str(self._stdout):
            status = self._UNPASSED
        elif "SSH" in str(self._stdout):
            status = self._UNAUTHEN
        else:
            status = self._ERROR

        if status == self._UNPASSED and not args.logs:
            self._unpassed_logs.append(
                {"name": self._name, "stdout": self._stdout})

        self._status = status

    def handle_submit_out(self):
        if self._exitcode == 0:
            status = self._DONE
        elif "Invalid slug" in str(self._stdout):
            status = self._INVALID_SLUG
        elif "You seem to be missing these required files" in str(self._stdout):
            status = self._MISSING
        elif "SSH" in str(self._stdout):
            status = self._UNAUTHEN
        else:
            status = self._ERROR

        self._status = status

    def styling(self):
        ...

    def generate_slug(self):
        match self._course:
            case "p":
                course = "python"
                pure_name = (
                    self._name.removeprefix("test_")
                    .removesuffix(" (lab)")
                )
                if not self._name.startswith("test_"):
                    self._slug = (
                        "cs50/"
                        + "problems/"
                        + self._year
                        + "/"
                        + course
                        + "/"
                        + pure_name
                    )
                else:
                    self._slug = (
                        "cs50/"
                        + "problems/"
                        + self._year
                        + "/"
                        + course
                        + "/"
                        + "tests/"
                        + pure_name
                    )

            case "x":
                course = "x"
                pure_name = (
                    self._name.replace("-", "")
                    .removeprefix("sentimental")
                    .removesuffix("more")
                    .removesuffix("less")
                    .removesuffix(" (lab)")
                )

                if not self._lab:
                    self._slug = (
                        "cs50/"
                        + "problems/"
                        + self._year
                        + "/"
                        + course
                        + "/"
                    )

                    if self._name.startswith("sentimental"):
                        self._slug = self._slug + "sentimental/"

                    self._slug = self._slug + pure_name

                    if self._name.endswith("more"):
                        self._slug = self._slug + "/more"

                else:
                    self._slug = (
                        "cs50/"
                        + "labs/"
                        + self._year
                        + "/"
                        + course
                        + "/"
                        + pure_name
                    )


    def regenerate_slug(self):
        self.generate_slug()


class runner50:
    _DONE = "\033[1;32m" + "Done" + "\033[0m"
    _INVALID_SLUG = "\033[1;33m" + "Invalid slug" + "\033[0m"
    _UNPASSED = "\033[1;33m" + "Unpassed" + "\033[0m"
    _TIME_OUT = "\033[1;31m" + "Timeout" + "\033[0m"
    _ERROR = "\033[1;31m" + "NetError" + "\033[0m"
    _MISSING = "\033[1;31m" + "Missing" + "\033[0m"
    _UNAUTHEN = "\033[1;33m" + "UnAuthen" + "\033[0m"

    def __init__(
        self, commandtype: str, course: str, year: str, retry_time=10, retry_wait=5
    ) -> None:
        self._command_type = commandtype
        self._retry_time = retry_time
        self._retry_wait = retry_wait
        self._course = course
        self._year = year
        self._cmds: list[cmd50] = []
        self._dones: list[str] = []

    @property
    def dones(self) -> list[str]:
        return self._dones

    @property
    def unpassedlogs(self) -> list[list[dict]]:
        return self._unpassedlogs

    def run(self, names: list[str]):
        match self._command_type:
            case "submit50":
                cowsay.cow(("Submitting now... "))
                print()
            case "check50":
                cowsay.cow(("Checking now... "))
                print()

        for name in names:
            cmd = cmd50(self._command_type, name, self._course, self._year)
            self._cmds.append(cmd)

        self._run_the_cmds()

        for idx in range(len(self._cmds)):
            if self._cmds[idx]._lab == True:
                self._cmds[idx].regenerate_slug()

        self._run_the_cmds(lab=True)

    def _run_the_cmds(self, lab=False):
        for idx in range(len(self._cmds)):
            if (lab ^ self._cmds[idx]._lab):  # if they are not same.
                continue

            if (self._cmds[idx]._name.endswith(" (lab)") and lab == False):
                self._cmds[idx]._lab = True
                continue

            for i in range(self._retry_time + 1):
                if i > 0:
                    print(Colored.yellow(
                        f"[{i}]Retrying {self._cmds[idx]._name}..."))
                    sleep(self._retry_wait)

                print(Colored.white(self._cmds[idx]._name + ": "), end="")
                self._cmds[idx].run()
                print(self._cmds[idx]._status)

                if args.logs or args.dev:
                    print(Colored.magenta("\nSTDOUT:\n") +
                          self._cmds[idx]._stdout)
                    print(Colored.magenta("STDERR:\n") +
                          self._cmds[idx]._stderr)

                if self._cmds[idx]._status == self._UNPASSED:
                    print(
                        Colored.magenta("\nUnpassed log:\n") +
                        self._cmds[idx]._stdout
                    )

                elif self._cmds[idx]._status == self._UNAUTHEN:
                    print(":( Ops! you haven't authenticated with your GitHub by ssh yet.")
                    print("You can follow the doc \"https://cs50.readthedocs.io/github/#ssh\" to authenticate.")
                    print(time.ctime())
                    sleep(0.5)
                    print("\n")
                    exit()

                print(time.ctime())
                sleep(0.5)
                print("\n")

                if (
                    self._cmds[idx]._status == self._DONE
                    or self._cmds[idx]._status == self._INVALID_SLUG
                    or self._cmds[idx]._status == self._MISSING
                    or self._cmds[idx]._status == self._UNPASSED
                ):
                    break

            if (
                self._cmds[idx]._status == self._INVALID_SLUG
                and self._cmds[idx]._lab == False
            ):
                self._cmds[idx]._lab = True
                self._cmds[idx]._name = self._cmds[idx]._name + " (lab)"

        self._dones = [
            cmd._name for cmd in self._cmds if cmd._status == self._DONE]
        self._unpassedlogs = [
            cmd._unpassed_logs for cmd in self._cmds if cmd._status == self._UNPASSED
        ]


if __name__ == "__main__":
    try:
        if args.init:
            preparer = Preparer()
            preparer.Pre_starting(usr=["cowsay", "check50", "submit50", "colorama"])

        else:
            try:
                import cowsay
                import check50
                import submit50
                import colorama

            except ImportError:
                exit("\nThe env hasn't be prepared, run with `-I` argument to init the env.\n")

            else:
                sleep(0.7)
                main()

    except KeyboardInterrupt:
        exit("\nManually stopped.")
