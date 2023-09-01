from setuptools import setup, find_packages

# Read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='petronas-common-utils',
      version='0.0.4',
      license='Apache License, Version 2.0',
      author='Marc Escandell Mari',
      author_email='marc.escandellmari@petronas.com',
      description='A collection of reusable components and utilities for streamlining development across Petronas projects and submodules ',
      long_description=long_description,
      long_description_content_type="text/markdown",
      python_requires='>=3.9',
      packages=find_packages(),
      package_data={'petronas_common_utils': ['resources/*.jar']},
      url='https://github.com/MarcEscandell/petronas-common-utils',
      keywords='petronas-common-utils',
      install_requires=['py4j']
)