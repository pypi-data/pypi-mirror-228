from .buffer import SunscreenInteropBuffer, DEFAULT_BUFFER_LENGTH
from .encrypted import Encrypted
from .context import SunscreenFHEContext, KeySet
from typing import Optional, Any


class EncryptedUnsigned256(Encrypted):
    def __init__(
        self,
        pointer: Any,
        context: SunscreenFHEContext,
        is_fresh: bool,
        key_set_override: Optional[KeySet],
    ):
        Encrypted.__init__(self, pointer, context, is_fresh, key_set_override)

    @classmethod
    def create_from_plain(
        cls,
        number: int,
        context: SunscreenFHEContext,
        key_set_override: Optional[KeySet] = None,
    ) -> "EncryptedUnsigned256":
        encoded_bytes = number.to_bytes(32, byteorder="big")
        buffer = SunscreenInteropBuffer.create_from_bytes(
            bytearray(encoded_bytes), context.get_rust_library()
        )
        cipher = (
            context.get_rust_library()
            .get()
            .encrypt_unsigned256(
                context.get_inner_context(),
                context.get_public_key(key_set_override),
                buffer.get(),
            )
        )

        result = EncryptedUnsigned256(
            cipher,
            context,
            True,
            key_set_override,
        )
        return result

    @classmethod
    def create_from_encrypted_cipher_bytes(
        cls,
        cipher: bytearray,
        context: SunscreenFHEContext,
        is_fresh: bool = False,
        key_set_override: Optional[KeySet] = None,
    ) -> "EncryptedUnsigned256":
        buffer = SunscreenInteropBuffer.create_from_bytes(
            cipher, context.get_rust_library()
        )
        cipher = context.get_rust_library().get().get_cipher_from_string(buffer.get())

        return EncryptedUnsigned256(cipher, context, is_fresh, key_set_override)

    @classmethod
    def create_from_encrypted_cipher_pointer(
        cls,
        cipher: Any,  # type: ignore
        context: SunscreenFHEContext,
        is_fresh: bool = False,
        key_set_override: Optional[KeySet] = None,
    ) -> "EncryptedUnsigned256":
        return EncryptedUnsigned256(cipher, context, is_fresh, key_set_override)

    def reencrypt(self):
        value = self.decrypt()
        reencrypted = EncryptedUnsigned256.create_from_plain(
            value, self.context, self.key_set_override
        )
        self.replace_pointer(reencrypted.release())
        self.is_fresh = True

    def decrypt(self) -> int:
        decrypt_buffer = SunscreenInteropBuffer.create_for_length(
            DEFAULT_BUFFER_LENGTH, self.rust_library
        )
        self.rust_library.get().decrypt_unsigned256(
            self.context.get_inner_context(),
            self.context.get_private_key(self.key_set_override),
            self.get(),
            decrypt_buffer.get(),
        )

        return int.from_bytes(decrypt_buffer.get_bytes(), byteorder="big")


class EncryptedUnsigned256Zero(EncryptedUnsigned256):
    def __init__(
        self, context: SunscreenFHEContext, key_set_override: Optional[KeySet] = None
    ):
        EncryptedUnsigned256.__init__(
            self,
            None,
            context,
            True,
            key_set_override,
        )
        encoded_bytes = int(0).to_bytes(32, byteorder="big")
        buffer = SunscreenInteropBuffer.create_from_bytes(
            bytearray(encoded_bytes), context.get_rust_library()
        )
        self.pointer = (
            context.get_rust_library()
            .get()
            .encrypt_unsigned256(
                context.get_inner_context(),
                context.get_public_key(key_set_override),
                buffer.get(),
            )
        )
