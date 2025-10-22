#!/usr/bin/env python3
# envcrypt.py - encrypt/decrypt .env using password (click + cryptography)

import os
import sys
import base64
import click
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KDF_ITERS = 390000
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_LEN = 32

def derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LEN,
        salt=salt,
        iterations=KDF_ITERS,
    )
    return kdf.derive(password)

def write_atomic(path: str, data: bytes):
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, path)
    os.chmod(path, 0o600)

@click.group()
def cli():
    pass

@cli.command()
@click.option("--infile", "-i", default=".env", show_default=True)
@click.option("--outfile", "-o", default=".env.enc", show_default=True)
@click.option("--remove/--no-remove", default=False, help="Remove source after success")
def encrypt(infile, outfile, remove):
    "Encrypt infile -> outfile (password prompted)"
    if not os.path.exists(infile):
        click.echo("input file not found", err=True)
        sys.exit(1)
    pwd = click.prompt("Password", hide_input=True, confirmation_prompt=True).encode()
    with open(infile, "rb") as f:
        plaintext = f.read()
    salt = os.urandom(SALT_SIZE)
    key = derive_key(pwd, salt)
    aes = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)
    ct = aes.encrypt(nonce, plaintext, None)
    payload = base64.b64encode(salt + nonce + ct)
    write_atomic(outfile, payload)
    if remove:
        os.remove(infile)
    click.echo(f"Encrypted -> {outfile}")

@cli.command()
@click.option("--infile", "-i", default=".env.enc", show_default=True)
@click.option("--outfile", "-o", default=".env", show_default=True)
@click.option("--remove/--no-remove", default=False, help="Remove source after success")
def decrypt(infile, outfile, remove):
    "Decrypt infile -> outfile (password prompted)"
    if not os.path.exists(infile):
        click.echo("input file not found", err=True)
        sys.exit(1)
    pwd = click.prompt("Password", hide_input=True).encode()
    raw = base64.b64decode(open(infile, "rb").read())
    if len(raw) < (SALT_SIZE + NONCE_SIZE + 16):
        click.echo("input file looks invalid", err=True)
        sys.exit(1)
    salt = raw[:SALT_SIZE]
    nonce = raw[SALT_SIZE:SALT_SIZE+NONCE_SIZE]
    ct = raw[SALT_SIZE+NONCE_SIZE:]
    key = derive_key(pwd, salt)
    aes = AESGCM(key)
    try:
        pt = aes.decrypt(nonce, ct, None)
    except Exception:
        click.echo("decryption failed - bad password or corrupted file", err=True)
        sys.exit(1)
    write_atomic(outfile, pt)
    if remove:
        os.remove(infile)
    click.echo(f"Decrypted -> {outfile}")

if __name__ == "__main__":
    cli()
