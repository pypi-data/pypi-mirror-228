![Horizontal Lockupblack](https://user-images.githubusercontent.com/293079/169453889-ae211c6c-7634-4ccd-8ca9-8970c2621b6f.png#gh-light-mode-only)
![Horizontal Lockup copywhite](https://user-images.githubusercontent.com/293079/169453892-895f637b-4633-4a14-b997-960c9e17579b.png#gh-dark-mode-only)

# Anvil Encryption

[![PyPI License](https://img.shields.io/pypi/l/python-anvil-encryption.svg)](https://pypi.org/project/python-anvil-encryption)
[![PyPI Version](https://img.shields.io/pypi/v/python-anvil-encryption.svg)](https://pypi.org/project/python-anvil-encryption)

This library is a small wrapper around the [`pypa/cryptography` library](https://cryptography.io/en/latest/).
It offers convenience methods for encrypting and decrypting arbitrary payloads in both AES and RSA.

For use encrypting / decrypting payloads in Anvil, you can generate an RSA keypair from
your [organization's settings page](https://www.useanvil.com/docs/api/getting-started#encryption).

[Anvil](www.useanvil.com/developers) provides easy APIs for all things paperwork.

1. [PDF filling API](https://www.useanvil.com/products/pdf-filling-api/) - fill out a PDF template with a web request
   and structured JSON data.
2. [PDF generation API](https://www.useanvil.com/products/pdf-generation-api/) - send markdown or HTML and Anvil will
   render it to a PDF.
3. [Etch E-sign with API](https://www.useanvil.com/products/etch/) - customizable, embeddable, e-signature platform with
   an API to control the signing process end-to-end.
4. [Anvil Workflows (w/ API)](https://www.useanvil.com/products/workflows/) - Webforms + PDF + E-sign with a powerful
   no-code builder. Easily collect structured data, generate PDFs, and request signatures.

Learn more about Anvil on our [Anvil developer page](https://www.useanvil.com/developers).

## Setup

### Requirements

* Python 3.7+

### Installation

Install it directly into an activated virtual environment:

```text
$ pip install python-anvil-encryption
```

or add it to your [Poetry](https://poetry.eustace.io/) project:

```text
$ poetry add python-anvil-encryption
```

## Usage

This usage example is also in a runnable form in the `examples/` directory.

```python
import os
from python_anvil_encryption import encryption

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

# Keys could be read from a file (or preferably from environment variables)
public_key = None
private_key = None
with open(os.path.join(CURRENT_PATH, "keys/public.pub"), "rb") as pub_file:
    public_key = pub_file.read()

with open(os.path.join(CURRENT_PATH, "./keys/private.pem"), "rb") as priv_file:
    private_key = priv_file.read()

# RSA
message = b"Super secret message"
encrypted_message = encryption.encrypt_rsa(public_key, message)
decrypted_message = encryption.decrypt_rsa(private_key, encrypted_message)
assert decrypted_message == message
print(f"Are equal? {decrypted_message == message}")

# AES
aes_key = encryption.generate_aes_key()
aes_encrypted_message = encryption.encrypt_aes(aes_key, message)
# The aes key in the first parameter is required to be in a hex
# byte string format.
decrypted_message = encryption.decrypt_aes(
    aes_key.hex().encode(),
    aes_encrypted_message
)
assert decrypted_message == message
print(f"Are equal? {decrypted_message == message}")
```
