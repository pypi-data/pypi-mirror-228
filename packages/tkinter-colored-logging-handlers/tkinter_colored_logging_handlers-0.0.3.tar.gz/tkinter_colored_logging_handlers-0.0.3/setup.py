from setuptools import setup, find_packages


NAME = "tkinter_colored_logging_handlers"
VERSION = "0.0.3"
PYTHON_REQUIRES = ">=3.6"
REQUIRES = []

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=NAME,
    version=VERSION,
    description="Tkinker Logger",
    author="yuki",
    author_email="yuki@yuki0311.com",
    url="https://github.com/fa0311/tkinter_colored_logging_handlers",
    keywords=["tkinter", "logging", "handler"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="MIT",
    long_description_content_type="text/markdown",
    long_description=long_description,
    package_data={"tkinter_colored_logging_handlers": ["py.typed"]},
)
