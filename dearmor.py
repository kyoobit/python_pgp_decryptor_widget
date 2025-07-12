#!/usr/bin/env python3

import argparse
import getpass
import os
import re

from pathlib import Path

# https://gnupg.readthedocs.io/
import gnupg


DEFAULT = None


def dearmor(**kwargs) -> str:
    """...

    **kwargs

      ... <...>: ...
        Default: ...
    """


def decrypt_pgp_message(pgp_message: str, passphrase: str) -> str:
    """..."""
    gpg = gnupg.GPG()
    message = gpg.decrypt(
        pgp_message,
        passphrase=passphrase,
        always_trust=True,
    )
    if not message.ok:
        raise ValueError(f"{message.status}; {message.stderr}")
    return str(message)


def decrypt(input_text: str, passphrase: str) -> str:
    """..."""
    # Split the single encrypted input message into lines
    input_text = input_text.split("\n")
    # Process the lines looking for PGP messages to decrypt
    output_text = []
    pgp_message = False
    pgp_message_indent = ""
    for input_line in input_text:
        if input_line.strip() == "-----BEGIN PGP MESSAGE-----":
            pgp_message = [input_line.strip()]
            # Set the indent to the indent of the first line of the PGP message
            m = re.search(r"(?P<indent>^\s*)(?P<line>[^\s].+)", input_line)
            pgp_message_indent = m.groupdict().get("indent", "")
        elif input_line.strip() == "-----END PGP MESSAGE-----":
            pgp_message.append(input_line.strip())
            pgp_message = "\n".join(pgp_message)
            # Decrypt the PGP message
            message = decrypt_pgp_message(pgp_message, passphrase)
            # Add the original PGP message indentation to the decrypted message
            for message_line in message.strip().split("\n"):
                output_text.append(pgp_message_indent + message_line)
            # Set "pgp_message" to False for the next PGP message
            pgp_message = False
        elif pgp_message:
            pgp_message.append(input_line.strip())
        else:
            output_text.append(input_line)
    # Combine the lines into a single decrypted output message
    output_text = "\n".join(output_text)
    return output_text


def get_arguments(args: list = None) -> (argparse.Namespace, list):
    """Return parsed cli arguments as (args, unknown_args)"""
    parser = argparse.ArgumentParser(
        description="A silly widget to handle encryption/decryption of sensitive values in text files.",
    )

    # GPG options
    parser.add_argument(
        "--passphrase",
        "-P",
        help="Passphrase used with decryption (default=None)",
    )

    # Input options
    parser.add_argument(
        "--input",
        "-i",
        dest="input_text",
        metavar="<PATH>",
        help="Input file path of text containing encrypted PGP messages to decrypt",
    )

    # Output options
    parser.add_argument(
        "--output",
        "-o",
        dest="output_text",
        metavar="<PATH>",
        help="Output file path to write decrypted text (Default: None)",
    )

    args, unknown_args = parser.parse_known_args(args)
    return args, unknown_args


def main(args: argparse.Namespace):
    input_text = Path(args.input_text).read_text()

    if args.passphrase is None:
        # Check for PGP_KEY_PASSPHRASE in the environment variables
        passphrase = os.environ.get("PGP_KEY_PASSPHRASE")
        # Prompt for a passphrase when one was not provided
        if passphrase is None:
            passphrase = getpass.getpass(prompt="Key passphrase: ")
        args.passphrase = passphrase

    output_text = decrypt(input_text, args.passphrase)
    print(output_text)


if __name__ == "__main__":
    args, unknown_args = get_arguments()
    main(args)
