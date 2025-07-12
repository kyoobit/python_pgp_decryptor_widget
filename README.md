# Python Armor/Dearmor Widget

A silly widget to handle encryption/decryption of sensitive values in text files.

# Use the Armor/Dearmor Widget

Install `uv`:
```shell
[ -n "$(uv --version)" ] || curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install the dependencies:
```shell
uv add --upgrade --requirements requirements.txt
```

Alias the program:
```shell
alias dearmor='uv run --project $HOME/repos/python/python_dearmor_widget \
  $HOME/repos/python/python_dearmor_widget/dearmor.py $*';
```

Run the program:
```shell
dearmor --help
```

# Manual Testing

Install `uv`:
```shell
[ -n "$(uv --version)" ] || curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install the dependencies:
```shell
uv add --upgrade --requirements requirements-ci.txt --dev
```

Manual test run:
```shell
export PGP_KEY_PASSPHRASE='<YOUR PGP KEY PASSPHRASE>'
uv run coverage run -m pytest -v test_dearmor.py
uv run coverage report -m
uv run ruff check dearmor.py
```
