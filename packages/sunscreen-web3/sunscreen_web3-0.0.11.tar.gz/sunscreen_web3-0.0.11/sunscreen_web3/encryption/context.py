import ctypes
from .buffer import SunscreenInteropBuffer, DEFAULT_BUFFER_LENGTH
from .rustlibrary import RustLibrary
from typing import Optional


class KeySet:
    def __init__(
        self,
        public_key: ctypes.c_void_p,
        private_key: Optional[ctypes.c_void_p],
        rust_library: RustLibrary,
    ):
        self.public_key = public_key
        self.private_key = private_key
        self.rust_library = rust_library

    @classmethod
    def initialize_from_pointers(
        cls, public_key: ctypes.c_void_p, private_key: Optional[ctypes.c_void_p] = None
    ) -> "KeySet":
        return KeySet(public_key, private_key, RustLibrary())

    @classmethod
    def initialize_from_bytes(
        cls, public_key: bytearray, private_key: Optional[bytearray] = None
    ) -> "KeySet":
        library = RustLibrary()
        buffer = SunscreenInteropBuffer.create_from_bytes(public_key, library)
        public_key_obj = library.get().get_public_key_from_string(buffer.get())
        private_key_obj = None
        if private_key:
            raise Exception("Unimplemented with private key")
            pvt_buffer = SunscreenInteropBuffer.create_from_bytes(private_key, library)
            private_key_obj = library.get().get_private_key_from_string(
                pvt_buffer.get()
            )

        return KeySet(public_key_obj, private_key_obj, library)

    @classmethod
    def initialize_from_bytes_with_public_key(cls, public_key: bytearray) -> "KeySet":
        return KeySet.initialize_from_bytes(public_key, None)

    def get_public_key(self) -> ctypes.c_void_p:
        return self.public_key

    def get_private_key(self) -> Optional[ctypes.c_void_p]:
        return self.private_key

    def get_public_key_as_bytes(self) -> bytearray:
        param_buffer = SunscreenInteropBuffer.create_for_length(
            DEFAULT_BUFFER_LENGTH, self.rust_library
        )

        self.rust_library.get().get_public_key_as_string(
            self.public_key, param_buffer.get()
        )
        return param_buffer.get_bytes()

    def __del__(self):
        if self.public_key:
            self.rust_library.get().release_public_key(self.public_key)
        if self.private_key:
            self.rust_library.get().release_private_key(self.private_key)


class SunscreenFHEContext:
    def __init__(self, rust_library: RustLibrary, context: ctypes.c_void_p):
        self.rust_library = rust_library
        self.context = context
        self.key_set = None

    @classmethod
    def create_from_params_as_string(cls, params: str) -> "SunscreenFHEContext":
        rust_library = RustLibrary()
        buffer = SunscreenInteropBuffer.create_from_string(params, rust_library)
        context = rust_library.get().initialize_context_with_params_as_string(
            buffer.get()
        )
        return SunscreenFHEContext(rust_library, context)

    @classmethod
    def create_from_params_as_bytes(cls, params: bytearray) -> "SunscreenFHEContext":
        rust_library = RustLibrary()
        buffer = SunscreenInteropBuffer.create_from_bytes(params, rust_library)
        context = rust_library.get().initialize_context_with_params_as_string(
            buffer.get()
        )
        return SunscreenFHEContext(rust_library, context)

    @classmethod
    def create_from_standard_params(cls) -> "SunscreenFHEContext":
        rust_library = RustLibrary()
        context = rust_library.get().initialize_context_with_standard_params()
        return SunscreenFHEContext(rust_library, context)

    def __del__(self):
        if self.context:
            self.rust_library.get().release_context(self.context)

    def get_rust_library(self) -> RustLibrary:
        return self.rust_library

    def get_inner_context(self) -> ctypes.c_void_p:
        return self.context

    def get_params(self) -> bytearray:
        param_buffer = SunscreenInteropBuffer.create_for_length(
            DEFAULT_BUFFER_LENGTH, self.rust_library
        )
        self.rust_library.get().get_params_as_string(self.context, param_buffer.get())

        return param_buffer.get_bytes()

    def get_public_key(
        self, key_set_override: Optional[KeySet] = None
    ) -> Optional[ctypes.c_void_p]:
        if key_set_override:
            return key_set_override.get_public_key()

        if self.key_set:
            return self.key_set.get_public_key()

        return None

    def get_private_key(
        self, key_set_override: Optional[KeySet] = None
    ) -> Optional[ctypes.c_void_p]:
        if key_set_override:
            return key_set_override.get_private_key()

        if self.key_set:
            return self.key_set.get_private_key()

        return None

    def generate_keys(self) -> KeySet:
        keys = self.rust_library.get().generate_keys(self.context)
        public_key = self.rust_library.get().get_public_key(keys)
        private_key = self.rust_library.get().get_private_key(keys)
        self.key_set = KeySet(public_key, private_key, self.rust_library)
        return self.key_set
