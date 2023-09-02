"""Tests for encryption module."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned
import json

import pytest

from python_anvil_encryption import encryption


def describe_encryption():
    def describe_generate_aes_key():
        aes_key = encryption.generate_aes_key()
        assert aes_key

    def describe_decrypt_rsa():
        def test_decrypt_real_test_data_bytes(forge_complete_payload, private_key):
            data = forge_complete_payload.get("data")

            # Convert data into `bytes` since the fixture parses the file's
            # JSON, converting everything into a `str`.
            res = encryption.decrypt_rsa(private_key, bytes(data, "utf-8"))
            res_json = json.loads(res)
            assert res_json.get("weld").get("eid")
            assert res_json.get("forge").get("eid")

        def test_decrypt_real_test_data_str(forge_complete_payload, private_key):
            """Test decrypting when `data` is a `str`."""
            data = forge_complete_payload.get("data")
            res = encryption.decrypt_rsa(private_key, data)
            res_json = json.loads(res)
            assert res_json.get("weld").get("eid")
            assert res_json.get("forge").get("eid")

        def test_decrypt_real_test_data_all_str(forge_complete_payload, private_key):
            """Test decrypting when `data` and `private_key` is a `str`."""
            data = forge_complete_payload.get("data")

            # Convert data into `bytes` since the fixture parses the file's
            # JSON, converting everything into a `str`.
            res = encryption.decrypt_rsa(private_key.decode(), data)
            res_json = json.loads(res)
            assert res_json.get("weld").get("eid")
            assert res_json.get("forge").get("eid")

    def describe_encrypt_rsa():
        def test_encrypt_bytes_padded(public_key):
            # This message should get padded
            message = b"some message"
            res = encryption.encrypt_rsa(public_key, message, auto_padding=True)
            splits = res.split(b":")
            assert len(splits) == 3
            for item in splits:
                # Simple check to see if each item at least has something
                assert bool(item) is True

        def test_encrypt_bytes_not_padded_fail(public_key):
            # This message will not get padded, so it will throw an error since
            # the length isn't a multiple of the block length.
            message = b"some message"

            def func():
                encryption.encrypt_rsa(public_key, message, auto_padding=False)

            with pytest.raises(ValueError):
                func()

        def test_encrypt_bytes_not_padded_ok(public_key):
            # This message will not get padded, but meets the length requirement.
            message = b"some message1111"
            res = encryption.encrypt_rsa(public_key, message, auto_padding=False)
            splits = res.split(b":")
            assert len(splits) == 3

    def describe_encrypt_aes():
        message = b"Secret message"
        aes_key = encryption.generate_aes_key()
        aes_encrypted_message = encryption.encrypt_aes(aes_key, message)
        # The aes key in the first parameter is required to be in a hex
        # byte string format.
        decrypted_message = encryption.decrypt_aes(
            aes_key.hex().encode(), aes_encrypted_message
        )
        assert decrypted_message == message
