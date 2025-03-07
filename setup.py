"""
toolbox-acclimate
-------------------------

Python package and collection of example scripts for preparing simulations and processing output of the `Acclimate model "https://github.com/acclimate/acclimate".

Some methods may also be suitable for the general setup and processing of ensemble simulations.

"""

from setuptools import find_packages, setup

import versioneer

NAME = "toolbox_acclimate"
SHORT_DESCRIPTION = (
    "Python library and scripts for ensemble simulations and processing output of the Acclimate model"
)
AUTHORS = [
    ("Lennart Quante", "https://github.com/lquante"),
    ("Robin Middelanis", "https://github.com/rmiddelanis"),
    ("Sven Willner", "https://github.com/swillner"),
]
URL = "https://github.com/acclimate/toolbox"
PROJECT_URLS = {
    "Bug Reports": "https://github.com/acclimate/toolbox/issues",
    # "Documentation": "https://acclimate-toolbox.readthedocs.io/en/latest",
    "Source": "https://github.com/acclimate/toolbox",
}
LICENSE = "GNU Affero General Public License v3.0 or later"
CLASSIFIERS = [
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
]
REQUIREMENTS_INSTALL = ["numpy>=1.7", "netcdf4", 'xarray', 'pandas']
REQUIREMENTS_DOCS = ["sphinx>=1.8", "sphinx_rtd_theme"]
REQUIREMENTS_DEV = [
    "black",
    "bandit",
    "flake8",
    "isort",
    "pydocstyle",
    "pylint",
] + REQUIREMENTS_DOCS

REQUIREMENTS_EXTRAS = {
    "docs": REQUIREMENTS_DOCS,
    "dev": REQUIREMENTS_DEV,
}

setup(
    name=NAME,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    python_requires=">3",
    description=SHORT_DESCRIPTION,
    long_description=SHORT_DESCRIPTION,
    long_description_content_type="text/x-rst",
    author=", ".join([author[0] for author in AUTHORS]),
    author_email=", ".join([author[1] for author in AUTHORS]),
    url=URL,
    project_urls=PROJECT_URLS,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIREMENTS_INSTALL,
    extras_require=REQUIREMENTS_EXTRAS,
)
