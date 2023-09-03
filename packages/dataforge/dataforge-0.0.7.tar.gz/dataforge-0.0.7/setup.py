from setuptools import setup, find_namespace_packages

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(
    name='dataforge',
    version='0.0.7',
    author='Phil Schumm',
    author_email='pschumm@uchicago.edu',
    description='Tools for creating and packaging data products',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://gitlab.com/phs-rcg/data-forge',
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    install_requires=[
        'click',
        'confuse',
        'keyring',
        'requests',
        'pandas',
        'gitpython',
        'pyreadstat==1.2.0',
    ],
    extras_require={
        'redcap': ['xmarshal @ git+https://github.com/pschumm/xmarshal.git@d980fd376b7ef3fd0c2376e62c784a54814240a8'],
        'frictionless': ['frictionless~=5.15.10']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_data={'dataforge': ['config_default.yaml']},
    entry_points='''
        [console_scripts]
        redcap_export=dataforge.sources.redcap.api:export
    ''',
)
