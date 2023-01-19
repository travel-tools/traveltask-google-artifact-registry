import os
from setuptools import setup, find_packages


requirements_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")


if __name__ == "__main__":
    with open(requirements_file, "rt") as f:
        requirements = f.read().splitlines()
    
    setup(
        description="A Travel task to download/upload a Python package from/to Google Artifact Registry using pip",
        include_package_data=True,
        install_requires=requirements,
        name="traveltask_google_artifact_registry",
        packages=find_packages(),
        version="0.0.0",
    )
