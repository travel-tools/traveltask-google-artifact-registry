from traveltask_google_artifact_registry.config import TaskConfig


def perform(config: TaskConfig):

    print(f"Task: {config.task} for {config.context}")
