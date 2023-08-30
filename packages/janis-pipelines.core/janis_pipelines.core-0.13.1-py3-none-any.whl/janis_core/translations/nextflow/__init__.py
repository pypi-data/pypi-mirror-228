"""
    Nextflow modelling:
        Using DSL2

    Video: https://youtu.be/I-hunuzsh6A
    DSL2: https://www.nextflow.io/docs/latest/dsl2.html

"""

# from . import casefmt
from . import generate
from . import model
from . import naming
from . import params
# from . import plumbing
from . import preprocessing

from .main import NextflowTranslator
from . import nfgen_utils
from .scope import Scope
from . import task_inputs
from .unwrap import unwrap_expression





