"""Installer for the collective.tiles.discussion package."""

from pathlib import Path
from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        Path("README.rst").read_text(),
        Path("CONTRIBUTORS.rst").read_text(),
        Path("CHANGES.rst").read_text(),
    ]
)


setup(
    name="collective.tiles.discussion",
    version="1.0.0a1",
    description="Tile for showing most recent discussion items.",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="Maurits van Rees",
    author_email="maurits@vanrees.org",
    url="https://github.com/collective/collective.tiles.discussion",
    project_urls={
        "PyPI": "https://pypi.org/project/collective.tiles.discussion/",
        "Source": "https://github.com/collective/collective.tiles.discussion",
        "Tracker": "https://github.com/collective/collective.tiles.discussion/issues",
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective", "collective.tiles"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        "plone.app.tiles",
    ],
    extras_require={
        "test": [
            "plone.app.mosaic",
            "plone.app.testing",
            "plone.testing",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
