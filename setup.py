
from setuptools import setup, find_packages

version = {}
exec(open('deolingo/_version.py').read(), version)

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='deolingo',
    version=version['__version__'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'clingo>=5.7.1',
        'clingox>=1.2.0'
    ],
    entry_points={
        'console_scripts': [
            'deolingo=deolingo.__main__:main'
        ]
    },
    author='Ovidio M. Moar',
    author_email='ovidio.manteiga@udc.es',
    description='A deontic logic solver for explainable deontic reasoning with Answer Set Programming (ASP).',
    license='MIT',
    keywords='ASP, NMR, Deontic Logic, SDL, Deontic Reasoning, Clingo, Xclingo, Telingo',
    url='https://github.com/ovidiomanteiga/deolingo',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ]
)
