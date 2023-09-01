from dflow import (
    upload_s3,
    InputParameter, InputArtifact,
    OutputParameter, OutputArtifact,
)
from dflow.op_template import ScriptOPTemplate

from os import PathLike
import os


class DflowBuilder:

    def __init__(self, name:str, artifact_prefix: str):
        self.name = name
        self.artifact_prefix = artifact_prefix


    def upload_s3(self, path: PathLike, key: str):
        key = os.path.join(self.artifact_prefix, key)
        return upload_s3(path , key)


    def get_output_artifact(self, ):
        ...


    def make_python_step(self, ):
        ...

