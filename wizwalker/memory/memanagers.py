import os
import struct
from typing import Type, TypeVar

import ctypes
from ctypes import wintypes
_kernel32 = ctypes.windll.kernel32

_ReadProcessMemory = _kernel32.ReadProcessMemory
_ReadProcessMemory.argtypes = (
    wintypes.HANDLE,
    wintypes.LPCVOID,
    wintypes.LPVOID,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_size_t)
)
_ReadProcessMemory.restype = wintypes.BOOL

_WriteProcessMemory = _kernel32.WriteProcessMemory
_WriteProcessMemory.argtypes = (
    wintypes.HANDLE,
    wintypes.LPVOID,
    wintypes.LPCVOID,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_size_t)
)
_WriteProcessMemory.restype = wintypes.BOOL

_VirtualAllocEx = _kernel32.VirtualAllocEx
_VirtualAllocEx.argtypes = (
    wintypes.HANDLE,
    wintypes.LPVOID,
    ctypes.c_size_t,
    wintypes.DWORD,
    wintypes.DWORD
)
_VirtualAllocEx.restype = wintypes.LPVOID

_VirtualFreeEx = _kernel32.VirtualFreeEx
_VirtualFreeEx.argtypes = (
    wintypes.HANDLE,
    wintypes.LPVOID,
    ctypes.c_size_t,
    wintypes.DWORD,
)
_VirtualFreeEx.restype = wintypes.BOOL



type_dict = {
    # int types
    "int8": struct.Struct("<b"),
    "uint8": struct.Struct("<B"),
    "int16": struct.Struct("<h"),
    "uint16": struct.Struct("<H"),
    "int32": struct.Struct("<i"),
    "uint32": struct.Struct("<I"),
    "int64": struct.Struct("<q"),
    "uint64": struct.Struct("<Q"),

    # float types
    "float32": struct.Struct("<f"),
    "float64": struct.Struct("<d"),

    # other types
    "bool": struct.Struct("?"),
    "char": struct.Struct("<c"),

    # special
    "pointer": struct.Struct("<Q")
}


class ViewBackend:
    def address(self) -> int:
        raise NotImplementedError()

    def size(self) -> int:
        raise NotImplementedError()

    def end_address(self) -> int:
        return self.address() + self.size()

    def read_bytes(self, count: int, offset: int) -> bytes:
        raise NotImplementedError()

    def write_bytes(self, data: bytes, offset: int) -> None:
        raise NotImplementedError()

    def read_primitive(self, typename: str, offset=0) -> int | float | bool | str:
        t = type_dict[typename]
        assert offset + t.size <= self.size()
        return t.unpack(self.read_bytes(t.size, offset=offset))[0]

    def write_primitive(self, typename: str, value, offset: int) -> None:
        t = type_dict[typename]
        assert offset + t.size <= self.size()
        self.write_bytes(t.pack(value), offset=offset)

    def read_primitive_array(self, typename: str, count: int, offset: int) -> list[int | float | bool | str]:
        t = type_dict[typename]
        assert offset + t.size * count <= self.size()

        arr_bytes = self.read_bytes(t.size * count, offset)
        structstr = "<" + t.format.replace("<", "") * count
        return struct.unpack(structstr, arr_bytes)

    def write_primitive_array(self, typename: str, values, offset: int):
        t = type_dict[typename]
        assert offset + t.size * len(values) <= self.size()

        structstr = "<" + t.format.replace("<", "") * len(values)
        arr_bytes = struct.pack(structstr, values)
        self.write_bytes(arr_bytes, offset)

