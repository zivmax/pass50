import os
import re
import sys
from time import sleep
import datetime

import cowsay

from .color import Colored
from .args import args
from .runner50 import runner50


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


if __name__ == "__main__":
    try:
        sleep(0.7)
        main()

    except KeyboardInterrupt:
        exit("\nManually stopped.")
