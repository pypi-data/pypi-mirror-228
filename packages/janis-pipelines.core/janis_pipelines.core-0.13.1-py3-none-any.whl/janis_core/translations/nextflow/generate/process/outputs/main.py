
from typing import Any

from janis_core import (
    ToolOutput, 
    TOutput, 
    CommandTool, 
    PythonTool,
)

from ....scope import Scope
from ....model.process.outputs import NFProcessOutput

from .factory_cmdtool import CmdtoolProcessOutputFactory
from .factory_pythontool import PythonToolProcessOutputFactory

from ....variables import VariableManager

def gen_nf_process_outputs(
    tool: CommandTool | PythonTool,
    variable_manager: VariableManager, 
    ) -> list[NFProcessOutput]:
    
    process_outputs: list[NFProcessOutput] = []
    # name_clashes: set[str] = set()
    # if isinstance(tool, CommandTool):
    #     name_clashes = _ensure_unique_filenames(tool, sources)
    
    for out in tool.outputs():
        if isinstance(out, ToolOutput) and isinstance(tool, CommandTool):
            factory = CmdtoolProcessOutputFactory(
                out=out, 
                tool=tool, 
                variable_manager=variable_manager, 
            )
        if isinstance(out, TOutput) and isinstance(tool, PythonTool):
            factory = PythonToolProcessOutputFactory(
                out=out, 
                tool=tool, 
                variable_manager=variable_manager, 
            )
    
        new_output = factory.create()
        process_outputs.append(new_output)
    
    return process_outputs




# def _ensure_unique_filenames(tool: CommandTool, sources: dict[str, Any]) -> set[str]:
#     """
#     Ensures that files have unique filename. 
#     Changes filename to the path of 
#     This is necessary because nextflow will stage files into a process using filename only. 
#     For example, if process1 creates a file @ 'data/data.txt' and another file @ 'outs/data.txt',
#     for a process which stages those two files, they will be both staged as '{job_working_dir}/data.txt'.
#     The filenames now clash, as the folder structure was not preserved. 
#     """
#     name_clashes: set[str] = set()
#     for out in tool.outputs():
#         if isinstance(out.output_type, File):
#             process_inputs = get_process_inputs(sources)
#             param_inputs = get_param_inputs(sources)
#             internal_inputs = get_internal_inputs(tool, sources)
#             if isinstance(out.selector, list):
#                 pass

#             expr = unwrap_expression(
#                 val=out.selector, 
#                 tool=tool, 
#                 sources=sources,
#                 process_inputs=process_inputs,
#                 param_inputs=param_inputs,
#                 internal_inputs=internal_inputs,
#             )

#             print()
#     return name_clashes