class ExternalPointerBackend(ViewBackend):
    def __init__(self, handle: int, address: int, size: int) -> None:
        self._process_handle = handle
        self._address = address
        self._size = size

    def address(self) -> int:
        return self._address

    def size(self) -> int:
        return self._size

    def read_bytes(self, count: int, offset: int) -> bytes:
        assert offset + count <= self.size()
        buff = ctypes.create_string_buffer(count)
        _ReadProcessMemory(self._process_handle, self.address() + offset, buff, count, ctypes.c_size_t(0))
        return buff.raw

    def write_bytes(self, data: bytes, offset: int) -> None:
        assert offset + len(data) <= self.size()
        _WriteProcessMemory(self._process_handle, self.address() + offset, data, len(data), ctypes.c_size_t(0))


class ExternalOwnedPointerBackend(ExternalPointerBackend):
    def __init__(self, handle: int, address: int, size: int, allocator: "BaseAllocator") -> None:
        super().__init__(handle, address, size)
        self._by_allocator = allocator

class ExternalUnownedPointerBackend(ExternalPointerBackend):
    pass


class MemoryView:
    ## Forwarded functions for convenience so objects that inherit from it can use them directly

    def __init__(self, backend: ViewBackend) -> None:
        self.backend = backend

    @staticmethod
    def obj_size() -> int:
        raise NotImplementedError()

    def read_bytes(self, count: int, offset=0) -> bytes:
        return self.backend.read_bytes(count, offset)

    def write_bytes(self, data: bytes, offset=0) -> None:
        self.backend.write_bytes(data, offset)

    def read_primitive(self, typename: str, offset=0) -> int | float | bool | str:
        return self.backend.read_primitive(typename, offset)

    def write_primitive(self, typename: str, value, offset=0) -> None:
        self.backend.write_primitive(typename, value, offset)

    def read_primitive_array(self, typename: str, count=1, offset=0) -> list[int | float | bool | str]:
        return self.backend.read_primitive_array(typename, count, offset)

    def write_primitive_array(self, typename: str, values, offset=0):
        self.backend.write_primitive_array(typename, values, offset)

class AllocatorError(RuntimeError):
    pass

T = TypeVar("T", bound="MemoryView")
class BaseAllocator:
    def __init__(self) -> None:
        ## Not thread safe!
        # _owned_pointers remains sorted so it's reasonable efficient
        # Most likely want to use a tree structure instead though, this may be too slow
        self._owned_pointers: list[MemoryView] = []

    def _addptr(self, ptr: MemoryView) -> None:
        assert isinstance(ptr.backend, ExternalOwnedPointerBackend)
        if len(self._owned_pointers) == 0:
            self._owned_pointers = [ptr]
            return
        i = 0
        addr = ptr.backend.address()
        while i < len(self._owned_pointers):
            cur = self._owned_pointers[i]
            if addr < cur.backend.address():
                # insert here
                self._owned_pointers.insert(i, ptr)
                break
            elif addr > cur.backend.address():
                if i + 1 >= len(self._owned_pointers):
                    # insert at end
                    self._owned_pointers.append(ptr)
                    break
                # continue on
                i += 1
            else:
                # should not happen, but if it does we will escape quickly
                break

    def _removeptr(self, ptr: MemoryView) -> None:
        assert isinstance(ptr.backend, ExternalOwnedPointerBackend)
        i = 0
        addr = ptr.backend.address()
        while i < len(self._owned_pointers):
            if addr == self._owned_pointers[i].backend.address():
                self._owned_pointers.pop(i)
                break

    def alloc(self, size: int, cls=MemoryView) -> MemoryView:
        raise NotImplementedError()

    def alloc(self, cls: Type[T]) -> T:
        return self.alloc(cls.obj_size(), cls)

    def free(self, ptr: MemoryView) -> None:
        # can't provide default because order of dealloc and _removeptr might matter
        raise NotImplementedError()

