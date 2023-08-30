


from __future__ import annotations
from enum import Enum, auto 

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from janis_core.types import DataType

from janis_core.types import (
    File, 
    Directory,
    UnionType,
    Filename,
    Stdout,
    Filename
)


class DTypeType(Enum):
    SECONDARY_ARRAY = auto()
    SECONDARY       = auto()
    FILE_PAIR_ARRAY = auto()
    FILE_PAIR       = auto()
    FILE_ARRAY      = auto()
    FILE            = auto()
    FILENAME        = auto()
    FLAG_ARRAY      = auto()
    FLAG            = auto()
    GENERIC_ARRAY   = auto()
    GENERIC         = auto()
    STDOUT          = auto()

def get_dtt(dtype: DataType) -> DTypeType:
    if is_stdout_type(dtype):
        return DTypeType.STDOUT
    
    elif is_secondary_array_type(dtype):
        return DTypeType.SECONDARY_ARRAY
    
    elif is_secondary_type(dtype):
        return DTypeType.SECONDARY

    elif is_file_pair_array_type(dtype):
        return DTypeType.FILE_PAIR_ARRAY

    elif is_file_pair_type(dtype):
        return DTypeType.FILE_PAIR

    elif is_file_array_type(dtype):
        return DTypeType.FILE_ARRAY

    elif is_file_type(dtype):
        return DTypeType.FILE
    
    elif is_filename_type(dtype):
        return DTypeType.FILENAME
    
    elif is_flag_array_type(dtype):
        return DTypeType.FLAG_ARRAY

    elif is_flag_type(dtype):
        return DTypeType.FLAG

    elif is_array_type(dtype):
        return DTypeType.GENERIC_ARRAY
    
    else:
        return DTypeType.GENERIC



# STDOUT
def is_stdout_type(dtype: DataType) -> bool:
    if isinstance(dtype, Stdout):
        return True
    return False

# FLAGS 

def is_flag_array_type(dtype: DataType) -> bool:
    if dtype.name() == 'Array':
        if is_flag_type(dtype):
            return True
    return False

def is_flag_type(dtype: DataType) -> bool:
    basetype = get_base_type(dtype)
    if basetype.name() == 'Boolean':
        return True
    return False


# GENERAL

def get_base_type(dtype: DataType, ensure_single: bool=True) -> DataType:
    while dtype.name() == 'Array' and dtype.subtype():
        dtype = dtype.subtype()
    if ensure_single:
        dtype = ensure_single_type(dtype)
    return dtype

def ensure_single_type(dtype: DataType) -> DataType:
    if isinstance(dtype, UnionType):
        return dtype.subtypes[0]
    return dtype    


# NON-FILES

def is_array_type(dtype: DataType) -> bool:
    if dtype.name() == 'Array':
        return True
    return False

# FILES

def is_file_type(dtype: DataType) -> bool:
    basetype = get_base_type(dtype)
    
    if isinstance(basetype, (File, Directory)):
    # if isinstance(basetype, (File, Filename, Directory)):
        return True
    elif is_file_pair_type(basetype):
        return True
    
    return False

def is_file_array_type(dtype: DataType) -> bool:
    if is_array_type(dtype):
        if is_file_type(dtype):
            return True
    return False
    

# FILE PAIRS

known_file_pair_types = set([
    'FastqPair',
    'FastqGzPair',
])

def is_file_pair_type(dtype: DataType) -> bool:
    basetype = get_base_type(dtype)
    if basetype.name() in known_file_pair_types:
        return True
    return False

def is_file_pair_array_type(dtype: DataType) -> bool:
    if dtype.name() == 'Array':
        if is_file_pair_type(dtype):
            return True
    return False


### FILENAMES

def is_filename_type(dtype: DataType) -> bool:
    basetype = get_base_type(dtype)
    if isinstance(basetype, Filename):
        return True
    return False


### SECONDARIES 

def is_secondary_type(dtype: DataType) -> bool:
    basetype = get_base_type(dtype)
    if isinstance(basetype, File) and basetype.has_secondary_files():
        return True
    return False

def is_secondary_array_type(dtype: DataType) -> bool:
    if dtype.name() == 'Array':
        if is_secondary_type(dtype):
            return True
    return False

def get_extensions(dtype: File, remove_prefix_symbols: bool=False, ignore_duplicates: bool=False) -> list[str]:
    """returns extension of each file for File types with secondaries"""
    primary_ext: str = ''
    secondary_exts: list[str] = []

    # primary extension
    if isinstance(dtype, Directory):
        return []
    if len(dtype.get_extensions()) > 0:
        primary_ext = dtype.get_extensions()[0]
    else:
        primary_ext = 'primary'
    
    # secondary extensions
    if dtype.secondary_files() is not None:
        secondary_exts = dtype.secondary_files()
    else:
        secondary_exts = []

    exts = _sort_extensions(primary_ext, secondary_exts)

    # filters
    if ignore_duplicates:
        exts = _apply_ignore_duplicates_filter(exts)
    if remove_prefix_symbols:
        exts = _apply_remove_prefix_symbols(exts)
    
    return exts

def _apply_ignore_duplicates_filter(exts: list[str]) -> list[str]:
    valid_ext_list: list[str] = []
    
    for ext in exts:
        # check if the normal ext is already declared valid
        if ext in valid_ext_list:
            continue
        # check if the base ext is already declared valid
        elif ext.lstrip('^') in valid_ext_list:
            continue
        else:
            valid_ext_list.append(ext)
    
    return valid_ext_list

def _apply_remove_prefix_symbols(exts: list[str]) -> list[str]:
    return [x.lstrip('.^') for x in exts]

def _sort_extensions(primary_ext: str, secondary_exts: list[str]) -> list[str]:
    out: list[str] = []
    out.append(primary_ext)
    secondary_exts = sorted(secondary_exts, key=lambda x: x.rsplit('.')[-1])
    out += secondary_exts
    return out


### CHANNELS AND VARIABLES 

def datatype_will_be_channel(dtype: DataType) -> bool:
    dtt = get_dtt(dtype)
    if dtt in [
        DTypeType.SECONDARY_ARRAY,
        DTypeType.FILE_PAIR_ARRAY,
        DTypeType.FILE_ARRAY,
    ] and not dtype.optional:
        return True
    
    return False

def datatype_will_be_variable(dtype: DataType) -> bool:
    dtt = get_dtt(dtype)
    # optional file arrays should be variables
    if dtt in [
        DTypeType.SECONDARY_ARRAY,
        DTypeType.FILE_PAIR_ARRAY,
        DTypeType.FILE_ARRAY,
    ] and dtype.optional:
        return True
    
    # files should be variables
    elif dtt in [
        DTypeType.SECONDARY,
        DTypeType.FILE_PAIR,
        DTypeType.FILE,
    ]:
        return True
    
    return False