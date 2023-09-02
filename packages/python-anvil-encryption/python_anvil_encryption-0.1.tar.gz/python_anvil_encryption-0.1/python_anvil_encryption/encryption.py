import base64
import os
from typing import AnyStr

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

IV_LENGTH = 16
AES_KEY_LENGTH = 32
PADDING_SIZE = 128
DEFAULT_ENCODING = "utf-8"


def generate_aes_key():
    return os.urandom(AES_KEY_LENGTH)


def encrypt_rsa(raw_public_key: bytes, message: bytes, auto_padding=True) -> bytes:
    """
    Encrypt with RSA.

    RSA has an upper limit on how much data it can encrypt. So we create an AES
    key, encrypt the AES key with RSA, then encrypt the actual message with AES.

    :param raw_public_key:
    :type raw_public_key:  bytes
    :param message:
    :type message: bytes
    :param auto_padding:
    :type auto_padding: bool
    :return: Returns a `string` like 'abcdef:abcdef:abcdef'
        which is '<rsaEncryptedAESKey:aesIV:aesEncryptedMessage>'
    :rtype: bytes
    """
    public_key = serialization.load_pem_public_key(
        raw_public_key
    )  # type: rsa.RSAPublicKey  # type: ignore
    aes_key = os.urandom(AES_KEY_LENGTH)
    encrypted_aes_key = public_key.encrypt(
        aes_key.hex().encode(),
        padding=padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None,
        ),
    )

    b64_aes_key = base64.b64encode(encrypted_aes_key)
    enc_message = encrypt_aes(aes_key, message, auto_padding)

    return b":".join([b64_aes_key, enc_message])


def decrypt_rsa(_raw_private_key: AnyStr, _message: AnyStr):
    """
    Decrypt with RSA.

    :param raw_private_key:
    :type raw_private_key: AnyStr
    :param message:
    :type message: AnyStr
    :return:
    :rtype:
    """
    if isinstance(_message, str):
        message = bytes(_message, DEFAULT_ENCODING)
    else:
        message = _message

    if isinstance(_raw_private_key, str):
        raw_private_key = bytes(_raw_private_key, DEFAULT_ENCODING)
    else:
        raw_private_key = _raw_private_key

    private_key = serialization.load_pem_private_key(
        raw_private_key, password=None
    )  # type: rsa.RSAPrivateKey  # type: ignore
    index = message.index(b":")
    enc_aes_key = message[:index]
    encrypted_message = message[index + 1 :]

    aes_key = private_key.decrypt(
        base64.b64decode(enc_aes_key),
        padding=padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None,
        ),
    )

    return decrypt_aes(aes_key, encrypted_message)


def encrypt_aes(aes_key: bytes, message: bytes, auto_padding=True) -> bytes:
    """
    Encrypt with AES.

    :param aes_key:
    :type aes_key:
    :param message:
    :type message:
    :param auto_padding: Whether to pad the encrypted message automatically if
        it does not meet the required block size.
        If `auto_padding=False` this may throw an error if the message does
        not meet block size requirements.
    :type auto_padding: bool
    :return:
    :rtype:
    """
    iv = os.urandom(IV_LENGTH)
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))

    if auto_padding:
        padder = sym_padding.PKCS7(PADDING_SIZE).padder()
        message = padder.update(message) + padder.finalize()

    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(message) + encryptor.finalize()

    return b":".join([iv.hex().encode(), encrypted_data.hex().encode()])


def decrypt_aes(aes_key: bytes, encrypted_message: bytes):
    """
    Decrypt with AES.

    :param aes_key:
    :type aes_key:
    :param encrypted_message:
    :type encrypted_message:
    :return:
    :rtype:
    """
    iv, ciphertext = encrypted_message.split(b":")

    _aes_key = bytes.fromhex(aes_key.decode())
    _iv = bytes.fromhex(iv.decode())

    cipher = Cipher(algorithms.AES(_aes_key), modes.CBC(_iv))
    decryptor = cipher.decryptor()
    decrypted_data = (
        decryptor.update(bytes.fromhex(ciphertext.decode())) + decryptor.finalize()
    )

    unpadder = sym_padding.PKCS7(PADDING_SIZE).unpadder()
    return unpadder.update(decrypted_data) + unpadder.finalize()
