import setuptools
setuptools.setup(
 name='tmath',
 version='0.4',
 author="Tushali Devikar",
 author_email="tushalidevikar1997@gmail.com",
 description="Only for demo purpose add, sub, mul, div and squ",
 readme = "README.md",
 packages=setuptools.find_packages(),
 classifiers=[
 "Programming Language :: Python :: 3",
 "License :: OSI Approved :: MIT License",
 "Operating System :: OS Independent",
 ],
 
long_description_content_type="text/markdown",

long_description="""Project description

The project was started in 2023 by Tushali Devikar for mathematical function.

Installation
Dependencies
tmath requires:

Python (>= 3.8)

User installation
The easiest way to install tmath is using pip:

pip install -U tmath

USAGE
Quickstart

import tmath
# For Checking Version
print(tmath.__version__)

# The dir() function can be used on all modules
print(dir(tmath))

# For addition
tmath.add(1,2)

# For substraction
tmath.sub(1,2)

# For Multiplication
tmath.mul(1,2)

# For division
tmath.div(1,2)

# For square
tmath.squ(2)

# Use this way also
from tmath import add
print(add(1,2))


Development
The tmath goals are to be helpful, welcoming, and effective. The Development Guide has detailed information about contributing code, documentation, tests, and more. I am included some basic information in this README.

Project History
The project was started in 2023 by Tushali Devikar for mathematical function.

Help and Support


""",
include_package_data=True,
)


    