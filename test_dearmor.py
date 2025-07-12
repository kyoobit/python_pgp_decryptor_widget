import getpass
import os

import pytest

from dearmor import decrypt_pgp_message
from dearmor import decrypt
from dearmor import get_arguments


PASSPHRASE = os.environ.get("PGP_KEY_PASSPHRASE")
if PASSPHRASE is None:
    PASSPHRASE = getpass.getpass(prompt="Enter your PGP key passphrase: ")


'''
@pytest.fixture
def isolated_gpg_home():
    """Create an isolated GPG home directory for each test"""
    with tempfile.TemporaryDirectory() as tmpdir:
        gpg_home = os.path.join(tmpdir, ".gnupg")
        os.makedirs(gpg_home)
        os.environ["GNUPGHOME"] = gpg_home
        yield gpg_home
'''


def test_decrypt_pgp_message():
    pgp_message = """-----BEGIN PGP MESSAGE-----

hF4D6u0zIETweqYSAQdAEsKbA+wj+syBmbf1lULGScX6/8PjhP+O/C6YSV1DXDQw
jvqXTRGq+tJdT0SAz9kFeMgLiIXR3juVQmUNzIBkxwidk00dQouIe6Tnx0TEjmuP
1GcBCQIQyvPXHXY0JaL7x79pIvoY86O1buhb940d4t25pUr5WKT/U0wnOECKcAmJ
/5CTvum/AWpR+yCXHo6SyWQ67xccFkfVU45VquC+FwzyWpGK1xyR/gs5hNzH+vk/
zzI99qsNG7HJ
=pnBz
-----END PGP MESSAGE-----
    """
    message = decrypt_pgp_message(pgp_message, PASSPHRASE)
    assert message.startswith("key: multi line test")


@pytest.mark.skip(reason="GPG session reuse causes this to fail")
def test_decrypt_pgp_message_failure():
    pgp_message = """-----BEGIN PGP MESSAGE-----

hF4D6u0zIETweqYSAQdAEsKbA+wj+syBmbf1lULGScX6/8PjhP+O/C6YSV1DXDQw
jvqXTRGq+tJdT0SAz9kFeMgLiIXR3juVQmUNzIBkxwidk00dQouIe6Tnx0TEjmuP
1GcBCQIQyvPXHXY0JaL7x79pIvoY86O1buhb940d4t25pUr5WKT/U0wnOECKcAmJ
/5CTvum/AWpR+yCXHo6SyWQ67xccFkfVU45VquC+FwzyWpGK1xyR/gs5hNzH+vk/
zzI99qsNG7HJ
=pnBz
-----END PGP MESSAGE-----
    """
    with pytest.raises(ValueError):
        decrypt_pgp_message(pgp_message, "WHOOPS!")


def test_decrypt():
    encrypted_yaml = """---
# secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: secrets-test
  namespace: test
type: Opaque
stringData:
  # gpg --encrypt --armor --recipient foo@bar.net <<EOF
  # key: multi line test
  #   test:
  #     - test
  #     - test
  #     - test
  # EOF
  # gpg --decrypt
  -----BEGIN PGP MESSAGE-----
  
  hF4D6u0zIETweqYSAQdAEsKbA+wj+syBmbf1lULGScX6/8PjhP+O/C6YSV1DXDQw
  jvqXTRGq+tJdT0SAz9kFeMgLiIXR3juVQmUNzIBkxwidk00dQouIe6Tnx0TEjmuP
  1GcBCQIQyvPXHXY0JaL7x79pIvoY86O1buhb940d4t25pUr5WKT/U0wnOECKcAmJ
  /5CTvum/AWpR+yCXHo6SyWQ67xccFkfVU45VquC+FwzyWpGK1xyR/gs5hNzH+vk/
  zzI99qsNG7HJ
  =pnBz
  -----END PGP MESSAGE-----
    """
    decrypted_yaml = decrypt(encrypted_yaml, PASSPHRASE)
    print(decrypted_yaml)
    assert decrypted_yaml.find("  key: multi line test") != -1


TEST_ARGUMENTS = [
    ("input_text", "--input", "/some/file/path.ext", "/some/file/path.ext"),
    ("input_text", "-i", "/some/file/path.ext", "/some/file/path.ext"),
    ("output_text", "--output", "/some/file/path.ext", "/some/file/path.ext"),
    ("output_text", "-o", "/some/file/path.ext", "/some/file/path.ext"),
    ("passphrase", "--passphrase", "<PASSPHRASE>", "<PASSPHRASE>"),
    ("passphrase", "-P", "<PASSPHRASE>", "<PASSPHRASE>"),
]


@pytest.mark.parametrize(
    "key, flag, value, expected",
    TEST_ARGUMENTS,
    ids=[test[1] for test in TEST_ARGUMENTS],
)
def test_get_arguments(key, flag, value, expected):
    args, unknown_args = get_arguments([flag, value])
    assert getattr(args, key) == expected


'''
def test_main(capsys):
    args = get_arguments(args=["--foo", "--bar"])
    main(args)
    captured = capsys.readouterr()
    assert (
        captured.out
        == """...\n"""
    )
'''
