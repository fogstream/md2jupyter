from setuptools import setup, find_packages

from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.pip', session=False)

reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='md2jupyter',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=reqs,
    entry_points='''
        [console_scripts]
        md2jupyter=md2jupyter:convert
    ''',
)
