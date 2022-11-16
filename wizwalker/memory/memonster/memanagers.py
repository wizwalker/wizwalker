import inspect
import os
import struct
from typing import Any, Generic, Type, TypeVar

from .addon_primitives import *
from .memast import memclass, ParamType

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
    "pointer": struct.Struct("<Q"),
}


class ViewBackend:
    def backend_to_propagate(self):
        return None

    def address(self) -> int:
        raise NotImplementedError()

    def set_address(self, address: int) -> None:
        raise NotImplementedError()

    def size(self) -> int:
        raise NotImplementedError()
    
    def set_size(self, size: int) -> None:
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

    def write_primitive(self, typename: str, value: int | float | bool | str, offset: int) -> None:
        t = type_dict[typename]
        assert offset + t.size <= self.size()
        self.write_bytes(t.pack(value), offset=offset)

class ExternalPointerBackend(ViewBackend):
    def __init__(self, handle: int, address: int, size: int, allocator) -> None:
        self._process_handle = handle
        self._address = address
        self._size = size
        self._allocator = allocator

    def backend_to_propagate(self):
        return ExternalUnownedPointerBackend(
            self._process_handle,
            self.address(),
            self.size(),
            self._allocator
        )

    def address(self) -> int:
        return self._address

    def set_address(self, address: int) -> None:
        self._address = address

    def size(self) -> int:
        return self._size

    def set_size(self, size: int) -> None:
        self._size = size

    def read_bytes(self, count: int, offset: int) -> bytes:
        assert offset + count <= self.size()
        buff = ctypes.create_string_buffer(count)
        _ReadProcessMemory(self._process_handle, self.address() + offset, buff, count, ctypes.c_size_t(0))
        return buff.raw

    def write_bytes(self, data: bytes, offset: int) -> None:
        assert offset + len(data) <= self.size()
        _WriteProcessMemory(self._process_handle, self.address() + offset, data, len(data), ctypes.c_size_t(0))


class ExternalOwnedPointerBackend(ExternalPointerBackend):
    def set_size(self, size: int) -> None:
        raise ValueError()

    def set_address(self, address: int) -> None:
        raise ValueError()

class ExternalUnownedPointerBackend(ExternalPointerBackend):
    pass


MTV = TypeVar("MTV")
MTT = TypeVar("MTT", bound="MemType")
@memclass
class MemType(Generic[MTV]):
    _offset: ParamType | int = 0
    _view: "MemoryView" = None
    
    def __post_init__(self):
        pass

    def propagate_view(self) -> None:
        # could probably do this lazily
        for name, field in inspect.getmembers(self):
            if issubclass(type(field), MemType):
                attr: MemType = self.__getattribute__(name)
                attr._view = self._view
                attr.load_view(self._view, self._offset + attr._offset)

    def load_view(self: MTT, view: "MemoryView", offset=0) -> MTT:
        self._view = view
        self._offset = offset
        self.propagate_view()
        return self

    # TODO: Bounds are not checked
    @classmethod
    def from_view(cls: Type[MTT], view: "MemoryView") -> MTT:
        result = cls(0)
        result.load_view(view, 0)
        return result
    
    def get_dummy_inst(self: Type[MTT]) -> MTT:
        return type(self)(0)

    def fieldsize(self) -> int:
        raise NotImplementedError()

    def fieldview(self) -> "MemoryView":
        return self._view.subview(self.fieldsize(), self._offset)

    def read(self) -> MTV:
        raise NotImplementedError()

    def write(self, value: MTV):
        raise NotImplementedError

    def isnull(self) -> bool:
        return self.fieldview().backend.address() == 0


MPT = TypeVar("MPT", bound=MemType)

@memclass
class MemPointer(MemType[MPT]):
    _dummy: ParamType | Type[MPT]

    def propagate_view(self) -> None:
        for name, field in vars(type(self)).items():
            if issubclass(type(field), MemType):
                attr: MemType = self.__getattribute__(name)
                # Propagating into the dummy would be a waste of time
                if id(attr) == self._dummy:
                    continue
                attr._view = self._view
                attr.load_view(self._view, attr._offset)

    def fieldsize(self) -> int:
        return type_dict["pointer"].size

    def read(self) -> MPT:
        view = self.fieldview()
        result: MemType = self._dummy.get_dummy_inst()
        result.load_view(view.ptr_view(result.fieldsize()))
        return result

    def write(self, value: int):
        view = self.fieldview()
        view.write_primitive("pointer", value)

    def alloc_dummy(self, dummy: MPT = None):
        ## Replaces the stored dummy, allocates it and writes the new address
        if dummy is not None:
            self._dummy = dummy
        allocated: MemoryView = self._view.backend._allocator.alloc(self._dummy.fieldsize())
        self.write(allocated.backend.address())
        self.read().propagate_view()

