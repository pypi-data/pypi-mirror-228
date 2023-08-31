""" Setup script for PythonEDI

"""
import re
from setuptools import setup, find_packages

long_description = """Pyedi830 uses JSON format definitions to make it easy to parse and convert from EDI830 file to JSON, CSV, HTML, PDF file/data."""

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name="pyedi830",
    description="EDI 830 parser/converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dev0088/pyedi830",
    author="Ninja Dev",
    author_email="ninjadev999@gmail.com",
    license="MIT",
    version="1.5.1",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Topic :: Office/Business",
        "Topic :: Text Processing"
    ],
    keywords="x12 edi 830 csv pdf html",
    packages=['pyedi830', 'pyedi830.formats', 'pyedi830.template'],
    package_data={
        "pyedi830": ["formats/*.json", "template/*.html"]
    },
    install_requires=['colorama', 'pandas', 'jinja2', 'weasyprint'],
    include_package_data=True,
)
