#!/usr/bin/env python

import sys
import os
import warnings

from setuptools import setup
from setuptools import Extension
from Cython.Build import cythonize

import numpy

lib_talib_name = 'ta_lib'  # the underlying C library's name

runtime_lib_dirs = []

platform_supported = False
for prefix in ['darwin', 'linux', 'bsd', 'sunos']:
    if prefix in sys.platform:
        platform_supported = True
        include_dirs = [
            '/usr/include',
            '/usr/local/include',
            '/opt/include',
            '/opt/local/include',
        ]
        if 'TA_INCLUDE_PATH' in os.environ:
            include_dirs.append(os.environ['TA_INCLUDE_PATH'])
        lib_talib_dirs_all = [
            '/usr/lib',
            '/usr/local/lib',
            '/usr/lib64',
            '/usr/local/lib64',
            '/opt/lib',
            '/opt/local/lib',
        ]
        lib_talib_dirs = []
        for lib_talib_dir in lib_talib_dirs_all:
            if os.path.exists(lib_talib_dir):
                lib_talib_dirs.append(lib_talib_dir)
        if 'TA_LIBRARY_PATH' in os.environ:
            runtime_lib_dirs = os.environ['TA_LIBRARY_PATH']
            if runtime_lib_dirs:
                runtime_lib_dirs = runtime_lib_dirs.split(os.pathsep)
                lib_talib_dirs.extend(runtime_lib_dirs)
        break

if sys.platform == "win32":
    platform_supported = True
    lib_talib_name = 'ta_libc_cdr'
    include_dirs = [r"c:\ta-lib\c\include"]
    lib_talib_dirs = [r"c:\ta-lib\c\lib"]

if not platform_supported:
    raise NotImplementedError(sys.platform)

include_dirs.insert(0, numpy.get_include())

for lib_talib_dir in lib_talib_dirs:
    try:
        files = os.listdir(lib_talib_dir)
        if any(lib_talib_name in f for f in files):
            break
    except OSError:
        pass
else:
    warnings.warn('Cannot find ta-lib library, installation may fail.')

ext_modules = [
    Extension(
        'talib._ta_lib',
        ['talib/_ta_lib.pyx'],
        define_macros=[],
        include_dirs=include_dirs,
        library_dirs=lib_talib_dirs,
        libraries=[lib_talib_name],
        runtime_library_dirs=runtime_lib_dirs
    )
]

setup(
    name = 'TA-Lib',
    version = '0.4.10',
    packages = ['talib'],

    install_requires=['numpy>=1.11.1', 'Cython>=0.24.1'],

    author = 'John Benediktsson',
    author_email = 'mrjbq7@gmail.com',
    description = 'Python wrapper for TA-Lib',
    url = 'http://github.com/mrjbq7/ta-lib',
    download_url = 'https://github.com/mrjbq7/ta-lib/releases',
    classifiers = [
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Cython",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Financial and Insurance Industry",
    ],
    ext_modules = cythonize(ext_modules),
)
