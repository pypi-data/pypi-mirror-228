

from enum import Enum, auto

from janis_core.types import File
from janis_core import (
    TOutput, 
    PythonTool,
)

from janis_core import settings
from janis_core import translation_utils as utils

from ....model.process.outputs import (
    NFProcessOutput,
    NFValProcessOutput,
)

from ....variables import VariableManager


class OType(Enum):
    NON_FILE        = auto()
    NON_FILE_ARRAY  = auto()
    FILE            = auto()


def get_otype(out: TOutput) -> OType:
    if is_file_type(out):
        return OType.FILE
    elif is_non_file_type(out) and is_array_type(out):
        return OType.NON_FILE_ARRAY
    elif is_non_file_type(out):
        return OType.NON_FILE
    else:
        # some future OType
        raise NotImplementedError

def is_file_type(out: TOutput) -> bool:
    basetype = utils.get_base_type(out.outtype)
    basetype = utils.ensure_single_type(basetype)
    if isinstance(basetype, File):
        return True
    return False

def is_array_type(out: TOutput) -> bool:
    if out.outtype.is_array():
        return True
    return False

def is_non_file_type(out: TOutput) -> bool:
    basetype = utils.get_base_type(out.outtype)
    basetype = utils.ensure_single_type(basetype)
    if not isinstance(basetype, File):
        return True
    return False



### PYTHONTOOL OUTPUTS ###
class PythonToolProcessOutputFactory:
    def __init__(
        self, 
        out: TOutput, 
        tool: PythonTool, 
        variable_manager: VariableManager,
    ) -> None:
        self.out = out
        self.tool = tool
        self.variable_manager = variable_manager
        self.otype = get_otype(self.out)
        self.strategy_map = {
            OType.FILE: self.file_output,
            OType.NON_FILE: self.nonfile_output,
            OType.NON_FILE_ARRAY: self.nonfile_array_output,
        }

    @property
    def optional(self) -> bool:
        if self.out.outtype.optional:
            return True
        return False
    
    @property
    def target_file(self) -> str:
        return f'{settings.translate.nextflow.PYTHON_CODE_OUTPUT_FILENAME_PREFIX}{self.out.id()}'

    def create(self) -> NFProcessOutput:
        strategy = self.strategy_map[self.otype]
        process_output = strategy()
        return process_output
    
    def file_output(self) -> NFValProcessOutput:
        # expr = f'"${{file("${{task.workDir}}/" + file("${{task.workDir}}/{self.target_file}").text.replace(\'"\', \'\'))}}", emit: out'
        work_dir = '${task.workDir}'
        local_path = f'file("{work_dir}/{self.target_file}").text.replace(\'"\', \'\')'
        expr = f'"${{file("{work_dir}/" + {local_path})}}"'
        
        new_output = NFValProcessOutput(
            name=self.out.id(),
            janis_tag=self.out.id(),
            is_optional=self.optional, 
            expression=expr
        )
        return new_output
    
    def nonfile_output(self) -> NFValProcessOutput:
        filepath = f'\"${{task.workDir}}/{self.target_file}\"'
        processing = ".text"
        expr = f'"${{file({filepath}){processing}}}"'
        new_output = NFValProcessOutput(
            name=self.out.id(),
            janis_tag=self.out.id(),
            is_optional=self.optional, 
            expression=expr
        )
        return new_output

    def nonfile_array_output(self) -> NFValProcessOutput:
        # filepath = f'\"${{workDir}}/{self.target_file}\"'
        filepath = f'\"${{task.workDir}}/{self.target_file}\"'
        processing = ".text.replace('[', '').replace(']', '')"
        expr = f'"${{file({filepath}){processing}}}"'
        new_output = NFValProcessOutput(
            name=self.out.id(), 
            janis_tag=self.out.id(),
            is_optional=self.optional, 
            expression=expr
        )
        return new_output
