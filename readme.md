<h1 align="center">VALORANT Discord Rich Presence Client</h1>
<p align="center"><sup>Isn't the official VALORANT Discord RPC client a bit too lame?</sup></p>

This project is heavily motivated by <a href="https://github.com/colinhartigan/valorant-rpc">colinhartigan/valorant-rpc</a>, mostly because:
- The code is quite messy and is, incredibly inefficient with its resources.
- Isn't really easy to use for some users.

## Installation

This project can be installed on to your device via the source code download mechanism.

- Source Code Download

    ```
    $ git clone https://www.github.com/justfoolingaround/animdl
    ```

    Given that you have [`git`](https://git-scm.com/) installed, you can clone the repository from GitHub. If you do not have or want to deal with installation of [`git`](https://git-scm.com/), you can simply download the repository using [this link.](https://github.com/justfoolingaround/animdl/archive/refs/heads/master.zip)

    After the repository is downloaded and placed in an appropriate directory, you can, either use [`runner.py`](./runner.py) to use the project without installation **or** use [`setup.py`](./setup.py) to proceed with the installation.

    The former can be done via:

    ```py
    $ python runner.py
    ```

    The latter can be done via:

    ```py
    $ pip install .
    ```

    Both commands are to be executed from the directory where the repository is located.

**Additional information:** You **must** have Python installed **and** in PATH to use this project properly. Your Python executable may be `py` **or** `python` **or** `python3`. **Only Python 3.6 and higher versions are supported by the project.**


## Usage

```
Usage: valorantrpc [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version  Show the version and exit.
  --help         Show this message and exit.

Commands:
  run
```


### Running normally

If you have a VALORANT instance running, you can just use the following command.


- ```sh
    $ valorantrpc run
    ```

If you do not have VALORANT instance running, you can simply use the following command to both, start the instance and run the client.


- ```sh
    $ valorantrpc run --run-valorant
    ```

**Note:** If you have VALORANT running and run this too, do not worry, the project will automatically detect it and proceed forward.

## Easy access

You can create a shortcut to your Desktop that will use the set of options passed to the project during the creation of that shortcut easily.

- ```sh
    $ valorantrpc run --run-valorant --shortcut
    ```

## Disclaimer

Haven't really had an account banned from VALORANT just for using the RPC client so you as a user should be fine but I don't take responsibility of any such actions taken on your account.

Please use the project at your own risk.