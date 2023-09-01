'''Copyright (c) 2022 Z.Ai Inc. ALL RIGHTS RESERVED

Z.Ai official client SDK.
'''

import pathlib
import setuptools

long_description = (pathlib.Path(__file__).parent.joinpath('README.md').read_text())

setuptools.setup(
    name='zaiclient',
    version='4.0.1',
    description='Z.Ai official client SDK.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zaikorea/zaiclient-python',
    author='Z.Ai Inc.',
    author_email='tech@zaikorea.org',
    license='Proprietary',
    # PyPI package information.
    classifiers=[
        'License :: Other/Proprietary License',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=setuptools.find_packages(exclude=( "tests",)),
    include_package_data=True,
    install_requires=pathlib.Path('requirements.txt').read_text().splitlines(),
    keywords='zai client sdk api ml',
)
