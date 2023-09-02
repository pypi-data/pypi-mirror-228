from .buffer import SunscreenInteropBuffer
from .encrypted import Encrypted
from .context import SunscreenFHEContext, KeySet
from typing import Optional, Any


class EncryptedSigned(Encrypted):
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
    ) -> "EncryptedSigned":
        cipher = (
            context.get_rust_library()
            .get()
            .encrypt_signed(
                context.get_inner_context(),
                context.get_public_key(key_set_override),
                number,
            )
        )

        result = EncryptedSigned(
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
    ) -> "EncryptedSigned":
        buffer = SunscreenInteropBuffer.create_from_bytes(
            cipher_bytes, context.get_rust_library()
        )
        cipher = context.get_rust_library().get().get_cipher_from_string(buffer.get())

        return EncryptedSigned(cipher, context, is_fresh, key_set_override)

    @classmethod
    def create_from_encrypted_cipher_pointer(
        cls,
        cipher: Any,
        context: SunscreenFHEContext,
        is_fresh: bool = False,
        key_set_override: Optional[KeySet] = None,
    ) -> "EncryptedSigned":
        return EncryptedSigned(cipher, context, is_fresh, key_set_override)

    def reencrypt(self):
        value = self.decrypt()
        reencrypted = EncryptedSigned.create_from_plain(
            value, self.context, self.key_set_override
        )
        self.replace_pointer(reencrypted.release())
        self.is_fresh = True

    def decrypt(self) -> int:
        return self.rust_library.get().decrypt_signed(
            self.context.get_inner_context(),
            self.context.get_private_key(self.key_set_override),
            self.get(),
        )


class EncryptedSignedZero(EncryptedSigned):
    def __init__(
        self, context: SunscreenFHEContext, key_set_override: Optional[KeySet] = None
    ):
        EncryptedSigned.__init__(
            self,
            None,
            context,
            True,
            key_set_override,
        )
        self.pointer = self.rust_library.get().encrypt_signed(
            self.context.get_inner_context(),
            self.context.get_public_key(self.key_set_override),
            0,
        )
