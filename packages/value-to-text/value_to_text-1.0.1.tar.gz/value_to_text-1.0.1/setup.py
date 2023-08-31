import setuptools
from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name="value_to_text",
    version="1.0.1",
    license='MIT License',
    author="Edenilson Fernandes dos Santos",
    author_email='santoeen@gmail.com',
    description="classe para converter valor monetario para texto por extenso... e percentual por extenso",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords='value_to_text write_value numero para texto valor para texto num_to_text num2text',
    include_package_data=True,
    packages=setuptools.find_packages(),
    zip_safe=False,
    url = "https://github.com/edenilsonsantos/value_to_text",
    project_urls = {
        "repository": "https://github.com/edenilsonsantos/value_to_text",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires='>=3.8',
    install_requires=[]
)