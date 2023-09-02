from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Build stracture data'
LONG_DESCRIPTION = 'A package that allows to build tangelo data..'

# Setting up
setup(
    name="tangelokit",
    version=VERSION,
    author="Arnold Blandon",
    author_email="arnold.blandon1@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(exclude=["tests"]),
    install_requires=[],
    keywords=['python', 'tangelo', 'kit', 'data'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)