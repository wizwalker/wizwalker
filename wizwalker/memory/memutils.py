import asyncio
import regex
from typing import Union

import pefile
import pymem.process

from ctypes import wintypes

from .memonster import memanagers
from wizwalker import (
    PatternFailed,
    PatternMultipleResults,
    utils,
)


def _scan_page_return_all(handle, address, pattern):
    mbi = pymem.memory.virtual_query(handle, address)
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

    page_view = memanagers.ProcessUnownedPointer(address, mbi.RegionSize, handle)
    page_bytes = page_view.read_bytes(mbi.RegionSize)

    found = []

    for match in regex.finditer(pattern, page_bytes, regex.DOTALL):
        found_address = address + match.span()[0]
        found.append(found_address)

    return next_region, found

def _scan_all(
    handle: int,
    pattern: bytes,
    return_multiple: bool = False,
):
    next_region = 0

    found = []
    while next_region < 0x7FFFFFFF0000:
        next_region, page_found = _scan_page_return_all(
            handle, next_region, pattern
        )
        if page_found:
            found += page_found

        if not return_multiple and found:
            break

    return found

def _scan_entire_module(handle, module, pattern):
    base_address = module.lpBaseOfDll
    max_address = module.lpBaseOfDll + module.SizeOfImage
    page_address = base_address

    found = []
    while page_address < max_address:
        page_address, page_found = _scan_page_return_all(
            handle, page_address, pattern
        )
        if page_found:
            found += page_found

    return found

async def pattern_scan(
    handle, pattern: bytes, size_of_views: int = None, *, module: str = None, return_multiple: bool = False
) -> Union[list, int, memanagers.MemoryView]:
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
        module_object = pymem.process.module_from_name(handle, module)

        if module_object is None:
            raise ValueError(f"{module} module not found.")

        # this can take a long time to run when collecting multiple results
        # so must be run in an executor
        found_addresses = await utils.run_in_executor(
            _scan_entire_module,
            handle,
            module_object,
            pattern,
        )

    else:
        found_addresses = await utils.run_in_executor(
            _scan_all,
            handle,
            pattern,
            return_multiple,
        )

    if (found_length := len(found_addresses)) == 0:
        raise PatternFailed(pattern)
    elif found_length > 1 and not return_multiple:
        raise PatternMultipleResults(f"Got {found_length} results for {pattern}")
    elif return_multiple:
        if size_of_views:
            result = []
            for addr in found_addresses:
                result.append(memanagers.MemoryView(
                    memanagers.ExternalUnownedPointerBackend(
                        handle,
                        addr,
                        size_of_views,
                    )
                ))
            return result
        return found_addresses
    else:
        if size_of_views:
            return memanagers.MemoryView(
                memanagers.ExternalUnownedPointerBackend(
                    handle,
                    found_addresses[0],
                    size_of_views,
                )
            )
        return found_addresses[0]


# TODO: figure out how params works
async def start_thread(process, address: int):
    """
    Start a thread at an address

    Args:
        address: The address to start the thread at
    """
    await utils.run_in_executor(process.start_thread, address)


def is_running(handle) -> bool:
    """
    If the process we're reading/writing to/from is running
    """
    return utils.check_if_process_running(handle)


def _get_symbols(file_path: str):
    # exe_path = utils.get_wiz_install() / "Bin" / "WizardGraphicalClient.exe"
    pe = pefile.PE(file_path)

    symbols = {}

    for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        if exp.name:
            symbols[exp.name.decode()] = exp.address

        else:
            symbols[f"Ordinal {exp.ordinal}"] = exp.address

    return symbols

async def get_address_from_symbol(
    handle: wintypes.HANDLE,
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

    symbols = await utils.run_in_executor(
        _get_symbols, file_path, force_reload=force_reload
    )

    if not (symbol := symbols.get(symbol_name)):
        raise ValueError(f"No symbol named {symbol_name} in module {module_name}")

    module = pymem.process.module_from_name(
        handle, module_name
    )

    return module.lpBaseOfDll + symbol
