import os
import sys

from travel.config.bag import Bag
from travel.config.reader import parse_bags
from travel.tools.pip import Pip
from travel.tools.python import Python
from travel.tools.venv import Virtualenv

from traveltask_google_artifact_registry.config import TaskConfig


PyPI_keyrings_google_artifact_registry_auth = "keyrings.google-artifactregistry-auth"


def _get_index_url(config: TaskConfig):
    return f"https://{config.region}-python.pkg.dev/{config.project}/{config.repository}/"


def _fix_requirements(bag: Bag, python: Python, config: TaskConfig) -> None:
    # Get the right venv
    env = Virtualenv(bag)
    
    if not os.path.exists(env.path):
        raise ValueError(
            "The venv must be created before running the 'fix_requirements' action. "
            "Did you forget to run 'travel setup'?"
        )
        
    with open(env.requirements_file, "rt") as f:
        requirements = f.read().splitlines()
        
    if PyPI_keyrings_google_artifact_registry_auth not in requirements:
        requirements.append(PyPI_keyrings_google_artifact_registry_auth)
        
    index_url = _get_index_url(config) + "simple"
    requirements.insert(0, f"--extra-index-url {index_url}")
    
    with open(env.requirements_file, "wt") as f:
        for requirement in requirements:
            f.write(f"{requirement}\n")


def _install(bag: Bag, python: Python, config: TaskConfig):

    # Validate input
    if not config.packages:
        raise ValueError("Parameter 'packages' cannot be empty and must be in the format '<package>==<version>'")

    # Get the right venv
    env = Virtualenv(bag)
    env.create()

    # Get the site-packages folder
    if os.name == "posix":
        lib = os.path.join(env.path, "lib")
        lib = os.path.join(lib, [d for d in os.listdir(lib) if d.startswith("python")][0])
    else:
        lib = os.path.join(env.path, "Lib")
    site_packages = os.path.join(lib, "site-packages")

    # Install the packages
    pip = Pip(python)
    index_url = _get_index_url(config)+"simple/"
    pip.run(f"install --extra-index-url {index_url} --target {site_packages} {config.packages}")


def _upload(bag: Bag, python: Python, config: TaskConfig):

    # Get path to dist and url of registy
    dist = os.path.join(bag.build_folder, "package", "dist")
    url = _get_index_url(config)

    # Upload with twine
    python.run(f"-m twine upload --repository-url {url} {dist}/*")


def perform(config: TaskConfig):

    python = Python(sys.executable)
    bag, _ = parse_bags(config.context)

    if config.action == "install":
        _install(bag, python, config)
    elif config.action == "upload":
        _upload(bag, python, config)
    elif config.action == "fix_requirements":
        _fix_requirements(bag, python, config)
    else:
        raise ValueError(f"Uknown action (valid options are 'upload', 'install' or 'fix_requirements'): {config.action}")
