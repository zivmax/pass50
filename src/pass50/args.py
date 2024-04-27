import argparse
from color import Colored

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
