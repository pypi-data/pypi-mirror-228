import ctypes
from threading import RLock
from typing import Any
from .rustlibrary import RustLibrary

DEFAULT_BUFFER_LENGTH = 50 * 1024 * 1024


class SunscreenInteropBuffer:
    def __init__(self, buffer, rust_library: RustLibrary):
        self.library = rust_library
        self.buffer = buffer
        self.lock = RLock()

    @classmethod
    def create_from_string(
        cls, data: str, rust_library: RustLibrary
    ) -> "SunscreenInteropBuffer":
        encoded = bytearray(data, encoding="UTF-8")
        return SunscreenInteropBuffer.create_from_bytes(encoded, rust_library)

    @classmethod
    def create_from_bytes(
        cls, data: bytearray, rust_library: RustLibrary
    ) -> "SunscreenInteropBuffer":
        encoded = data
        length = len(encoded)
        buffer = None
        try:
            buffer = SunscreenInteropBuffer.__malloc_rust(length, rust_library)
            pointer = rust_library.get().buffer_data(buffer)
            encoded_ptr = (ctypes.c_char * length).from_buffer(encoded)
            ctypes.memmove(pointer, encoded_ptr, length)
            rust_library.get().set_buffer_length(buffer, length)
            return SunscreenInteropBuffer(buffer, rust_library)
        except:
            if buffer:
                SunscreenInteropBuffer.__free_rust(buffer, rust_library)
            raise

    @classmethod
    def create_for_length(
        cls, length: int, rust_library: RustLibrary
    ) -> "SunscreenInteropBuffer":
        buffer = None
        try:
            buffer = SunscreenInteropBuffer.__malloc_rust(length, rust_library)
            return SunscreenInteropBuffer(buffer, rust_library)
        except:
            if buffer:
                SunscreenInteropBuffer.__free_rust(buffer, rust_library)
            raise

    def get_bytes(self) -> bytearray:
        length = self.library.get().buffer_length(self.get())
        buffer = bytearray(length)
        buffer_ptr = (ctypes.c_char * length).from_buffer(buffer)
        pointer = self.library.get().buffer_data(self.get())
        ctypes.memmove(buffer_ptr, pointer, length)

        return buffer

    def get(self) -> Any:
        with self.lock:
            return self.buffer

    def release(self) -> Any:
        with self.lock:
            buffer = self.buffer
            self.buffer = None
            return buffer

    def replace_buffer(self, buffer) -> None:
        with self.lock:
            self.buffer = buffer

    def __del__(self):
        if self.buffer:
            SunscreenInteropBuffer.__free_rust(self.buffer, self.library)

    @classmethod
    def __malloc_rust(cls, size: int, rust_library: RustLibrary) -> Any:
        return rust_library.get().buffer_create(size)

    @classmethod
    def __free_rust(
        cls, ptr: Any, rust_library: RustLibrary  # type: ignore
    ):
        rust_library.get().buffer_release(ptr)
