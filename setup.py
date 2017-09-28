from setuptools import setup
import sys

requirements = ['numpy']

# WE MIGHT WANT TO CHANGE SOME OF THIS
if sys.version_info < (2, 7):
    sys.stdout.write("At least Python 3.3 is required.\n")
    sys.exit(1)

#import versioneer

setup(
    name='pyncorr',
    version="0.1",
    description='A python implementation for calculating n-pt correlation functions relevant to understanding the large-scale structure of galaxy clustering.',
    url='https://github.com/mattbellis/pyncorr',
    author='Fred Genier and Matt Bellis',
    author_email='mbellis@siena.edu',
    license='GPL3',
    packages = ['pyncorr'],
    #install_requires = requirements,
    #tests_require = ['pytest', 'pytest-cov'],
    classifiers=[ 
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Users',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'License :: Public Domain',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.6',
    ],
)
