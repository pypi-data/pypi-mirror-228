#!/usr/bin/env python3

"""
** Configuration file for pip. **
---------------------------------
"""

import sys

from setuptools import find_packages, setup, Extension

import cutcutcodec


if sys.version_info < (3, 9):
    print(
        "cutcutcodec requires Python 3.9 or newer. "
        f"Python {sys.version_info[0]}.{sys.version_info[1]} detected"
    )
    sys.exit(-1)

module = Extension("cutcutcodec.core.generation.video.fractal.fractal",
    sources=["cutcutcodec/core/generation/video/fractal/fractal.c"],
)


with open("README.rst", "r", encoding="utf-8") as file:
    long_description = file.read()


setup(
    name="cutcutcodec",
    version=cutcutcodec.__version__,
    author="Robin RICHARD (robinechuca)",
    author_email="serveurpython.oz@gmail.com",
    description="video editing software",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://framagit.org/robinechuca/cutcutcodec/-/blob/main/README.md",
    ext_modules=[module],
    data_files=[
        ("cutcutcodec/", ["README.rst", ".pylintrc"]),
    ],
    packages=find_packages(),
    install_requires=[ # dependences: apt install graphviz-dev ffmpeg
        "av", # apt install ffmpeg python3-av
        "cairosvg",
        "click", # apt install python3-click
        "networkx", # apt install python3-networkx
        "numpy >= 1.22", # apt install python3-numpy
        "opencv-contrib-python-headless", # apt install python3-opencv
        "sympy", # apt install python3-sympy
        ("torch >= 2.1.0" if sys.version_info >= (3, 11) else "torch"),
        "tqdm", # apt install python3-tqdm
        "unidecode", # apt install python3-unidecode
    ],
    extras_require={
        "gui": [
            "black", # apt install black python3-pyls-black
            "pdoc3",
            "pyqt6", # apt install python3-pyqt6[.sip]
            "pyqtgraph >= 0.3.1",
            "qtpy",
            "qtpynodeeditor > 0.3.0",
            # "qtpynodeeditor @ git+https://git@github.com/klauer/qtpynodeeditor",
        ], # apt install pylint, python3-pylint-common, python3-pytest
        "optional": [
            "black",
            "pdoc3",
            "pylint",
            "pyqt6",
            "pyqtgraph >= 0.3.1",
            "pytest",
            "qtpy",
            "qtpynodeeditor > 0.3.0",
            # "qtpynodeeditor @ git+https://git@github.com/klauer/qtpynodeeditor",
        ],
    },
    entry_points={
        "console_scripts": [
            "cutcutcodec=cutcutcodec.__main__:main",
            "cutcutcodec-test=cutcutcodec.testing.runtests:test",
        ],
        "gui_scripts": [
            "cutcutcodec-qt=cutcutcodec.gui.__main__:main",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: GPU",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Customer Service",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: C",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics :: Editors",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "Topic :: Multimedia :: Sound/Audio :: Mixers",
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video :: Conversion",
        "Topic :: Multimedia :: Video :: Display",
        "Topic :: Multimedia :: Video :: Non-Linear Editor",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
    keywords=[
        "video",
        "editing",
        "ffmpeg",
        "graphical",
    ],
    python_requires=">=3.9,<3.11",
    project_urls={
        "Source Repository": "https://framagit.org/robinechuca/cutcutcodec",
        # "Bug Tracker": "https://github.com/engineerjoe440/ElectricPy/issues",
        # "Documentation": "http://python-docs.ddns.net/raisin/",
        # "Packaging tutorial": "https://packaging.python.org/tutorials/distributing-packages/",
        },
    include_package_data=True,
)
