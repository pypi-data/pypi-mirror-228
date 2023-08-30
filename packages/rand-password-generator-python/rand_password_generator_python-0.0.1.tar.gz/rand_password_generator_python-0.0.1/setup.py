from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Generating a random password of desired length'
LONG_DESCRIPTION = 'A package that allows to generate passwords of required length and let us choose the complexity, by adding uppercase, lowercase, digits and special characters.'

# Setting up
setup(
    name="rand_password_generator_python",
    version=VERSION,
    author="Shalini Gupta (shalinigupta)",
    author_email="shalinigupta.int25@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description= LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires='',
    keywords=['python', 'video', 'password', 'random characters'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
