from setuptools import find_packages,setup
from typing import List
HYPENE = "-e ."

def get_requirements(file_path:str)->List[str]:
    requirements = []
    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [req.replace("\n","") for req in requirements]
        if HYPENE in requirements:
            requirements.remove(HYPENE)
    return requirements

setup(
name = "mlproject",
version="0.0.1",
author="ashishiyer",
packages=find_packages(),
install_requires=get_requirements("requirements.txt")

)