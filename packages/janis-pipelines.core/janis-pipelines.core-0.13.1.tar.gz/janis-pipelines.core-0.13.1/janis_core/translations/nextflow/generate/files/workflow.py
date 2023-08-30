

from typing import Optional

from janis_core import Workflow
from janis_core import settings

from ...casefmt import to_case

from ...model.files import NFFile
from ...model.files import NFImport
from ...model.files import NFImportItem
from ...model.files import NFImportsBlock
from ...model.files import NFFunctionsBlock
from ...model.files import NFChannelDefinitionBlock
from ...model.files import NFVariableDefinitionBlock
from ...model.workflow import NFWorkflow
from ...model.workflow import NFMainWorkflow
from ...model.workflow import NFSubWorkflow
from ...model.process import NFProcess

from .channel_declarations import gen_channels_block
from .variable_declarations import gen_variables_block


def generate_file_workflow(
    nf_workflow: NFWorkflow, 
    nf_processes: dict[str, NFProcess],
    nf_workflows: dict[str, NFWorkflow], 
    wf: Workflow,
    is_subworkflow: bool
    ) -> NFFile:
    """generates nextflow file for nextflow workflow"""
    # detect whether is main workflow or sub workflow
    subtype = 'sub_workflow' if is_subworkflow else 'main_workflow'
    nf_file = NFFile(subtype=subtype, name=nf_workflow.name)
    imports = gen_imports_for_workflow_file(nf_workflow, nf_processes, nf_workflows, wf)
    functions = gen_functions_for_workflow_file(nf_workflow, wf)
    channels = gen_channels_for_workflow_file(nf_workflow, wf)
    variables = gen_variables_for_workflow_file(nf_workflow, wf)

    if imports:
        nf_file.items.append(imports)
    if functions:
        nf_file.items.append(functions)
    if channels:
        nf_file.items.append(channels)
    if variables:
        nf_file.items.append(variables)
    nf_file.items.append(nf_workflow)
    
    return nf_file


def gen_imports_for_workflow_file(
    nf_workflow: NFWorkflow, 
    nf_processes: dict[str, NFProcess],
    nf_workflows: dict[str, NFWorkflow], 
    wf: Workflow
    ) -> Optional[NFImportsBlock]:
    # which tasks (tools, subworkflows) are called in this workflow?
    # (each file created during parsing sub elements needs to be imported)
    imports_block: Optional[NFImportsBlock] = None
    imports_list: list[NFImport] = []

    for step in wf.step_nodes.values():
        task_id = step.tool.id()
        task = _get_task(task_id, nf_processes, nf_workflows)
        relpath = _get_relpath(task, nf_workflow)
        alias = to_case(step.id(), settings.translate.nextflow.NF_PROCESS_CASE) 
        
        # get the task definition we want to import.
        # only 1 task per file.
        nf_item = NFImportItem(name=task.name, alias=alias)
        nf_import = NFImport(method='include', items=[nf_item], source=relpath)
        imports_list.append(nf_import)

    if imports_list:
        imports = [i.get_string() for i in imports_list]
        declarations = []  # declarations are for instantiating etc def jsonSlurper = new JsonSlurper()  
        imports_block = NFImportsBlock(imports, declarations)
    
    return imports_block

def _get_task(task_id: str, nf_processes: dict[str, NFProcess], nf_workflows: dict[str, NFWorkflow]) -> NFProcess | NFWorkflow:
    if task_id in nf_processes:
        return nf_processes[task_id]
    elif task_id in nf_workflows:
        return nf_workflows[task_id]
    else:
        raise Exception(f"Task '{task_id}' not found in nf_processes or nf_workflows")
    
def _get_relpath(task: NFProcess | NFWorkflow, nf_workflow: NFWorkflow) -> str:
    filename = to_case(task.name, settings.translate.nextflow.NF_FILE_CASE)

    # main -> subworkflow
    if isinstance(nf_workflow, NFMainWorkflow) and isinstance(task, NFSubWorkflow):
        relpath = f'./{settings.translate.nextflow.SUBWORKFLOW_OUTDIR}/{filename}'
    
    # main -> process
    elif isinstance(nf_workflow, NFMainWorkflow) and isinstance(task, NFProcess):
        relpath = f'./{settings.translate.nextflow.PROCESS_OUTDIR}/{filename}'

    # subworkflow -> subworkflow
    elif isinstance(nf_workflow, NFSubWorkflow) and isinstance(task, NFSubWorkflow):
        relpath = f'./{filename}'
    
    # subworkflow -> process
    elif isinstance(nf_workflow, NFSubWorkflow) and isinstance(task, NFProcess):
        relpath = f'../{settings.translate.nextflow.PROCESS_OUTDIR}/{filename}'

    # process -> subworkflow
    elif isinstance(nf_workflow, NFProcess) and isinstance(task, NFSubWorkflow):
        relpath = f'../{settings.translate.nextflow.SUBWORKFLOW_OUTDIR}/{filename}'
    
    # process -> process
    elif isinstance(nf_workflow, NFProcess) and isinstance(task, NFProcess):
        relpath = f'./{filename}'

    else:
        raise NotImplementedError
    
    return relpath
    
def gen_functions_for_workflow_file(nf_workflow: NFWorkflow, wf: Workflow) -> Optional[NFFunctionsBlock]:
    # do we need to generate any groovy functions for this workflow?
    # nothing for now
    return None

def gen_channels_for_workflow_file(nf_workflow: NFWorkflow, wf: Workflow) -> Optional[NFChannelDefinitionBlock]:
    # which wf input nodes will be declared as nextflow channels?
    # only valid if in main scope
    return gen_channels_block(nf_workflow, wf)

def gen_variables_for_workflow_file(nf_workflow: NFWorkflow, wf: Workflow) -> Optional[NFVariableDefinitionBlock]:
    # which wf input nodes will be declared as nextflow file variables?
    # only valid if in main scope
    return gen_variables_block(nf_workflow, wf)


