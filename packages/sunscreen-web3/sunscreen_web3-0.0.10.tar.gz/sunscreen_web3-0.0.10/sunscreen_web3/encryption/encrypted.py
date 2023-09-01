from .buffer import SunscreenInteropBuffer, DEFAULT_BUFFER_LENGTH
from threading import RLock
from .context import SunscreenFHEContext, KeySet
from typing import Optional, Any


class Encrypted:
    DEFAULT_ZERO_WORKAROUND = 0.000000000000001

    def __init__(
        self,
        buffer: Any,
        context: SunscreenFHEContext,
        is_fresh: bool,
        key_set_override: Optional[KeySet] = None,
    ):
        self.rust_library = context.get_rust_library()
        self.pointer = buffer
        self.context = context
        self.is_fresh = is_fresh
        self.key_set_override = key_set_override
        self.lock = RLock()

    def __del__(self):
        if self.pointer:
            self.rust_library.get().release_cipher(self.pointer)

    def get(self) -> Any:
        with self.lock:
            return self.pointer

    def release(self) -> Any:
        with self.lock:
            pointer = self.get()
            self.pointer = None
            return pointer

    def replace_pointer(self, pointer: Any):  # type: ignore
        with self.lock:
            if self.pointer:
                self.rust_library.get().release_cipher(self.pointer)
            self.pointer = pointer

    def get_bytes(self) -> bytearray:
        pointer = self.get()
        if pointer:
            buffer = SunscreenInteropBuffer.create_for_length(
                DEFAULT_BUFFER_LENGTH, self.rust_library
            )
            self.rust_library.get().get_cipher_as_string(pointer, buffer.get())
            return buffer.get_bytes()
        return bytearray(0)

    @classmethod
    def fix_zero_in_plain(cls, value) -> float:
        if value == 0:
            return Encrypted.DEFAULT_ZERO_WORKAROUND

        return value
