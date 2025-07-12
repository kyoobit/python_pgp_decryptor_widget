#!/usr/bin/env python3

## alias password='python3 ${HOME}/repos/python/password/password.py $*';

import getpass

DEFAULT = None

def dearmor(**kwargs) -> str:
    """...

    **kwargs

      ... <...>: ...
        Default: ...
    """

def get_arguments(args=None):
    """Return parsed cli arguments as (args, unknown_args)"""
    parser = ArgumentParser(description="A silly widget to ...")

    ## Input options
    parser.add_argument(
        "msg", nargs="*", help="Message input values to hash (default='')"
    )

    ## Output options

    return parser.parse_known_args(args)

def main(args):
    print(type(args))

    ## Prompt for a passphrase if one was not provided
    #if args.passphrase is None:
    #    args.passphrase = getpass.getpass(prompt='Key passphrase: ')

    """
    check to make sure we have access to the private key
    gpg --import prikey.asc
    gpg --decrypt

    python-gnupg
    https://gnupg.readthedocs.io/

    import gnupg

    gpg = gnupg.GPG()

    with open('encrypted_file.gpg', 'rb') as f:
        decrypted_data = gpg.decrypt_file(f, passphrase='your_passphrase_here', always_trust=True)

        if status.ok:
            print("Decryption successful!")
            print(f"Decrypted content saved to: {status.data.decode('utf-8')}") # If output is not specified, data is returned
        else:
            print("Decryption failed:")
            print(f"Status: {status.status}")
            print(f"Error: {status.stderr}")
    """

if __name__ == "__main__":
    args, unknown_args = get_arguments()
    main(args)
