# pass50

`pass50` is a convenient command-line tool designed to streamline the process of checking and submitting code assignments for Harvard's CS50 courses. It automates interactions with CS50's `check50` and `submit50` tools, making it easier to manage coursework directly from the terminal.

## Features

- **Auto-check**: Automatically run `check50` on specified assignments.
- **Auto-submit**: Automatically run `submit50` for submissions.
- **Custom Path**: Specify a relative or absolute path to the directory containing your project.
- **Identifier Selection**: Choose whether to identify assignments by directory or file names.
- **Course Selection**: Specify which CS50 course you are submitting for (e.g., `x` for CS50x).
- **Logging**: Option to print detailed logs for debugging and verification purposes.
- **Environment Initialization**: Prepare your environment for using `pass50`.

## Installation

To install `pass50`, you can directly use the provided script:

You can download the installation script:

```bash
wget https://raw.githubusercontent.com/zivmax/pass50/main/update.sh
```
, then run it to install:
```bash
bash update.sh
```

`update.sh` is also the script to update the `pass50` to the latest version.

## Usage

```plaintext
usage: pass50 [-h] [-c] [-s] [-p PATH] [-i {d,f}] [-C {x,p}] [-l] [-upl] [-d] [-I]

options:
  -h, --help            show this help message and exit
  -c, --check           Only auto check50.
  -s, --submit          Only auto submit50.
  -p PATH, --path PATH  the path (Rel or Abs) of the dir you want to work with.
  -i {d,f}, --identifier {d,f}
                        choose the identifier (dir's name or files' name) to generate slug.
  -C {x,p}, --course {x,p}
                        choose the course from cs50 you're taking.
  -l, --logs            print the logs of check50 & submit50.
  -upl, --unpassedLogs  print all logs of unpassed works at the bottom.
  -d, --dev             run in developing mode, printing all logs.
  -I, --init            Init the env for the app.
```

## Example Commands

- **Initialize the environment**:
  ```bash
  pass50 --init
  ```
- **Check and Submit the current work directory**:
  ```bash
  pass50 --course x
  ```
- **Only Submit assignment in the `pset1/`**:
  ```bash
  pass50 --submit --path ./pset1/ --identifier f --course x
  ```

## Contributing

Contributions to `pass50` are welcome! Please feel free to fork the repository, make changes, and submit pull requests. You can also open issues if you encounter bugs or have suggestions for improvements.

## License

`pass50` is released under the MIT License. See the LICENSE file in the repository for more details.

## Contact

For more information, please visit the [GitHub repository](https://github.com/zivmax/pass50) or contact the maintainers directly through GitHub issues.
