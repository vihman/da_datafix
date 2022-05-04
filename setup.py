import pathlib
from setuptools import find_packages, setup

from da_datafix import __version__

HERE = pathlib.Path(__file__).parent.resolve()
README = (HERE / "README.rst").read_text()

setup(
    name="da_datafix",
    description="Digiaudit Data Fixing package",
    long_description=README,
    long_description_content_type="text/x-rst",
    packages=find_packages(),
    version=__version__,
    python_requires='>=3.8',
    install_requires=[
        "numpy",
        "pandas"
    ]
)
