import sys

from pip.req import parse_requirements
from setuptools import setup, find_packages

if sys.version_info[0] < 3:
    sys.exit('Sorry, onlt Python 3 is supported')


install_reqs = parse_requirements('requirements.pip', session=False)

reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='md2jupyter',
    version='0.1',
    python_requires=">=3.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=reqs,
    entry_points='''
        [console_scripts]
        md2jupyter=md2jupyter.converter:convert
    ''',
)
