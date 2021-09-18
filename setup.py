'''Setup file for Pip package'''
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyExecutioner",
    version="0.0.4",
    author="dravog",
    author_email="dravog78@gmail.com",
    description="A library to execute code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iCodeDevs/EXecutioner",
    project_urls={
        "Bug Tracker": "https://github.com/iCodeDevs/EXecutioner/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Libraries",
        "Development Status :: 3 - Alpha",
    ],
    install_requires=[
        "setuptools>=42",
        "wheel",
        "deepmerge",
        "PyYAML",
        "tabulate",
    ],
    package_dir={"": "."},
    packages=["executioner"],
    python_requires=">=3.6",
)
