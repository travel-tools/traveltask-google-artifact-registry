from dataclasses import dataclass


@dataclass
class TaskConfig:

    # Travel parameters
    context: str
    task: str

    # Custom parameters
