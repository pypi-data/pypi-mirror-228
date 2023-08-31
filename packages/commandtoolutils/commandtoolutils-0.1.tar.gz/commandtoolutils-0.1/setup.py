import os
from setuptools import setup, find_packages

# Load the requirements from requirements.in
setup_dir = os.path.dirname(os.path.abspath(__file__))
requirements_file = os.path.join(setup_dir, 'requirements.in')

with open(requirements_file) as f:
    requirements = f.read().splitlines()

setup(
    name='commandtoolutils',
    version='0.1',
    author='Jonathan Borduas',
    description='A featherlight utility package for creating interactive command line tools',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jobordu/menu_utils',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)





