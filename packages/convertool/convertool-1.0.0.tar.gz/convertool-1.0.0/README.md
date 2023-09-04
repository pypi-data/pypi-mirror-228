# How to Build and Distribute a CLI Tool with Python

## Requirements

1. `virtualenv`: n isolated python env where we can test our tools/scripts etc while not installing them on our system globally.

```bash
pip install virtualenv
```

2. `wheel`: a packaging mechanism for python tools/packages.

```bash
pip install wheel
```

3. `setuptools`: a library that we will use to package our tool.

```bash
pip install --upgrade setuptools
```

4. `twine`: used for distributing the packages to `pypi/test.pypi`.

```bash
pip install twine
```

## Directory Structure & Initial Setup

```angular2html
MyTool
    - app
        - __init__.py
        - __main__.py
        - application.py
    - my_tool.py
    - setup.py
    - requirements.txt
    - README.md
    - LICENSE
    - MANIFEST.in
```

### License

Choose a LICENSE for distributing the package to pick from https://choosealicense.com/.

### Required packages

```bash
pip install -r requirements.txt
```

## `setup.py`

* `py_modules`
  - This is the place where we tell `setuptools` what modules it must be including while packaging the tool.
  - In our case, we are asking it to include `my_tool.py` and the whole app folder.
  - That is where the main functionalities of our tool will lie.

* `packages`
  - This tells the places setuptools should look for in the current directory to find packages required for the tool.
  - `find_packages()` without any arguments means look through the whole directory to find any packages required.

* `entry_points`
  - This is where we tell how our tool can be invoked and what function must be called when it is invoked.
  - [console_scripts] tells the `setuptools` that this tool will be used as a CLI tool (like `pip` or `npm`).

* `cooltool=my_tool:cli`
  - this tells `setuptools` that whenever somebody types `cooltool` in the terminal, call the cli function inside `my_tool.py`.
  - If we have another function called start, and we want that to be invoked, we would write `my_tool:start`.

## Testing the Tool

```bash
# Create a virtual env
virtualenv <virtual-env-name>

# Activate the created virtual env
source venv/bin/activate

# Install the CLI tool
python setup.py develop

# Verify the installation
which cooltool
```

### Tests

```bash
# Tests
% cooltool hello
Hello World

% cooltool hello -n Python
Hello Python
```

## Packaging and Distributing

```bash
python setup.py sdist bdist_wheel
```

Use `twine` to upload the binaries to `test.pypi.org`.

```bash
twine upload --repository testpypi --skip-existing dist/*
```

Now install it using `pip`.

```bash
pip install --index-url https://test.pypi.org/simple/ cooltool
```

## Reference

* [Click documentation](https://click.palletsprojects.com/en/7.x/)