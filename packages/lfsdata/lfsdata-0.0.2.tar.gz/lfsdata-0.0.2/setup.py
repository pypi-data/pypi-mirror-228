"""Install packages as defined in this file into the Python environment."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()
setup(
    name="lfsdata",
    version="0.0.2",
    author="Arusha Developers",
    author_email="info@arusha.dev",
    maintainer="Hamed Khademi Khaledi",
    maintainer_email="khaledihkh@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arushadev/lfsdata",
    packages=find_packages(),
    namespace_packages=['lfsdata'],
    install_requires=[
        "setuptools>=45.0",
        "coloredlogs",
        "python-gitlab",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.0",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
    ],
    python_requires='>=3.11',
)