MPT = TypeVar("MPT", int, float, str, bool)
@memclass
class MemPrimitive(MemType, Generic[MPT]):
    # defined by stuff that inherits from it
    typename: ParamType | str = ""

    def get_dummy_inst(self):
        return type(self)(0, self.typename)

    def fieldsize(self) -> int:
        return type_dict[self.typename].size

    def read(self) -> MPT:
        t = type_dict[self.typename]
        view = self.fieldview()
        vals = t.unpack(view.read_bytes(t.size))
        if len(vals) == 1:
            return vals[0]
        else:
            return vals

    def write(self, value: MPT):
        t = type_dict[self.typename]
        view = self.fieldview()
        view.write_bytes(t.pack(value))


class MemoryView:
    def __init__(self, backend: ViewBackend) -> None:
        self.backend = backend

    def read_bytes(self, count: int, offset=0) -> bytes:
        return self.backend.read_bytes(count, offset)

    def write_bytes(self, data: bytes, offset=0) -> None:
        self.backend.write_bytes(data, offset)

    def read_primitive(self, typename: str, offset=0) -> int | float | bool | str:
        return self.backend.read_primitive(typename, offset)

    def write_primitive(self, typename: str, value: int | float | bool | str, offset=0) -> None:
        self.backend.write_primitive(typename, value, offset)

    def read_typestring(self, typestring: str, offset=0) -> Any:
        s = struct.Struct(typestring)
        return s.unpack(self.backend.read_bytes(s.size, offset))

    def write_typestring(self, typestring: str, values: tuple, offset=0):
        s = struct.Struct(typestring)
        self.backend.write_bytes(s.pack(*values), offset)

    def subview(self, size: int, offset=0) -> "MemoryView":
        back = self.backend.backend_to_propagate()
        assert back
        assert offset + size <= self.backend.size()
        result = MemoryView(back)
        result.backend.set_address(self.backend.address() + offset)
        result.backend.set_size(size)
        return result

    def ptr_view(self, size: int, offset=0) -> "MemoryView":
        back = self.backend.backend_to_propagate()
        assert back
        result = MemoryView(back)
        result.backend.set_address(self.read_primitive("pointer", offset))
        result.backend.set_size(size)
        return result


class AllocatorError(RuntimeError):
    pass

T = TypeVar("T", bound=MemoryView)
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

    def alloc(self, size: int) -> MemoryView:
        raise NotImplementedError()

    def alloc0(self, size: int) -> MemoryView:
        result = self.alloc(size)
        result.write_bytes("\x00" * size)
        return result

    def free(self, ptr: MemoryView) -> None:
        # can't provide default because order of dealloc and _removeptr might matter
        raise NotImplementedError()

class ProcessAllocator(BaseAllocator):
    def __init__(self, process_handle: wintypes.HANDLE) -> None:
        super().__init__()
        # Could optimize to use pages correctly
        self.process_handle = process_handle

    def alloc(self, size: int) -> MemoryView:
        # could use large pages for big allocs
        if lpvoid := _VirtualAllocEx(
            self.process_handle,
            wintypes.LPVOID(0),
            size,
            0x1000 | 0x2000, # MEM_COMMIT and MEM_RESERVE
            0x40, # PAGE_EXECUTE_READWRITE
            ):
            ptr = MemoryView(ExternalOwnedPointerBackend(
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
    from memtypes import *
    def _main():
        @memclass
        class TestType(MemType):
            def fieldsize(self) -> int:
                return 32 + 12 + 8

            name = MemCppString(0)
            position = MemXYZ(32)
            ptr = MemPointer(44, MemXYZ(0))

        pid = os.getpid()
        # PROCESS_ALL_ACCESS
        handle = ctypes.windll.kernel32.OpenProcess(0xF0000 | 0x100000 | 0xFFFF, 0, pid)

        allocator = ProcessAllocator(handle)

        x = ctypes.c_uint64(0xBE1211)
        xt = MemInt64.from_view(MemoryView(ExternalUnownedPointerBackend(
            handle, type_dict["pointer"].unpack(ctypes.pointer(x))[0], 8, allocator
        )))
        print(xt.typename)
        print(hex(xt.read()))


        testview = allocator.alloc0(32+12+8)
        testtypeview = TestType.from_view(testview)

        testtypeview.name.write("test123456789test")
        print(testtypeview.name.read())
        testtypeview.name.write("test")
        print(testtypeview.name.read())

        print(testtypeview.name.fieldview().backend.address())
        print(testtypeview.position.fieldview().backend.address())
        print(testtypeview.position.x.fieldview().backend.address())

        testtypeview.position.x.write(1.0)
        print(testtypeview.position.x.read())
        print(testtypeview.position.read())

        testtypeview.ptr.alloc_dummy()

        testtypeview.ptr.read().write(XYZ(1.0, 2.0, 3.0))
        print(testtypeview.ptr.read().x._offset)
        testtypeview.ptr.read().x.write(99.0)
        print(testtypeview.ptr.read().read())

        ctypes.windll.kernel32.CloseHandle(handle)

    _main()

