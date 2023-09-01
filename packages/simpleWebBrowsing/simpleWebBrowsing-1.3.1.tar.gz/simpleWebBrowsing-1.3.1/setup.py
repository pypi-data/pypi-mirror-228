from setuptools import setup, find_packages

VERSION = '1.3.1' 
DESCRIPTION = 'Pacote Facilitador Para Manipulação Web'
LONG_DESCRIPTION = 'Pacote Facilitador Para Manipulação Web'

# Setting up
setup(
       # 'name' deve corresponder ao nome da pasta 'verysimplemodule'
        name="simpleWebBrowsing", 
        version=VERSION,
        author="Marco Rocha",
        author_email="<marco.rocha2@outlook.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['webdriver-manager'],         
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)