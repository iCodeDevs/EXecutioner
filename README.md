# EXecutioner

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/1fab847da8434968bb3c7bdaeae8fcb1)](https://www.codacy.com/gh/iCodeDevs/EXecutioner?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=iCodeDevs/EXecutioner&amp;utm_campaign=Badge_Grade)
![Build](https://github.com/iCodeDevs/EXecutioner/actions/workflows/test.yml/badge.svg)
![Build Docs](https://github.com/iCodeDevs/EXecutioner/actions/workflows/doc.yml/badge.svg)

A python library to execute untrusted code and evaluate the output.

## Requirements

- Python Libraries denoted by requirements.txt

- [FireJail](https://firejail.wordpress.com/) (for FireJail Sandbox)

    ```bash
        sudo apt install firejail
    ```

## INSTALLATION FOR DEV

- Clone the repository.
- make a virtual environment named 'venv' inside the repository. (Learn about [venv](https://docs.python.org/3/tutorial/venv.html))

  ```bash
  python -m venv venv
  ```

- access the virtualenv
- install python dev dependencies

  ```bash
  pip install -r requirements.txt
  ```

## Documentation

Documentation can be found at <https://iCodeDevs.github.io/EXecutioner/>
