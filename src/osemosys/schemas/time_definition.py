import os
import pandas as pd

from .base import *
from osemosys.utils import *

class TimeDefinition(BaseModel):
    years: Union[str,List[int]]



    @classmethod
    def from_simplicity(cls, root_dir):
        None
        