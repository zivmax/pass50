from subprocess import PIPE, Popen, TimeoutExpired
from cmd50 import cmd50
import time
from time import sleep

import cowsay

from color import Colored
from args import args

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