class ProcessAllocator(BaseAllocator):
    def __init__(self, process_handle: wintypes.HANDLE) -> None:
        super().__init__()
        # Could optimize to use pages correctly
        self.process_handle = process_handle

    def alloc(self, size: int, cls=MemoryView) -> MemoryView:
        # could use large pages for big allocs
        if lpvoid := _VirtualAllocEx(
            self.process_handle,
            wintypes.LPVOID(0),
            size,
            0x1000 | 0x2000, # MEM_COMMIT and MEM_RESERVE
            0x40, # PAGE_EXECUTE_READWRITE
            ):
            ptr = cls(ExternalOwnedPointerBackend(
                self.process_handle,
                int(lpvoid),
                size,
                self
            ))
            self._addptr(ptr)
            return ptr
        else:
            raise AllocatorError("VirtualAllocEx failed")

    def free(self, ptr: MemoryView) -> None:
        assert isinstance(ptr.backend, ExternalOwnedPointerBackend)
        self._removeptr(ptr) # dealloc after this, maybe it matters
        _VirtualFreeEx(
            self.process_handle,
            ptr.backend.address(),
            0,
            0x8000 # MEM_RELEASE
        )
        # TODO: Maybe just marking as dead would be better
        del ptr

class CaveAllocator(ProcessAllocator):
    ## Prone to fatal fragmentation, has no solution

    def __init__(self, cave_base: int, cave_size: int, process_handle: wintypes.HANDLE) -> None:
        super().__init__(process_handle)
        self.cave_base = cave_base
        self.cave_size = cave_size

    def start_addr(self) -> int:
        return self.cave_base

    def end_addr(self) -> int:
        return self.cave_base + self.cave_size

    def unsafe_view(self, start_offset=0, size=None, cls=MemoryView) -> MemoryView:
        size = size if size is not None else self.cave_size
        assert start_offset + size <= self.cave_size
        
        return cls(ExternalUnownedPointerBackend(
            self.process_handle,
            self.start_addr() + start_offset,
            size
        ))

    def unsafe_view(self, cls: Type[T], start_offset=0, size=None) -> T:
        return self.unsafe_view(start_offset=start_offset, size=size, cls=cls)

    def _find_free_block(self, size: int) -> int | None:
        # This is "slow" and fragmentation from alloc+free may lead this to return None when it worked before
        assert size <= self.cave_size

        if len(self._owned_pointers) == 0:
            return self.cave_base

        # check if there is space inbetween two blocks (from a previous free perhaps)
        i = 0
        while i + 1 < len(self._owned_pointers):
            cur = self._owned_pointers[i]
            next = self._owned_pointers[i+1]

            space = next.backend.address() - cur.backend.end_address()
            if space >= size:
                return cur.backend.end_address()
            i += 1

        # check if there is space at the end
        last = self._owned_pointers[-1]
        if last.backend.end_address() + size < self.end_addr():
            return last.backend.end_address()

    def alloc(self, size: int, cls=MemoryView) -> MemoryView:
        assert size <= self.cave_size
        if block_start := self._find_free_block(size):
            ptr = cls(ExternalOwnedPointerBackend(
                self.process_handle,
                block_start,
                size,
                self
            ))
            self._addptr(ptr)
            return ptr
        else:
            raise AllocatorError(f"Cave doesn't have a free block of size >= {size}")

    def free(self, ptr: MemoryView):
        assert isinstance(ptr.backend, ExternalOwnedPointerBackend)
        self._removeptr(ptr)
        # TODO: Maybe just marking as dead would be better
        del ptr

if __name__ == "__main__":
    def _main():
        pid = os.getpid()
        # PROCESS_ALL_ACCESS
        handle = ctypes.windll.kernel32.OpenProcess(0xF0000 | 0x100000 | 0xFFFF, 0, pid)

        x = ctypes.c_uint64(0xBE1211)
        x_view = MemoryView(ExternalUnownedPointerBackend(
            handle, type_dict["pointer"].unpack(ctypes.pointer(x))[0], 8
        ))
        print(hex(x_view.read_primitive("int64")))

        ctypes.windll.kernel32.CloseHandle(handle)

    _main()

