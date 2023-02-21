from ctypes.wintypes import HANDLE

import regex
import pefile
import pymem
import pymem.memory
import pymem.exception
import pymem.process
import pymem.ressources.structure

from memonster.memanagers import WindowsBackend

from wizwalker import (
    PatternFailed,
    PatternMultipleResults,
    utils,
)


class Process:
    def __init__(self, handle: HANDLE) -> None:
        self.handle = handle
        self._symbol_table = {}
        self._memory_backend = None
    
    @property
    def is_running(self) -> bool:
        return utils.check_if_process_running(self.handle)

    @property
    def memory_backend(self) -> WindowsBackend:
        if self.is_running():
            if self._memory_backend == None:
                self._memory_backend = WindowsBackend(self.handle)
            return self._memory_backend

    def _get_symbols(self, file_path: str, *, force_reload: bool = False):
        if (dll_table := self._symbol_table.get(file_path)) and not force_reload:
            return dll_table

        # exe_path = utils.get_wiz_install() / "Bin" / "WizardGraphicalClient.exe"
        pe = pefile.PE(file_path)

        symbols = {}

        for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            if exp.name:
                symbols[exp.name.decode()] = exp.address

            else:
                symbols[f"Ordinal {exp.ordinal}"] = exp.address

        self._symbol_table[file_path] = symbols
        return symbols

    def _scan_page_return_all(self, address, pattern):
        mbi = pymem.memory.virtual_query(self.handle, address)
        next_region = mbi.BaseAddress + mbi.RegionSize
        allowed_protections = [
            pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_READ,
            pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_READWRITE,
            pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READWRITE,
            pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READONLY,
        ]
        if (
            mbi.state != pymem.ressources.structure.MEMORY_STATE.MEM_COMMIT
            or mbi.protect not in allowed_protections
        ):
            return next_region, None

        page_bytes = self.memory_backend.read_bytes(mbi.RegionSize, address)

        found = []

        for match in regex.finditer(pattern, page_bytes, regex.DOTALL):
            found_address = address + match.span()[0]
            found.append(found_address)

        return next_region, found

    def _scan_all(
        self,
        pattern: bytes,
        return_multiple: bool = False,
    ):
        next_region = 0

        found = []
        while next_region < 0x7FFFFFFF0000:
            next_region, page_found = self._scan_page_return_all(
                next_region, pattern
            )
            if page_found:
                found += page_found

            if not return_multiple and found:
                break

        return found

    def _scan_entire_module(self, module, pattern):
        base_address = module.lpBaseOfDll
        max_address = module.lpBaseOfDll + module.SizeOfImage
        page_address = base_address

        found = []
        while page_address < max_address:
            page_address, page_found = self._scan_page_return_all(
                page_address, pattern
            )
            if page_found:
                found += page_found

        return found

    def pattern_scan(
        self, pattern: bytes, *, module: str = None, return_multiple: bool = False
    ) -> list | int:
        """
        Scan for a pattern

        Args:
            pattern: The byte pattern to search for
            module: What module to search or None to search all
            return_multiple: If multiple results should be returned

        Raises:
            PatternFailed: If the pattern returned no results
            PatternMultipleResults: If the pattern returned multiple results and return_multple is False

        Returns:
            A list of results if return_multple is True otherwise one result
        """
        if module:
            module_object = pymem.process.module_from_name(self.process.process_handle, module)

            if module_object is None:
                raise ValueError(f"{module} module not found.")

            found_addresses = self._scan_entire_module(module_object, pattern)

        else:
            found_addresses = self._scan_all(pattern, return_multiple)

        if (found_length := len(found_addresses)) == 0:
            raise PatternFailed(pattern)
        elif found_length > 1 and not return_multiple:
            raise PatternMultipleResults(f"Got {found_length} results for {pattern}")
        elif return_multiple:
            return found_addresses
        else:
            return found_addresses[0]

    def get_address_from_symbol(
        self,
        module_name: str,
        symbol_name: str,
        *,
        module_dir: str = None,
        force_reload: bool = False,
    ) -> int:
        """
        Get an address from a module using its symbol

        Args:
            module_name: Name of the module
            symbol_name: Name of the symbol
            module_dir: Dir the module is within
            force_reload: Force export table reload

        Returns:
            The address of the symbol in memory

        Raises:
            ValueError: No symbol/module with that name
        """
        if not module_dir:
            module_dir = utils.get_system_directory()

        file_path = module_dir / module_name

        if not file_path.exists():
            raise ValueError(f"No module named {module_name}")

        symbols = self._get_symbols(file_path, force_reload=force_reload)

        if not (symbol := symbols.get(symbol_name)):
            raise ValueError(f"No symbol named {symbol_name} in module {module_name}")

        module = pymem.process.module_from_name(
            self.handle, module_name
        )

        return module.lpBaseOfDll + symbol

    def start_thread(self, address: int):
        """
        Start a thread at an address

        Args:
            address: The address to start the thread at
        """
        p = pymem.Pymem()
        p.process_handle = self.handle
        p.start_thread(address)
