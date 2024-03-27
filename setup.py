
from setuptools import setup, find_packages

version = {}
exec(open('deolingo/_version.py').read(), version)

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
    description='A Python package for deontic reasoning with Clingo and Xclingo',
    license='MIT',
    keywords='ASP, NMR, Deontic Logic, Deontic Reasoning, Clingo',
    url='https://github.com/ovidiomanteiga/deolingo',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Education :: Language',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
