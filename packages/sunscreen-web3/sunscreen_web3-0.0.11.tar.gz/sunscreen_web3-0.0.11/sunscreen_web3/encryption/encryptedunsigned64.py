from .buffer import SunscreenInteropBuffer
from .encrypted import Encrypted
from .context import SunscreenFHEContext, KeySet
from typing import Optional, Any


class EncryptedUnsigned64(Encrypted):
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
    ) -> "EncryptedUnsigned64":
        cipher = (
            context.get_rust_library()
            .get()
            .encrypt_unsigned64(
                context.get_inner_context(),
                context.get_public_key(key_set_override),
                number,
            )
        )

        result = EncryptedUnsigned64(
            cipher,
            context,
            True,
            key_set_override,
        )
        return result

    @classmethod
    def create_from_encrypted_cipher_bytes(
        cls,
        cipher_bytes: bytearray,
        context: SunscreenFHEContext,
        is_fresh: bool = False,
        key_set_override: Optional[KeySet] = None,
    ) -> "EncryptedUnsigned64":
        buffer = SunscreenInteropBuffer.create_from_bytes(
            cipher_bytes, context.get_rust_library()
        )
        cipher = context.get_rust_library().get().get_cipher_from_string(buffer.get())

        return EncryptedUnsigned64(cipher, context, is_fresh, key_set_override)

    @classmethod
    def create_from_encrypted_cipher_pointer(
        cls,
        cipher: Any,
        context: SunscreenFHEContext,
        is_fresh: bool = False,
        key_set_override: Optional[KeySet] = None,
    ) -> "EncryptedUnsigned64":
        return EncryptedUnsigned64(cipher, context, is_fresh, key_set_override)

    def reencrypt(self):
        value = self.decrypt()
        reencrypted = EncryptedUnsigned64.create_from_plain(
            value, self.context, self.key_set_override
        )
        self.replace_pointer(reencrypted.release())
        self.is_fresh = True

    def decrypt(self):
        return self.rust_library.get().decrypt_unsigned64(
            self.context.get_inner_context(),
            self.context.get_private_key(self.key_set_override),
            self.get(),
        )


class EncryptedUnsigned64Zero(EncryptedUnsigned64):
    def __init__(
        self, context: SunscreenFHEContext, key_set_override: Optional[KeySet] = None
    ):
        EncryptedUnsigned64.__init__(
            self,
            None,
            context,
            True,
            key_set_override,
        )
        self.pointer = self.rust_library.get().encrypt_unsigned64(
            self.context.get_inner_context(),
            self.context.get_public_key(self.key_set_override),
            0,
        )
