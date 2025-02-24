import subprocess
import os, re, sys
import os.path
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext

import os
import shutil
from setuptools import setup, Extension
from distutils.command.clean import clean as CleanCommand
from setuptools.command.test import test as TestCommand


class CustomCleanCommand(CleanCommand):
    def run(self):
        CleanCommand.run(self)

        clean_dirs = ['.eggs', 'build', 'dist', '__pycache__', 'betafold.egg-info',
                      'cmake-build-betafold']
        clean_files = ['.pyi', '.so', '.pyd', '.log', ".pyc", ".pyo", ".o"]

        for directory in clean_dirs:
            if os.path.isdir(directory):
                print(f"Removing directory: {directory}")
                shutil.rmtree(directory, ignore_errors=True)

        for root, dirs, files in os.walk("."):
            for file in files:
                for pattern in clean_files:
                    if file.endswith(pattern):
                        file_path = os.path.join(root, file)
                        print(f"Removing file: {file_path}")
                        os.remove(file_path)


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    user_options = build_ext.user_options + [
        ("cmake-build-type=", "b",
         "Build type to pass to CMake. Options are Release for a highly optimized release build, or Debug for a debug build with C++ level logging and assertions."),
    ]

    def initialize_options(self):
        build_ext.initialize_options(self)
        self.cmake_build_type = "Debug"

    def finalize_options(self):
        build_ext.finalize_options(self)

    def run(self):
        try:
            out = subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: "
                + ", ".join(e.name for e in self.extensions)
            )

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        if not os.path.exists(extdir):
            os.makedirs(extdir)

        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + extdir,
            "-DCMAKE_BUILD_TYPE=" + self.cmake_build_type,
            "-DCMAKE_VERBOSE_MAKEFILE=ON",
            "-DPython_EXECUTABLE=" + sys.executable,
            ]

        if not os.path.exists(self.build_lib):
            os.makedirs(self.build_lib)

        build_args = []

        subprocess.check_call(
            ["cmake", ext.sourcedir] + cmake_args, cwd=self.build_lib
        )
        subprocess.check_call(
            ["cmake", "--build", "."] + build_args, cwd=self.build_lib
        )

        try:
            self.copy_extensions_to_source()
        except Exception as e:
            # I think depending on whether or not this is editable the build directory is different, so the built
            # extension lives at another path than self.build_lib, which is why this fails. It also happens that when it
            # fails; the extension is already copied to the source directory, so we can just pass here.
            pass


class CustomTestCommand(TestCommand):
    user_options = CMakeBuild.user_options + [
        ("addopts=", "a", "Additional options to pass to pytest.")
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.cmake_build_type = "Debug"
        self.addopts = []

    def finalize_options(self):
        TestCommand.finalize_options(self)

    def run_tests(self):
        """Run tests using pytest, and handle cases where pytest isn't available."""
        self.run_command("build_ext")
        try:
            import pytest
        except ImportError:
            print("pytest is not installed. Please install it by running:")
            print("    python3 -m pip install pytest")
            sys.exit(1)

        addopts = "" or self.addopts
        addopts = addopts.split(" ")
        errno = pytest.main(addopts)

        sys.exit(errno)



resp = setup(
    name="betafold",
    version="0.0.1",
    author="Andrew Kelleher, Romain Berton, John Nielson",
    author_email="andrew@refereelabs.com",
    description="Simulates energy using the tranformer AI architecture",
    long_description_content_type="text/markdown",
    url="https://github.com/refereelabs/betafold",
    cmdclass={"build_ext": CMakeBuild, "clean": CustomCleanCommand, "test": CustomTestCommand},
    extras_require={
        "dev": ["mypy==1.15.0", "pytest==8.3.4", "pytest-cov==6.0.0", "coverage==7.6.12", "pre-commit==4.1.0",
                "clang-format==19.1.7"]},
    packages=find_packages(),
    package_dir={"tests": "tests"},
    entry_points={},
    setup_requires=[
        "mypy==1.15.0",
        "cmake==3.31.4",
        "pybind11==2.13.6"
    ],
    ext_modules=[CMakeExtension("betafold", sourcedir=".")],
    zip_safe=False,
    python_requires=">=3.10",
)
