from subprocess import PIPE, Popen, TimeoutExpired

from .color import Colored
from .args import args

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