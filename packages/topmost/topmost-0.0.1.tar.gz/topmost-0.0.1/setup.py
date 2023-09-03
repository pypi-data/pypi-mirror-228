from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Topmost: Neural Topic Modeling System Tookit'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="topmost",
        version=VERSION,
        author="Xiaobao Wu",
        author_email="xiaobao002@e.ntu.edu.sg",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        url='',
        packages=find_packages(),
        license="MIT",
        install_requires=[], # add any additional packages that needs to be installed along with your package. Eg: 'caer'
        keywords=['python', 'topic model', 'neural topic model'],
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
