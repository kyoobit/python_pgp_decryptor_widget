# Python PGP Decryptor Widget

A silly widget to handle encryption/decryption of sensitive values in text files.

# Use the Decryptor Widget

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
alias pgp_decryptor='uv run --project $HOME/repos/python/python_pgp_decryptor_widget \
  $HOME/repos/python/python_pgp_decryptor_widget/pgp_decryptor.py $*';
```

Run the program:
```shell
pgp_decryptor --help
```

Example usage:
```shell
% sdiff secrets.yaml <(PGP_KEY_PASSPHRASE='<PASSPHRASE>' pgp_decryptor -i secrets.yaml)
---                                                             ---
# secrets.yaml                                                  # secrets.yaml
apiVersion: v1                                                  apiVersion: v1
kind: Secret                                                    kind: Secret
metadata:                                                       metadata:
  name: secrets-test                                              name: secrets-test
  namespace: test                                                 namespace: test
type: Opaque                                                    type: Opaque
stringData:                                                     stringData:
  # gpg --encrypt --armor --recipient foo@bar.net <<EOF           # gpg --encrypt --armor --recipient foo@bar.net <<EOF
  # key: <PLACEHOLDER>                                            # key: <PLACEHOLDER>
  # EOF                                                           # EOF
  # gpg --decrypt                                                 # gpg --decrypt
  -----BEGIN PGP MESSAGE-----                                 |   key: test
                                                              | 
  HF4D6u0zIETweqYSAQdAMe+o82H/CW3AZklCR3phwgMm1EGqVt3xV20xyc1 <
  hKYV3NocIe6BoLjxkyiSD5oGwooSBdb0c3eTI/BaNlvbRVK7eY7OUGFFIoi <
  1E8BCQIQ6+O6kPmtMvvv8//IByX6WM5s4ycK4iGh+Po7+v9Vte4ReCMhBz/ <
  sIuMiPlUWwAZx0FTg6dm6Nnq3AU8+Rt8aSuxrlAWdr/0                <
  =oC07                                                       <
  -----END PGP MESSAGE-----                                   <
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
uv run coverage run -m pytest -v test_pgp_decryptor.py
uv run coverage report -m
uv run ruff check pgp_decryptor.py
```
